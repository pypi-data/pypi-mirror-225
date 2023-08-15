#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
"""
Flask WSGI web app for managing student submissions & grading them w/
potluck. Fork of Ocean server for Codder. Can withhold feedback until
after the deadline, so the display of feedback is detached a bit from
the generation of feedback. Also supports exercises, which are graded
immediately & submitted programmatically via potluck_delivery (generally
set up to deliver when tests are run).

potluck_server/app.py

To run the server, the current directory must contain `ps_config.py` or
`ps_config.py.example` which will be copied to create `ps_config.py`. The
additional `secret` and `syntauth` files will be created automatically
using `os.urandom` if necessary; see `rundir` in the package directory
for an example.

Note that the `potluck` package must be installed, along with `flask`,
`jinja2`, and `flask_cas`. Additionally, `flask_talisman` and/or
`flask_seasurf` may be installed, and if present they will be used to
provide additional layers of security. Finally, if `pyopenssl` is
installed alongside `flask_talisman`, even when running in debug mode
HTTPS and the content-security-policy will be enabled, which helps spot
errors earlier at the cost of having to click through a security warning
from your browser about the self-signed certificate.

Students log in using CAS, select a project, and submit one file per task
(where the filename is checked against a configurable list), and can view
their most recent submission, see any warnings on it, or even submit a
revision. Once the deadline + review period has passed (modulo
extensions, or immediately in some cases), the full report from each
student's last on-time submission is made available. Main routes:

/ (route_index):
    Checks for CAS authentication and redirects to login page or to
    dashboard.

/dashboard (route_default_dash):
    Auto-redirects to the dashboard for the "current" course/semester
    based on configuration.

/**$course**/**$semester**/dashboard (route_dash):
    Main interface w/ rows for each project. Each row has sub-rows for
    each task w/ upload button to submit the task and link to latest
    feedback for that task. As well as project submission options, the
    dashboard has a course concepts overview that tracks competencies
    demonstrated in projects and via exercises. TODO: Concepts overview.

/**$course**/**$semester**/feedback/**$username**/**$phase**/**$project**/
  **$task**
(route_feedback):
    Displays latest feedback for a given user/phase/project/task.
    Pre-deadline this just shows any warnings.
    Allows resubmission of the task directly from this page.

/**$course**/**$semester**/evaluate/**$username**/**$phase**/**$project**/
  **$task** (route_evaluate):
    Admin-only route that shows feedback for a given
    user/phase/project/task, and allows the admin to enter a custom note
    that the student will see, and also to override the grade that will
    be entered on the gradesheet for that task. Note that grade overrides
    for revisions are still subject to the normal revision score cap in
    terms of their contributions to a final grade. Feedback for a
    non-submitted task may be overridden however.

/**$course**/**$semester**/set_eval/**$username**/**$phase**/**$project**/
  **$task** (route_set_evaluation):
    Form target for updating grade overrides from `route_evaluate`.

/**$course**/**$semester**/submit/**$username**/**$project**/**$task**
(route_submit):
    Form target for submissions; accepts valid submissions and redirects
    back to feedback page.

/**$course**/**$semester**/extension/**$project** (route_extension):
    Request an extension for a project (automatically grants the default
    extension; the extension always applies only to the initial deadline,
    not to revisions; and the extension applies to the whole problem set,
    not per-task).
    # TODO: Allow students to revoke requested extensions if they haven't
    # started using them yet.

/**$course**/**$semester**/solution/**$project**/**$task** (route_solution):
    View the solution code for a particular task. Only available once a
    task is finalized (on a per-student basis to deal with extensions).

/**$course**/**$semester**/gradesheet (route_full_gradesheet):
    An overview of all grades for ALL tasks and projects.

/**$course**/**$semester**/gradesheet/**$project** (route_gradesheet):
    An overview of all grades for a specific problem set, visible only to
    admins.

/**$course**/**$semester**/deliver (route_deliver):
    Delivery endpoint for POST data on exercise outcomes, which are
    submitted via the stand-alone `potluckDelivery` module. Unlike normal
    submissions, we do not run any code from these, and we also don't
    verify authorship (TODO: that!).

/**$course**/**$semester**/exercise/**$user**/**$exercise** (route_exercise):
    Shows submitted material & status for an exercise submission for a
    particular user received via `route_deliver`. Admins can modify
    exercise feedback for an individual exercise from this page.

/**$course**/**$semester**/ex_override/**$user**/**$exercise**
  (route_exercise_override):
    Form target for overriding exercise grades OR exercise group grades
    from `route_exercise`.

    TODO: Enable per-user dashboard vies without MASQUERADE and then let
    exercise group overrides be entered from the dashboard view of a
    particular student...

/**$course**/**$semester**/ex_gradesheet/**$group** (route_ex_gradesheet):
    An overview of all grades for a specific exercise group, visible only to
    admins.
    # TODO: Make this faster?
"""

# Attempts at 2/3 dual compatibility:
from __future__ import print_function

__version__ = "1.2.20"

import sys


# IF we're not in pyhton3:
if sys.version_info[0] < 3:
    reload(sys) # noqa F821
    # Set explicit default encoding
    sys.setdefaultencoding('utf-8')
    # Rename raw_input
    input = raw_input # noqa F821
    ModuleNotFound_or_Import_Error = ImportError
    anystr = (str, unicode) # noqa F821
else:
    ModuleNotFound_or_Import_Error = ModuleNotFoundError
    anystr = (str, bytes)


def ensure_directory(target):
    """
    makedirs 2/3 shim.
    """
    if sys.version_info[0] < 3:
        try:
            os.makedirs(target)
        except OSError:
            pass
    else:
        os.makedirs(target, exist_ok=True)


# Main imports
import os, subprocess, shutil # noqa E402
import datetime, time, random, copy, csv, re # noqa E402
import zipfile # noqa E402

import flask # noqa E402
import flask_cas # noqa E402
import jinja2 # noqa E402
import bs4 # noqa E402
import werkzeug # noqa E402

from flask import json # noqa E402

from . import storage # noqa E402

# Load potluck modules:
import potluck.render # noqa: E402
import potluck.html_tools # noqa: E402
import potluck.time_utils # noqa: E402


# Look for safe_join both in flask and in werkzeug...
if hasattr(flask, "safe_join"):
    safe_join = flask.safe_join
elif hasattr(werkzeug.utils, "safe_join"):
    safe_join = werkzeug.utils.safe_join
else:
    print(
        "Warning: safe_join was not found in either flask OR"
        " werkzeug.utils; using an unsafe function instead."
    )
    safe_join = lambda *args: os.path.join(*args)


#-------------#
# Setup setup #
#-------------#

class InitApp(flask.Flask):
    """
    A Flask app subclass which runs initialization functions right
    before app startup.
    """
    def __init__(self, *args, **kwargs):
        """
        Arguments are passed through to flask.Flask.__init__.
        """
        self.actions = []
        # Note: we don't use super() here since 2/3 compatibility is
        # too hard to figure out
        flask.Flask.__init__(self, *args, **kwargs)

    def init(self, action):
        """
        Registers an init action (a function which will be given the app
        object as its only argument). These functions will each be
        called, in order of registration, right before the app starts,
        withe the app_context active. Returns the action function
        provided, so that it can be used as a decorator, like so:

        ```py
        @app.init
        def setup_some_stuff(app):
            ...
        ```
        """
        self.actions.append(action)
        return action

    def setup(self):
        """
        Runs all registered initialization actions. If you're not running
        a debugging setup via the `run` method, you'll need to call this
        method yourself (e.g., in a .wsgi file).
        """
        with self.app_context():
            for action in self.actions:
                action(self)

    def run(self, *args, **kwargs):
        """
        Overridden run method runs our custom init actions with the app
        context first.
        """
        self.setup()
        # Note: we don't use super() here since 2/3 compatibility is
        # too hard to figure out
        flask.Flask.run(self, *args, **kwargs)


#-------#
# Setup #
#-------#

# Create our app object:
app = InitApp("potluck_server")


# Default configuration values if we really can't find a config file
DEFAULT_CONFIG = {
    "EVALUATION_BASE": '.',
    "POTLUCK_EVAL_PYTHON": None,
    "POTLUCK_EVAL_SCRIPT": None,
    "POTLUCK_EVAL_IMPORT_FROM": None,
    "DEFAULT_COURSE": 'test_course',
    "DEFAULT_SEMESTER": 'fall2021',
    "SUPPORT_EMAIL": 'username@example.com',
    "SUPPORT_LINK": '<a href="mailto:username@example.com">User Name</a>',
    "NO_DEBUG_SSL": False,
    "CAS_SERVER": 'https://login.example.com:443',
    "CAS_AFTER_LOGIN": 'dashboard',
    "CAS_LOGIN_ROUTE": '/module.php/casserver/cas.php/login',
    "CAS_LOGOUT_ROUTE": '/module.php/casserver/cas.php/logout',
    "CAS_AFTER_LOGOUT": 'https://example.com/potluck',
    "CAS_VALIDATE_ROUTE": '/module.php/casserver/serviceValidate.php',
    "DEFAULT_PROJECT_URL_FORMAT": (
        'https://example.com/archive/test_course_{semester}/'
        'public_html/projects/{project}'
    ),
    "DEFAULT_TASK_URL_FORMAT": (
        'https://example.com/archive/test_course_{semester}/'
        'public_html/project/{project}/{task}'
    ),
    "DEFAULT_EXERCISE_URL_FORMAT": (
        'https://example.com/archive/test_course_{semester}/'
        'public_html/lectures/{group}'
    ),
    "TASK_INFO_FILE": 'tasks.json',
    "CONCEPTS_FILE": 'pl_concepts.json',
    "ADMIN_INFO_FILE": 'potluck-admin.json',
    "ROSTER_FILE": 'roster.csv',
    "STUDENT_INFO_FILE": 'student-info.tsv',
    "SYNC_PORT": 51723,
    "FINAL_EVAL_TIMEOUT": 60,
    "USE_XVFB": False,
    "XVFB_SERVER_ARGS": "-screen 0 1024x768x24",
    "REMAP_STUDENT_INFO": {},
    "SCORE_BASIS": 100,
    "ROUND_SCORES_TO": 0,
    "EVALUATION_SCORES": {
        "excellent": 100,
        "complete": 100,
        "almost complete": 85,
        "partially complete": 75,
        "incomplete": 0,
        "__other__": None
    },
    "REVISION_MAX_SCORE": 100,
    "BELATED_MAX_SCORE": 85,
    "TIMELINESS_POINTS": 10,
    "TIMELINESS_ATTEMPT_THRESHOLD": 75,
    "TIMELINESS_COMPLETE_THRESHOLD": 85,
    "TASK_WEIGHT": 2,
    "EXERCISE_WEIGHT": 1,
    "OUTCOME_WEIGHT": 0.25,
    "EXERCISE_GROUP_THRESHOLD": 0.895,
    "EXERCISE_GROUP_PARTIAL_THRESHOLD": 0.495,
    "EXERCISE_GROUP_CREDIT_BUMP": 0.0,
    "LATE_EXERCISE_CREDIT_FRACTION": 0.5,
    "GRADE_THRESHOLDS": {
        "low": 75,
        "mid": 90
    }
}

# Loads configuration from file `ps_config.py`. If that file isn't
# present but `ps_config.py.example` is, copies the latter as the former
# first. Note that this CANNOT be run as an initialization pass, since
# the route definitions below require a working configuration.
try:
    sys.path.append('.')
    app.config.from_object('ps_config')
except Exception as e: # try copying the .example file?
    if os.path.exists('ps_config.py.example'):
        print("Creating new 'ps_config.py' from 'ps_config.py.example'.")
        shutil.copyfile('ps_config.py.example', 'ps_config.py')
        app.config.from_object('ps_config')
    else:
        print(
            "Neither 'ps_config.py' nor 'ps_config.py.example' is"
            " available, or there was an error in parsing them, so"
            " default configuration will be used."
        )
        print("CWD is:", os.getcwd())
        print("Error loading 'ps_config.py' was:", str(e))
        app.config.from_mapping(DEFAULT_CONFIG)
finally:
    sys.path.pop() # no longer need '.' on path...


class NotFound():
    """
    Placeholder class for fallback config values, since None might be a
    valid value.
    """
    pass


def fallback_config_value(key_or_keys, *look_in):
    """
    Gets a config value from the first dictionary it's defined in,
    falling back to additional dictionaries if the value isn't found.
    When the key is specified as a list or tuple of strings, repeated
    dictionary lookups will be used to retrieve a value.

    Returns the special class `NotFound` as a default value if none of
    the provided dictionaries have a match for the key or key-path
    requested.
    """
    for conf_dict in look_in:
        if isinstance(key_or_keys, (list, tuple)):
            target = conf_dict
            for key in key_or_keys:
                if not isinstance(target, dict):
                    break
                try:
                    target = target[key]
                except KeyError:
                    break
            else:
                return target
        elif key_or_keys in conf_dict:
            return conf_dict[key_or_keys]
        # else continue the loop
    return NotFound


def usual_config_value(
    key_or_keys,
    taskinfo,
    task=None,
    project=None,
    exercise=None,
    default=NotFound
):
    """
    Runs `fallback_config_value` with a task or exercise dictionary,
    then the specified task info dictionary, then the app.config values,
    and then the DEFAULT_CONFIG values.

    `task` will take priority over `project`, which takes priority over
    `exercise`; in general only one should be specified; each must be an
    ID string (for a task, a project, or an exercise group).

    If provided, the given `default` value will be returned instead of
    `NotFound` if the result would otherwise be `NotFound`.
    """
    if task is not None:
        result = fallback_config_value(
            key_or_keys,
            taskinfo.get("tasks", {}).get(task, {}),
            taskinfo,
            app.config,
            DEFAULT_CONFIG
        )

    elif project is not None:
        projects = taskinfo.get(
            "projects",
            taskinfo.get("psets", {})
        )
        matching = [p for p in projects if p["id"] == project]
        if len(matching) > 0:
            first = matching[0]
        else:
            first = {}
        result = fallback_config_value(
            key_or_keys,
            first,
            taskinfo,
            app.config,
            DEFAULT_CONFIG
        )

    elif exercise is not None:
        exgroups = taskinfo.get("exercises", [])
        matching = [
            g
            for g in exgroups
            if g.get("group", None) == exercise
        ]
        if len(matching) > 0:
            first = matching[0]
        else:
            first = {}
        result = fallback_config_value(
            key_or_keys,
            first,
            taskinfo,
            app.config,
            DEFAULT_CONFIG
        )
    else:
        result = fallback_config_value(
            key_or_keys,
            taskinfo,
            app.config,
            DEFAULT_CONFIG
        )

    return default if result is NotFound else result


@app.init
def setup_jinja_loader(app):
    """
    Set up templating with a custom loader that loads templates from the
    potluck package if it can't find them in this package. This is how
    we share the report template between potluck_server and potluck.
    """
    app.jinja_loader = jinja2.ChoiceLoader([
        jinja2.PackageLoader("potluck_server", "templates"),
        jinja2.PackageLoader("potluck", "templates")
    ])


@app.init
def enable_CAS(app):
    """
    Enable authentication via a Central Authentication Server.
    """
    global cas
    cas = flask_cas.CAS(app)


@app.init
def setup_potluck_reporting(app):
    """
    Setup for the potluck.render module (uses defaults).
    """
    potluck.render.setup()


@app.init
def create_secret_key(app):
    """
    Set secret key from secret file, or create a new secret key and
    write it into the secret file.
    """
    if os.path.exists("secret"):
        with open("secret", 'rb') as fin:
            app.secret_key = fin.read()
    else:
        print("Creating new secret key file 'secret'.")
        app.secret_key = os.urandom(16)
        with open("secret", 'wb') as fout:
            fout.write(app.secret_key)


@app.init
def initialize_storage_module(app):
    """
    Initialize file access and storage system.
    """
    storage.init(app.config)


@app.init
def ensure_required_folders(app):
    """
    Ensures required folders for the default course/semester.
    TODO: What about non-default courses/semesters? If they're fine, is
    this even necessary?
    """
    this_course = app.config.get("DEFAULT_COURSE", 'unknown')
    this_semester = app.config.get("DEFAULT_SEMESTER", 'unknown')
    storage.ensure_directory(
        storage.evaluation_directory(this_course, this_semester)
    )
    storage.ensure_directory(
        storage.submissions_folder(this_course, this_semester)
    )


#----------------#
# Security setup #
#----------------#

NOAUTH = False
USE_TALISMAN = True
if __name__ == "__main__":
    # Print intro here...
    print("This is potluck_server version {}".format(__version__))

    print("WARNING: Running in debug mode WITHOUT AUTHENTICATION!")
    input("Press enter to continue in debug mode.")
    # Disable login_required
    flask_cas.login_required = lambda f: f
    # Set up username workaround
    NOAUTH = True

    # If OpenSSL is available, we can use talisman even if running in
    # local debugging mode; otherwise we need to disable talisman.
    try:
        import OpenSSL
    except ModuleNotFound_or_Import_Error:
        USE_TALISMAN = False

    # Config may disable talisman
    if app.config.get('NO_DEBUG_SSL'):
        USE_TALISMAN = False


@app.init
def enable_talisman(app):
    """
    Enable talisman forced-HTTPS and other security headers if
    `flask_talisman` is available and it won't interfere with debugging.
    """
    talisman_enabled = False
    if USE_TALISMAN:
        try:
            import flask_talisman
            # Content-security policy settings
            csp = {
                'default-src': "'self'",
                'script-src': "'self' 'report-sample'",
                'style-src': "'self'",
                'img-src': "'self' data:"
            }
            flask_talisman.Talisman(
                app,
                content_security_policy=csp,
                content_security_policy_nonce_in=[
                    'script-src',
                    'style-src'
                ]
            )
            talisman_enabled = True
        except ModuleNotFound_or_Import_Error:
            print(
                "Warning: module flask_talisman is not available;"
                " security headers will not be set."
            )

    if talisman_enabled:
        print("Talisman is enabled.")
    else:
        print("Talisman is NOT enabled.")
        # Add csp_nonce global dummy since flask_talisman didn't
        app.add_template_global(
            lambda: "-nonce-disabled-",
            name='csp_nonce'
        )


@app.init
def setup_seasurf(app):
    """
    Sets up `flask_seasurf` to combat cross-site request forgery, if
    that module is available.

    Note that `route_deliver` is exempt from CSRF verification.
    """
    global route_deliver
    try:
        import flask_seasurf
        csrf = flask_seasurf.SeaSurf(app) # noqa F841
        route_deliver = csrf.exempt(route_deliver)
    except ModuleNotFound_or_Import_Error:
        print(
            "Warning: module flask_seasurf is not available; CSRF"
            " protection will not be enabled."
        )
        # Add csrf_token global dummy since flask_seasurf isn't available
        app.add_template_global(lambda: "-disabled-", name='csrf_token')


#---------#
# Helpers #
#---------#

def augment_arguments(route_function):
    """
    A decorator that modifies a route function to supply `username`,
    `is_admin`, `masquerade_as`, `effective_user`, and `task_info`
    keyword arguments along with the other arguments the route receives.
    Must be applied before app.route, and the first two parameters to the
    function must be the course and semester.

    Because flask/werkzeug routing requires function signatures to be
    preserved, we do some dirty work with compile and eval... As a
    result, this function can only safely be used to decorate functions
    that don't have any keyword arguments. Furthermore, the 5 augmented
    arguments must be the last 5 arguments that the function accepts.
    """
    def with_extra_arguments(*args, **kwargs):
        """
        A decorated route function which will be supplied with username,
        is_admin, masquerade_as, effective_user, and task_info parameters
        as keyword arguments after other arguments have been supplied.
        """
        # Get username
        if NOAUTH:
            username = "test"
        else:
            username = cas.username

        # Grab course + semester values
        course = kwargs.get('course', args[0] if len(args) > 0 else None)
        semester = kwargs.get(
            'semester',
            args[1 if 'course' not in kwargs else 0]
                if len(args) > 0 else None
        )

        if course is None or semester is None:
            flask.flash(
                (
                    "Error: Unable to get course and/or semester. Course"
                    " is {} and semester is {}."
                ).format(repr(course), repr(semester))
            )
            return error_response(
                course,
                semester,
                username,
                (
                    "Failed to access <code>course</code> and/or"
                    " <code>semester</code> values."
                )
            )

        # Get admin info
        admin_info = storage.get_admin_info(course, semester)
        if admin_info is None:
            flask.flash("Error loading admin info!")
            admin_info = {}

        # Check user privileges
        is_admin, masquerade_as = check_user_privileges(admin_info, username)

        # Effective username
        effective_user = masquerade_as or username

        # Get basic info on all projects/tasks
        task_info = storage.get_task_info(course, semester)
        if task_info is None: # error loading task info
            flask.flash("Error loading task info!")
            return error_response(
                course,
                semester,
                username,
                "Failed to load <code>tasks.json</code>."
            )

        # Set pause time for the task info
        set_pause_time(admin_info, task_info, username, masquerade_as)

        # Update the kwargs
        kwargs["username"] = username
        kwargs["is_admin"] = is_admin
        kwargs["masquerade_as"] = masquerade_as
        kwargs["effective_user"] = effective_user
        kwargs["task_info"] = task_info

        # Call the decorated function w/ the extra parameters we've
        # deduced.
        return route_function(*args, **kwargs)

    # Grab info on original function signature
    fname = route_function.__name__
    nargs = route_function.__code__.co_argcount
    argnames = route_function.__code__.co_varnames[:nargs - 5]

    # Create a function with the same signature:
    code = """\
def {name}({args}):
    return with_extra_arguments({args})
""".format(name=fname, args=', '.join(argnames))
    env = {"with_extra_arguments": with_extra_arguments}
    # 2/3 compatibility attempt...
    if sys.version_info[0] < 3:
        exec(code) in env, env
    else:
        exec(code, env, env) in env, env
    result = env[fname]

    # Preserve docstring
    result.__doc__ = route_function.__doc__

    # Return our synthetic function...
    return result


def goback(course, semester):
    """
    Returns a flask redirect aimed at either the page that the user came
    from, or the dashboard if that information isn't available.
    """
    if flask.request.referrer:
        # If we know where you came from, send you back there
        return flask.redirect(flask.request.referrer)
    else:
        # Otherwise back to the dashboard
        return flask.redirect(
            flask.url_for('route_dash', course=course, semester=semester)
        )


#-----------------#
# Route functions #
#-----------------#

@app.route('/')
def route_index():
    """
    Checks authentication and redirects to login page or to dashboard.
    """
    if NOAUTH or cas.username:
        return flask.redirect(flask.url_for('route_default_dash'))
    else:
        return flask.redirect(flask.url_for('cas.login'))


@app.route('/dashboard')
@flask_cas.login_required
def route_default_dash():
    """
    Redirects to dashboard w/ default class/semester.
    """
    return flask.redirect(
        flask.url_for(
            'route_dash',
            course=app.config.get("DEFAULT_COURSE", "unknown"),
            semester=app.config.get("DEFAULT_SEMESTER", "unknown")
        )
    )


@app.route('/<course>/<semester>/dashboard')
@flask_cas.login_required
@augment_arguments
def route_dash(
    course,
    semester,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Displays dashboard w/ links for submitting each project/task & summary
    information of task grades. Also includes info on submitted
    exercises.
    """

    # Add project status and task feedback summaries to task info
    amend_task_info(course, semester, task_info, effective_user)

    # Get concepts info
    concepts = storage.get_concepts(course, semester)
    if concepts is None:
        flask.flash("Warning: concepts not specified/available.")
        concepts = []

    # Grab latest-outcomes info for ALL exercises
    outcomes = fetch_all_best_outcomes(
        course,
        semester,
        effective_user,
        task_info
    )

    # Amend exercise statuses
    amend_exercises(course, semester, task_info, outcomes, effective_user)

    # Augment the concepts structure to include real object
    # references
    augment_concepts(concepts)

    # Update concepts list with statuses based on exercise outcomes
    # and amended task info.
    set_concept_statuses(concepts, task_info, outcomes)

    # Render dashboard template
    return flask.render_template(
        'dashboard.j2',
        course_name=task_info.get("course_name", course),
        course=course,
        semester=semester,
        username=username,
        is_admin=is_admin,
        masquerade_as=masquerade_as,
        effective_user=effective_user,
        task_info=task_info,
        timeliness_matters=(
            0 < usual_config_value("TIMELINESS_POINTS", task_info, default=0)
        ),
        outcomes=outcomes, # TODO: USE THIS
        concepts=concepts # TODO: USE THIS
    )


@app.route(
    '/<course>/<semester>/feedback/<target_user>/<phase>/<prid>/<taskid>'
)
@flask_cas.login_required
@augment_arguments
def route_feedback(
    course,
    semester,
    target_user,
    phase,
    prid,
    taskid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Displays feedback on a particular task of a particular problem set,
    for either the 'initial' or 'revision' phase.
    """
    if target_user != effective_user and not is_admin:
        return error_response(
            course,
            semester,
            username,
            "You are not allowed to view feedback for {}.".format(target_user)
        )
    elif target_user != effective_user:
        flask.flash("Viewing feedback for {}.".format(target_user))

    # From here on we treat the effective user as the target user
    effective_user = target_user

    # Check roster and flash a warning if we're viewing feedback for a
    # user who is not on the roster...
    try:
        roster = storage.get_roster(course, semester)
    except Exception as e:
        flask.flash(str(e))
        roster = None

    if roster is None:
        flask.flash(
            "Warning: could not fetch roster to check if this user is on"
            " it."
        )
    elif effective_user not in roster:
        flask.flash("Warning: this user is not on the roster!")

    # Get full feedback-ready project and task objects
    pr_and_task = get_feedback_pr_and_task(
        task_info,
        course,
        semester,
        target_user,
        phase,
        prid,
        taskid
    )
    if isinstance(pr_and_task, ValueError):
        flask.flash(str(pr_and_task))
        return goback(course, semester)
    else:
        pr, task = pr_and_task

    if task["eval_status"] not in (
        None,
        "unknown",
        "initial",
        "in_progress",
        "error",
        "expired",
        "completed"
    ):
        msg = "Invalid evaluation status <code>{}</code>.".format(
            task["eval_status"]
        )
        flask.flash(msg)
        return error_response(course, semester, username, msg)

    # Set auto-refresh based on evaluation status
    if task["eval_status"] in ("unknown", "in_progress", "error"):
        refresh = 20
        flask.flash("""\
This page should refresh itself {refresh} seconds after loading
<span
 role="timer"
 aria-live="off"
 class="timer"
 data-time="{refresh}"
>
  {refresh}
</span>.""".format(refresh=refresh))
    else:
        refresh = None

    return flask.render_template(
        'feedback.j2',
        course_name=task_info.get("course_name", course),
        course=course,
        semester=semester,
        username=username,
        is_admin=is_admin,
        masquerade_as=masquerade_as,
        effective_user=effective_user,
        target_user=target_user,
        phase=phase,
        pr=pr,
        task=task,
        task_info=task_info,
        fb_css=potluck.render.get_css(),
        fb_js=potluck.render.get_js(),
        score_basis=usual_config_value(
            "SCORE_BASIS",
            task_info,
            task=taskid,
            default=0
        ),
        support_link=usual_config_value(
            "SUPPORT_LINK",
            task_info,
            task=taskid
        ),
        refresh=refresh
    )


@app.route(
    '/<course>/<semester>/submit/<prid>/<taskid>',
    methods=['POST']
)
@flask_cas.login_required
@augment_arguments
def route_submit(
    course,
    semester,
    prid,
    taskid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Accepts a file submission for a task and initiates an evaluation
    process for that file. Figures out submission phase automatically
    based on task info, and assumes that the submission belongs to the
    authenticated user. However, if the authenticated user is an admin,
    the "phase" and "target_user" form values can override these
    assumptions. Redirects to the feedback page for the submitted task,
    or to the evaluation page if the user is an admin and is not the
    target user.

    Note: there are probably some nasty race conditions if the same user
    submits the same task simultaneously via multiple requests. We simply
    hope that that does not happen.
    """
    try:
        pr = get_pr_obj(task_info, prid)
    except ValueError as e:
        flask.flash(str(e))
        return goback(course, semester)

    try:
        task = get_task_obj(task_info, pr, taskid)
    except ValueError as e:
        flask.flash(str(e))
        return goback(course, semester)

    # Add status & time remaining info to project
    amend_project(course, semester, task_info, pr, effective_user)

    # Check for phase and/or target_user overrides in the form data if
    # the authenticated user is an admin
    target_user = effective_user
    phase = None
    destination_route = 'route_feedback'
    if is_admin:
        target_from_form = flask.request.form.get("target_user")
        if target_from_form not in ("", "auto"):
            target_user = target_from_form
        phase_from_form = flask.request.form.get("phase")
        if phase_from_form != "auto":
            phase = phase_from_form

        # Send admins to 'route_evaluate' instead of 'route_feedback' if
        # the target user is not the same as the actual user, whether
        # because of a masquerade or because of an explicit target user.
        if target_user != username:
            destination_route = 'route_evaluate'

    # Determine the phase from the project state if we need to
    if phase is None:
        pr_state = pr['status']['state']
        if pr_state == "unknown":
            msg = "{} has no deadline.".format(prid)
            flask.flash(msg)
            return error_response(course, semester, username, msg)
        elif pr_state in ("unreleased", "released"):
            phase = "initial"
        elif pr_state in ("under_review", "revisable"):
            phase = "revision"
            #if pr_state == "under_review":
            #    flask.flash(
            #        "You should probably wait until the review period is"
            #      + " over and view feedback on your initial submission"
            #      + " before submitting a revision."
            #    )
        elif pr_state == "final":
            flask.flash(
                "We are no longer accepting new submissions for {}.".format(
                    prid
                )
            )
            phase = "belated"

    # Ensure that there's a file being submitted
    files = flask.request.files
    if ('upload' not in files or files['upload'].filename == ''):
        flask.flash("You must choose a file to submit.")
        return goback(course, semester)
    else:
        uploaded = files['upload']

        # Check for an in-flight grading process for this task
        ts, _, _, status = storage.get_inflight(
            course,
            semester,
            effective_user,
            phase,
            prid,
            taskid
        )

        # If the submission is already being evaluated, or if we couldn't
        # figure out whether that was the case, we can't start another
        # evaluation process!
        if ts == "error":
            flask.flash(
                (
                    "ERROR: Failed to check evaluation status. Try"
                  + " refreshing this page, and if the problem persists,"
                  + " contact {}."
                ).format(
                    usual_config_value(
                        "SUPPORT_LINK",
                        task_info,
                        task=taskid
                    )
                )
            )
            return flask.redirect(
                flask.url_for(
                    destination_route,
                    course=course,
                    semester=semester,
                    target_user=effective_user,
                    phase=phase,
                    prid=prid,
                    taskid=taskid
                )
            )
        elif status in ("initial", "in_progress"):
            flask.flash(
                (
                    "ERROR: Task {taskid} for project {prid} is"
                  + " currently being evaluated. You must wait until"
                  + " that process is complete before uploading a"
                  + "revised submission. This should take no longer"
                  + "than {timeout} seconds."
                ).format(
                    taskid=taskid,
                    prid=prid,
                    timeout=usual_config_value(
                        'FINAL_EVAL_TIMEOUT',
                        task_info,
                        task=taskid
                    )
                )
            )
            return flask.redirect(
                flask.url_for(
                    destination_route,
                    course=course,
                    semester=semester,
                    target_user=effective_user,
                    phase=phase,
                    prid=prid,
                    taskid=taskid
                )
            )
        # else we assume the status is some final status or None meaning
        # this is the first submission

        # Record the time spent value
        if (
            'time_spent' not in flask.request.form
         or flask.request.form["time_spent"] == ""
        ):
            flask.flash(
                "You did not give us an estimate of how much time this"
              + " task took you. Please re-submit and enter a time spent"
              + " value so that we can help advise future students about"
              + " how long this task will take them."
            )
            time_spent = ""
        else:
            time_spent = flask.request.form["time_spent"]

        storage.record_time_spent(
            course,
            semester,
            target_user,
            phase,
            prid,
            taskid,
            time_spent
        )

        # Save the file with the correct filename, ignoring the name that
        # the user uploaded.
        target = get_submission_filename(
            course,
            semester,
            task_info,
            target_user,
            phase,
            prid,
            taskid
        )
        destdir, _ = os.path.split(target)
        storage.ensure_directory(destdir)
        storage.make_way_for(target)
        uploaded.save(target)
        # TODO: Flash categories
        if phase == "belated":
            flask.flash(
                (
                    "Uploaded LATE '{filename}' for {prid} {taskid}."
                ).format(
                    filename=uploaded.filename,
                    prid=prid,
                    taskid=taskid
                )
            )
        else:
            flask.flash(
                (
                    "Successfully uploaded {phase} submission"
                  + " '{filename}' for {prid} {taskid}."
                ).format(
                    phase=phase,
                    filename=uploaded.filename,
                    prid=prid,
                    taskid=taskid
                )
            )

        # Flash a warning if the uploaded filename seems wrong
        if uploaded.filename != task["target"]:
            flask.flash(
                (
                    "Warning: you uploaded a file named '{filename}',"
                  + " but {taskid} in {prid} requires a file named"
                  + " '{reqname}'. Are you sure you uploaded the"
                  + " correct file?"
                ).format(
                    filename=uploaded.filename,
                    prid=prid,
                    taskid=taskid,
                    reqname=task["target"]
                )
            )

        # Log setup
        ts, logfile, reportfile, _ = storage.put_inflight(
            course,
            semester,
            target_user,
            phase,
            prid,
            taskid
        )

        if ts == "error":
            flask.flash(
                (
                    "ERROR: Failed to check evaluation status. Try"
                  + " refreshing this page, and if the problem persists,"
                  + " contact {}."
                ).format(
                    usual_config_value(
                        "SUPPORT_LINK",
                        task_info,
                        task=taskid
                    )
                )
            )
            return flask.redirect(
                flask.url_for(
                    destination_route,
                    course=course,
                    semester=semester,
                    target_user=target_user,
                    phase=phase,
                    prid=prid,
                    taskid=taskid
                )
            )
        elif ts is None: # another grading process is already in-flight
            flask.flash(
                (
                    "ERROR: Task {taskid} for project {prid} is"
                  + "currently being evaluated. You must wait until"
                  + "that process is complete before uploading another"
                  + "submission. This should take no longer than"
                  + "{timeout} seconds."
                ).format(
                    prid=prid,
                    taskid=taskid,
                    timeout=usual_config_value(
                        'FINAL_EVAL_TIMEOUT',
                        task_info,
                        task=taskid
                    )
                )
            )
            return flask.redirect(
                flask.url_for(
                    destination_route,
                    course=course,
                    semester=semester,
                    target_user=target_user,
                    phase=phase,
                    prid=prid,
                    taskid=taskid
                )
            )

        # Start the evaluation process (we don't wait for it)
        launch_potluck(
            course,
            semester,
            target_user,
            taskid,
            target,
            logfile,
            reportfile
        )

    return flask.redirect(
        flask.url_for(
            destination_route,
            course=course,
            semester=semester,
            target_user=target_user,
            phase=phase,
            prid=prid,
            taskid=taskid
        )
    )


def which_exe(target, cwd='.'):
    """
    shutil.which 2/3 shim. Prepends cwd to current PATH.
    """
    if sys.version_info[0] < 3:
        finder = subprocess.Popen(
            [ 'which', target ],
            cwd=cwd,
            stdout=subprocess.PIPE
        )
        out, err = finder.communicate()
        return out.strip()
    else:
        return shutil.which(
            "potluck_eval",
            path=cwd + ':' + os.getenv("PATH")
        )


def launch_potluck(
    course,
    semester,
    username,
    taskid,
    target_file,
    logfile,
    reportfile,
    wait=False
):
    """
    Launches the evaluation process. By default this is fire-and-forget;
    we'll look for the output file to determine whether it's finished or
    not. However, by passing wait=True you can have the function wait for
    the process to terminate before returning.
    """
    eval_dir = storage.evaluation_directory(course, semester)

    task_info = storage.get_task_info(course, semester)

    pev_python = usual_config_value(
        "POTLUCK_EVAL_PYTHON",
        task_info,
        task=taskid,
        default=None
    )
    if pev_python is None:
        python = []
    else:
        python = [ pev_python ]

    pev_script = usual_config_value(
        "POTLUCK_EVAL_SCRIPT",
        task_info,
        task=taskid,
        default=None
    )
    if pev_script is None:
        potluck_exe = which_exe("potluck_eval", eval_dir)
    else:
        potluck_exe = os.path.join(os.getcwd(), pev_script)

    potluck_args = [
        "--task", taskid,
        "--user", username,
        "--target", os.path.abspath(target_file),
        "--outfile", os.path.abspath(reportfile),
        "--clean",
    ]

    pev_import_from = usual_config_value(
        "POTLUCK_EVAL_IMPORT_FROM",
        task_info,
        task=taskid,
        default=None
    )
    if pev_import_from is not None:
        import_dir = os.path.join(os.getcwd(), pev_import_from)
        potluck_args.extend(["--import-from", import_dir])
    with open(logfile, 'wb') as log:
        if usual_config_value(
            "USE_XVFB",
            task_info,
            task=taskid,
            default=False
        ):
            # Virtualise frame buffer for programs with graphics, so
            # they don't need to create Xwindow windows
            # '--auto-servernum', # create a new server??
            # '--auto-display',
            # [2019/02/08] Peter: try this instead per comment in -h?
            xvfb_err_log = os.path.splitext(logfile)[0] + ".xvfb_errors.log"
            full_args = (
                [
                    'xvfb-run',
                    '-d',
                    # [2019/02/11] Lyn: --auto-display doesn't work but -d
                    # does (go figure, since they're supposed to be
                    # synonyms!)
                    '-e', # --error-file doesn't work
                    xvfb_err_log,
                    '--server-args',
                    usual_config_value(
                        "XVFB_SERVER_ARGS",
                        task_info,
                        task=taskid,
                        default='-screen 0'
                    ), # screen properties
                    '--',
                ] + python + [
                    potluck_exe,
                ]
              + potluck_args
            )
        else:
            # Raw potluck launch without XVFB
            full_args = python + [ potluck_exe ] + potluck_args

        log.write(
            ("Full args: " + repr(full_args) + '\n').encode("utf-8")
        )
        log.flush()

        p = subprocess.Popen(
            full_args,
            cwd=eval_dir,
            stdout=log,
            stderr=log,
        )

        if wait:
            p.wait()


@app.route('/<course>/<semester>/extension/<prid>', methods=['GET'])
@flask_cas.login_required
@augment_arguments
def route_extension(
    course,
    semester,
    prid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Requests (and automatically grants) the default extension on the
    given problem set. The extension is applied to the initial phase
    only. For now, nonstandard extensions and revision extensions must be
    applied by hand-editing JSON files in the `extensions/` directory.
    """
    try:
        pr = get_pr_obj(task_info, prid)
    except ValueError as e:
        flask.flash(str(e))
        return goback(course, semester)

    # Add status & time remaining info to project
    amend_project(course, semester, task_info, pr, effective_user)
    # TODO: triple-check the possibility of requesting an extension
    # during the period an extension would grant you but after the
    # initial deadline?

    # Grant the extension
    if (
        pr["status"]["state"] in ("unreleased", "released")
    and pr["status"]["initial_extension"] == 0
    ):
        succeeded = storage.set_extension(
            course,
            semester,
            effective_user,
            prid,
            "initial"
        )
        if succeeded:
            flask.flash("Extension granted for {}.".format(prid))
        else:
            flask.flash("Failed to grant extension for {}.".format(prid))
    elif pr["status"]["state"] not in ("unreleased", "released"):
        flask.flash(
            (
                "It is too late to request an extension for {}. You must"
                " request extensions before the deadline for each"
                " project."
            ).format(prid)
        )
    elif pr["status"]["initial_extension"] != 0:
        flask.flash(
            "You have already been granted an extension on {}.".format(prid)
        )
    else:
        flask.flash(
            "You cannot take an extension on {}.".format(prid)
        )

    # Send them back to the dashboard or wherever they came from
    return goback(course, semester)


@app.route(
    '/<course>/<semester>/set_extensions/<target_user>/<prid>',
    methods=['POST']
)
@flask_cas.login_required
@augment_arguments
def route_set_extensions(
    course,
    semester,
    target_user,
    prid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Form target for editing extensions for a particular user/project.
    Only admins can use this route. Can be used to set custom extension
    values for both initial and revised deadlines.

    Note that for now, we're also using it for exercise extensions.
    TODO: Fix that, since it means that if an exercise has the same ID
    as a project, their extensions will overwrite each other!!!
    """
    if not is_admin:
        flask.flash("Only admins can grant extensions.")
        return goback(course, semester)

    # Get initial/revision extension values from submitted form values
    try:
        initial = int(flask.request.form["initial"])
    except Exception:
        initial = None

    try:
        revision = int(flask.request.form["revision"])
    except Exception:
        revision = None

    # At least one or the other needs to be valid
    if initial is None and revision is None:
        flask.flash(
            (
                "To set extensions, you must specify either an initial"
                " or a revision value, and both values must be integers."
            )
        )
        return goback(course, semester)

    # Grant the extension(s)
    if initial is not None:
        # TODO: Use only_from here to help prevent race conditions on
        # loading the HTML page that displays the extension values
        succeeded = storage.set_extension(
            course,
            semester,
            target_user,
            prid,
            "initial",
            initial
        )
        if succeeded:
            flask.flash(
                "Set {}h initial extension for {} on {}.".format(
                    initial,
                    target_user,
                    prid
                )
            )
        else:
            flask.flash(
                "Failed to grant initial extension for {} on {} (try again?)."
                .format(target_user, prid)
            )

    if revision is not None:
        succeeded = storage.set_extension(
            course,
            semester,
            target_user,
            prid,
            "revision",
            revision
        )
        if succeeded:
            flask.flash(
                "Set {}h revision extension for {} on {}.".format(
                    revision,
                    target_user,
                    prid
                )
            )
        else:
            flask.flash(
                "Failed to grant revision extension for {} on {} (try again?)."
                .format(target_user, prid)
            )

    # Send them back to the dashboard or wherever they came from
    return goback(course, semester)


@app.route(
    '/<course>/<semester>/manage_extensions/<target_user>',
    methods=['GET']
)
@flask_cas.login_required
@augment_arguments
def route_manage_extensions(
    course,
    semester,
    target_user,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Admin-only route that displays a list of forms for each project
    showing current extension values and allowing the user to edit them
    and press a button to update them.
    """
    if not is_admin:
        flask.flash("Only admins can grant extensions.")
        return goback(course, semester)

    # Get extensions info for the target user for all projects
    amend_task_info(course, semester, task_info, target_user)

    # Amend exercise statuses (using blank outcomes since we're only
    # using the extension info)
    amend_exercises(course, semester, task_info, {}, target_user)

    return flask.render_template(
        'extension_manager.j2',
        course_name=task_info.get("course_name", course),
        course=course,
        semester=semester,
        username=username,
        is_admin=is_admin,
        masquerade_as=masquerade_as,
        task_info=task_info,
        target_user=target_user
    )


@app.route(
    '/<course>/<semester>/set_eval/<target_user>/<phase>/<prid>/<taskid>',
    methods=['POST']
)
@flask_cas.login_required
@augment_arguments
def route_set_evaluation(
    course,
    semester,
    target_user,
    phase,
    prid,
    taskid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Form target for editing custom evaluation info for a particular
    user/project. Only admins can use this route. Can be used to set
    custom notes and/or a grade override for a particular
    user/phase/project/task.
    """
    if not is_admin:
        # TODO: Grader role!
        flask.flash("Only admins can edit evaluations.")
        return goback(course, semester)

    # Get notes & overrides from form values
    try:
        notes = flask.request.form["notes_md"]
    except Exception:
        notes = None

    try:
        override = flask.request.form["override"]
    except Exception:
        override = None

    # Attempt to convert to a number
    if override is not None:
        try:
            override = float(override)
        except Exception:
            pass

    try:
        timeliness = flask.request.form["timeliness_override"]
    except Exception:
        timeliness = None

    # Attempt to convert to a number
    if timeliness is not None:
        try:
            timeliness = float(timeliness)
        except Exception:
            pass

    # At least one of them needs to be valid
    if notes is None and override is None and timeliness is None:
        flask.flash(
            "To set an evaluation, you must specify at least one of: a"
            " notes string, a grade override, or a timeliness override."
        )
        return goback(course, semester)

    # Turn Nones into empty strings:
    if notes is None:
        notes = ''

    if override is None:
        override = ''

    if timeliness is None:
        timeliness = ''

    # TODO: Create and use an only_from mechanism here to help
    # prevent race conditions on loading the HTML page that displays
    # the old evaluation values?
    succeeded = storage.set_evaluation(
        course,
        semester,
        target_user,
        phase,
        prid,
        taskid,
        notes,
        override,
        timeliness
    )
    if succeeded:
        flask.flash(
            "Updated evaluation for {} on {} {} {} submission.".format(
                target_user,
                prid,
                taskid,
                phase
            )
        )
    else:
        flask.flash(
            (
                "Failed to update evaluation for {} on {} {} {}"
                " submission."
            ).format(
                target_user,
                prid,
                taskid,
                phase
            )
        )

    # Send them to the evaluation-editing page
    return flask.redirect(
        flask.url_for(
            'route_evaluate',
            course=course,
            semester=semester,
            target_user=target_user,
            phase=phase,
            prid=prid,
            taskid=taskid
        )
    )


@app.route(
    '/<course>/<semester>/evaluate/<target_user>/<phase>/<prid>/<taskid>',
    methods=['GET']
)
@flask_cas.login_required
@augment_arguments
def route_evaluate(
    course,
    semester,
    target_user,
    phase,
    prid,
    taskid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Displays student feedback and also includes a form at the top for
    adding a custom note and/or overriding the grade.
    """
    if not is_admin:
        # TODO: Grader role!
        flask.flash("Only admins can evaluate submissions.")
        return goback(course, semester)

    # Check roster and flash a warning if we're viewing feedback for a
    # user who is not on the roster...
    try:
        roster = storage.get_roster(course, semester)
    except Exception as e:
        flask.flash(str(e))
        roster = None

    if roster is None:
        flask.flash(
            "Warning: could not fetch roster to check if this user is on"
            " it."
        )
    elif target_user not in roster:
        flask.flash("Warning: this user is not on the roster!")

    # Get full feedback info
    pr_and_task = get_feedback_pr_and_task(
        task_info,
        course,
        semester,
        target_user,
        phase,
        prid,
        taskid
    )
    if isinstance(pr_and_task, ValueError):
        flask.flash(str(pr_and_task))
        return goback(course, semester)
    else:
        pr, task = pr_and_task

    return flask.render_template(
        'evaluate.j2',
        course_name=task_info.get("course_name", course),
        course=course,
        semester=semester,
        username=username,
        is_admin=is_admin,
        masquerade_as=masquerade_as,
        effective_user=effective_user,
        target_user=target_user,
        phase=phase,
        pr=pr,
        task=task,
        task_info=task_info,
        fb_css=potluck.render.get_css(),
        fb_js=potluck.render.get_js(),
        score_basis=usual_config_value(
            "SCORE_BASIS",
            task_info,
            task=taskid,
            default=0
        ),
        timeliness_points=usual_config_value(
            "TIMELINESS_POINTS",
            task_info,
            task=taskid,
            default=0
        ),
        support_link=usual_config_value(
            "SUPPORT_LINK",
            task_info,
            task=taskid
        )
    )


@app.route('/<course>/<semester>/solution/<prid>/<taskid>', methods=['GET'])
@flask_cas.login_required
@augment_arguments
def route_solution(
    course,
    semester,
    prid,
    taskid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Visible only once a task's status is final, accounting for all
    extensions, and if the active user has an evaluated submission for
    the task, or another task in the same pool (or if they're an admin).
    Shows the solution code for a particular task, including a formatted
    version and a link to download the .py file.
    """
    try:
        pr = get_pr_obj(task_info, prid)
    except ValueError as e:
        flask.flash("ValueError: " + str(e))
        return goback(course, semester)

    # Add status & time remaining info to project and objects
    amend_project(course, semester, task_info, pr, effective_user)

    # Grab task object for this task
    try:
        task = get_task_obj(task_info, pr, taskid)
    except ValueError as e:
        flask.flash("ValueError: " + str(e))
        return goback(course, semester)

    # Find tasks in the same pool as this one:
    if "pool" in task:
        tasks_in_pool = [
            tentry["id"]
            for tentry in pr["tasks"]
            if tentry.get("pool") == task["pool"]
        ]
    else:
        tasks_in_pool = [ task["id"] ]

    # Grab task objects for each task in our pool and amend them:
    submitted_to_pool = False
    for taskid in tasks_in_pool:
        try:
            tobj = get_task_obj(task_info, pr, taskid)
        except ValueError as e:
            flask.flash("ValueError: " + str(e))
            return goback(course, semester)

        initial = tobj
        revised = copy.deepcopy(tobj)

        amend_task(
            course,
            semester,
            task_info,
            prid,
            initial,
            effective_user,
            "initial"
        )
        if initial.get("submitted"):
            submitted_to_pool = True
            break

        amend_task(
            course,
            semester,
            task_info,
            prid,
            revised,
            effective_user,
            "revision"
        )
        if revised.get("submitted"):
            submitted_to_pool = True
            break

    # Check roster so that only students on the roster can view solutions
    # (we don't want future-semester students viewing previous-semester
    # solutions!).
    try:
        roster = storage.get_roster(course, semester)
    except Exception as e:
        flask.flash(str(e))
        roster = None

    if roster is None:
        msg = "Failed to load <code>roster.csv</code>."
        flask.flash(msg)
        return error_response(course, semester, username, msg)

    if pr["status"]["state"] != "final":
        if is_admin:
            flask.flash(
                "Viewing solution code as admin; solution is not"
              + " visible to students until revision period is over."
            )
        else:
            flask.flash(
                (
                    "You cannot view the solutions for {project} {task}"
                  + " until the revision period is over."
                ).format(project=prid, task=taskid)
            )
            return goback(course, semester)

    elif effective_user not in roster: # not on the roster
        if is_admin:
            flask.flash(
                (
                    "Viewing solution code as admin; solution is not"
                  + " visible to user {} as they are not on the roster"
                  + " for this course/semester."
                ).format(effective_user)
            )
        else:
            flask.flash(
                (
                    "You cannot view solutions for {course} {semester}"
                  + " because you are not on the roster for that class."
                ).format(course=course, semester=semester)
            )
            return goback(course, semester)

    elif not (
        usual_config_value(
            "DISPLAY_UNSUBMITTED_SOLUTIONS",
            task_info,
            task=taskid,
            default=False
        )
     or submitted_to_pool
    ):
        # This user hasn't submitted this task, so we'd like to make it
        # possible for them to get an extension later without worrying about
        # whether they've accessed solution code in the mean time.
        if is_admin:
            flask.flash(
                (
                    "Viewing solution code as admin; solution is not"
                  + " visible to user {} as they don't have a submission"
                  + " for this task or another task in this pool."
                ).format(effective_user)
            )
        else:
            flask.flash(
                (
                    "You cannot view the solution for {} {} becuase you"
                    " haven't submitted that task or any task in the"
                    " same pool."
                ).format(prid, taskid)
            )
            return goback(course, semester)

    # At this point, we've verified it's okay to display the solution:
    # the project is finalized, and the user is an admin or at least on
    # the roster for this particular course/semester, and the user has a
    # submission for this task, or at least to another task in the same
    # pool.

    # We'd like the feedback CSS & JS because we're going to render code
    # as HTML using potluck.
    fb_css = potluck.render.get_css()
    fb_js = potluck.render.get_js()

    # TODO: This feels a bit hardcoded... can we do better?
    # TODO: Multi-file stuff!
    soln_filename = os.path.join(
        storage.evaluation_directory(course, semester),
        "specs",
        task["id"],
        "soln",
        task["target"]
    )

    with open(soln_filename, 'r') as fin:
        soln_code = fin.read()

    soln_code_html = potluck.render.render_code(
        taskid,
        soln_filename,
        soln_code
    )

    return flask.render_template(
        'solution.j2',
        course_name=task_info.get("course_name", course),
        course=course,
        semester=semester,
        username=username,
        is_admin=is_admin,
        masquerade_as=masquerade_as,
        effective_user=effective_user,
        pr=pr,
        task=task,
        task_info=task_info,
        soln_code=soln_code,
        rendered_soln=soln_code_html,
        fb_css=fb_css,
        fb_js=fb_js,
        support_link=usual_config_value(
            "SUPPORT_LINK",
            task_info,
            task=taskid
        )
    )


@app.route(
    '/<course>/<semester>/starter/<taskid>.zip',
    methods=['GET']
)
def route_starter_zip(course, semester, taskid):
    """
    For each task, serves a cached copy of a zip file that includes all
    files in that task's starter directory (+ subdirectories, including
    ones that are symlinks). If the cached zip does not exist, or if it's
    older than any of the files it needs to include, it will be
    generated. Note that login is NOT required for this route.

    `__pycache__` directories and any files they contain will not be
    included in the zip file. There is a configurable maximum number of
    files, to help detect issues caused by cyclic symbolic links; set
    `MAX_STARTER_FILES` to modify this from the default of 100000 (which
    is probably already enough that unzipping would be problematic?).

    Raises an `OSError` if too many files are present.
    """
    # TODO: This feels a bit hardcoded... can we do better?
    # Compute filenames and directories
    starter_dir = os.path.join(
        storage.evaluation_directory(course, semester),
        "specs",
        taskid,
        "starter"
    )

    # We 'detect' symlink loops without doing something like stating each
    # directory along the way by using a max # of files (the zip would
    # become unmanageable at some point anyways
    max_starter_files = usual_config_value(
        "MAX_STARTER_FILES",
        storage.get_task_info(course, semester),
        task=taskid,
        default=100000
    )

    # Note: a symlink-to-an-ancestor will cause an infinite loop here.
    starter_files = []
    for dirpath, dirnames, filenames in os.walk(
        starter_dir,
        followlinks=True
    ):
        # Don't include __pycache__ directories
        if '__pycache__' in dirnames:
            dirnames.remove('__pycache__')

        for filename in filenames:
            starter_files.append(
                os.path.relpath(os.path.join(dirpath, filename), starter_dir)
            )
            if len(starter_files) > max_starter_files:
                raise OSError(
                    (
                        "We've found more than {max_starter_files}"
                        " starter files; it's likely that you have a"
                        " symbolic link loop. Aborting..."
                    ).format(max_starter_files=max_starter_files)
                )

    starter_zip = os.path.join(
        storage.evaluation_directory(course, semester),
        "specs",
        taskid,
        taskid + ".zip"
    )

    # Compute most-recent-modification time for any starter file
    updated_at = None
    for file in starter_files:
        full_path = os.path.join(starter_dir, file)
        mtime = os.stat(full_path).st_mtime
        if updated_at is None or updated_at < mtime:
            updated_at = mtime

    # Check for freshness
    if (
        not os.path.exists(starter_zip)
     or os.stat(starter_zip).st_mtime < updated_at
    ):
        # Zip up all the starter files, erasing and overwriting the old
        # zip file if it was there before
        with zipfile.ZipFile(starter_zip, 'w', zipfile.ZIP_DEFLATED) as zout:
            for file in starter_files:
                full_path = os.path.join(starter_dir, file)
                zout.write(full_path, taskid + '/' + file)

    with open(starter_zip, 'rb') as fin:
        raw_bytes = fin.read()

    return flask.Response(raw_bytes, mimetype='application/zip')


@app.route('/<course>/<semester>/gradesheet', methods=['GET'])
@flask_cas.login_required
@augment_arguments
def route_full_gradesheet(
    course,
    semester,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Visible by admins only, this route displays an overview of the status
    of every student on the roster, for ALL exercises and projects.
    """
    if not is_admin:
        flask.flash("You do not have permission to view gradesheets.")
        return goback(course, semester)

    # Get the roster
    try:
        roster = storage.get_roster(course, semester)
    except Exception as e:
        flask.flash(str(e))
        roster = None

    if roster is None:
        msg = "Failed to load <code>roster.csv</code>."
        flask.flash(msg)
        return error_response(course, semester, username, msg)

    # Assemble one gradesheet row per student
    rows = []
    for stid in sorted(
        roster,
        key=lambda stid: (
            roster[stid]["course_section"],
            roster[stid]["sortname"]
        )
    ):
        if roster[stid]["course_section"] == "__hide__":
            continue

        row = roster[stid]
        row_info = copy.deepcopy(task_info)
        row["task_info"] = row_info

        # Get info for each exercise group and project
        grade_items = []

        # Grab latest-outcomes info for ALL exercises
        ex_outcomes = fetch_all_best_outcomes(
            course,
            semester,
            row["username"],
            row_info
        )
        # Compute grades for each group
        amend_exercises(
            course,
            semester,
            row_info,
            ex_outcomes,
            row["username"]
        )
        # Exercise groups
        for ex in row_info.get("exercises", []):
            if ex.get("hide"):
                continue
            item = copy.deepcopy(ex)
            item["name"] = ex["group"]
            item["grade"] = ex_combined_grade(ex, row_info)
            item["deadline"] = ex.get("timely")
            item["url"] = flask.url_for(
                'route_ex_gradesheet',
                course=course,
                semester=semester,
                group=ex["group"]
            )
            grade_items.append(item)

        # Amend info for all projects + tasks, and pick up grade items
        for pr in row_info.get("projects", row_info.get("psets", [])):
            if pr.get("hide"):
                continue
            amend_project_and_tasks(
                course,
                semester,
                row_info,
                pr,
                row["username"]
            )

            item = copy.deepcopy(pr)
            item["name"] = pr["id"]
            item["grade"] = project_combined_grade(pr, row_info)
            item["deadline"] = pr.get("due")
            item["url"] = flask.url_for(
                "route_gradesheet",
                course=course,
                semester=semester,
                prid=pr["id"]
            )
            grade_items.append(item)

            tasks = pr.get("tasks", [])

            if len(tasks) > 1:
                item["parts"] = []

                for taskobj in tasks:
                    part = copy.deepcopy(taskobj)
                    part["name"] = taskobj["id"]
                    part["grade"] = task_combined_grade(taskobj, row_info)
                    part["url"] = flask.url_for(
                        "route_gradesheet",
                        course=course,
                        semester=semester,
                        prid=pr["id"]
                    )
                    item["parts"].append(part)

        # Sort items by deadlines and compute combined percentage
        grade_items.sort(key=lambda x: (x["deadline"], x["name"]))
        combined_num = 0
        combined_denom = 0
        for item in grade_items:
            due_at = potluck.time_utils.task_time__time(
                row_info,
                item["deadline"],
                default_time_of_day=row_info.get(
                    "default_due_time_of_day",
                    "23:59"
                )
            )
            now = potluck.time_utils.now()
            if due_at < now:
                combined_num += item["grade"]
                combined_denom += fallback_config_value(
                    "SCORE_BASIS",
                    item,
                    row_info,
                    app.config,
                    DEFAULT_CONFIG
                )

        # Add grade items & combined percentage to row
        if combined_denom > 0:
            row["combined_pct"] = round(
                100 * (combined_num / combined_denom),
                1
            )
        else:
            row["combined_pct"] = None
        row["grade_items"] = grade_items

        rows.append(row)

    # Get the student info
    try:
        student_info = storage.get_student_info(course, semester)
    except Exception as e:
        flask.flash(str(e))
        student_info = None

    return flask.render_template(
        'full_gradesheet.j2',
        course_name=task_info.get("course_name", course),
        course=course,
        semester=semester,
        username=username,
        is_admin=is_admin,
        masquerade_as=masquerade_as,
        task_info=task_info,
        grade_items=rows[0]["grade_items"], # arbitrary for header
        roster=rows,
        student_info=student_info
    )


@app.route('/<course>/<semester>/gradesheet/<prid>', methods=['GET'])
@flask_cas.login_required
@augment_arguments
def route_gradesheet(
    course,
    semester,
    prid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Visible by admins only, this route displays an overview of the status
    of every student on the roster, with links to the feedback views for
    each student/project/phase/task.
    """
    if not is_admin:
        flask.flash("You do not have permission to view gradesheets.")
        return goback(course, semester)

    # Create base task info from logged-in user's perspective
    base_task_info = copy.deepcopy(task_info)
    amend_task_info(course, semester, base_task_info, username)

    try:
        pr = get_pr_obj(base_task_info, prid)
    except ValueError as e:
        flask.flash(str(e))
        return goback(course, semester)

    # Get the roster
    try:
        roster = storage.get_roster(course, semester)
    except Exception as e:
        flask.flash(str(e))
        roster = None

    if roster is None:
        msg = "Failed to load <code>roster.csv</code>."
        flask.flash(msg)
        return error_response(course, semester, username, msg)

    initial_task_times = {}
    revision_task_times = {}
    rows = []
    for stid in sorted(
        roster,
        key=lambda stid: (
            roster[stid]["course_section"],
            roster[stid]["sortname"]
        )
    ):
        if roster[stid]["course_section"] == "__hide__":
            continue
        row = roster[stid]
        row_info = copy.deepcopy(task_info)
        row["task_info"] = row_info
        probj = get_pr_obj(row_info, prid)
        row["this_project"] = probj

        amend_project_and_tasks(
            course,
            semester,
            row_info,
            probj,
            row["username"]
        )

        probj["total_time"] = 0

        for taskobj in probj["tasks"]:
            taskid = taskobj["id"]
            time_spent = taskobj["time_spent"]
            if time_spent is not None:
                time_val = time_spent["time_spent"]
                if taskid not in initial_task_times:
                    initial_task_times[taskid] = {}

                if isinstance(time_val, (float, int)):
                    initial_task_times[taskid][row["username"]] = time_val
                    taskobj["initial_time_val"] = time_val
                    if isinstance(probj["total_time"], (int, float)):
                        probj["total_time"] += time_val
                elif isinstance(time_val, str) and time_val != "":
                    taskobj["initial_time_val"] = time_val
                    probj["total_time"] = "?"
                else: # empty string or None or the like
                    taskobj["initial_time_val"] = "?"
            else:
                taskobj["initial_time_val"] = 0

            rev_time_spent = taskobj.get("revision", {}).get("time_spent")
            if rev_time_spent is not None:
                rev_time_val = rev_time_spent["time_spent"]
                if taskid not in revision_task_times:
                    revision_task_times[taskid] = {}

                if isinstance(rev_time_val, (float, int)):
                    revision_task_times[taskid][row["username"]] = rev_time_val
                    taskobj["revision_time_val"] = rev_time_val
                    if isinstance(probj["total_time"], (int, float)):
                        probj["total_time"] += rev_time_val
                    if isinstance(taskobj["initial_time_val"], (int, float)):
                        taskobj["combined_time_val"] = (
                            taskobj["initial_time_val"]
                          + rev_time_val
                        )
                    elif ( # initial was a non-empty string
                        isinstance(taskobj["initial_time_val"], str)
                    and taskobj["initial_time_val"] not in ("", "?")
                    ):
                        taskobj["combined_time_val"] = "?"
                    else: # empty string or None or the like
                        taskobj["combined_time_val"] = rev_time_val

                elif isinstance(rev_time_val, str) and rev_time_val != "":
                    taskobj["revision_time_val"] = rev_time_val
                    probj["total_time"] = "?"
                    taskobj["combined_time_val"] = "?"

                else: # empty string or None or the like
                    taskobj["revision_time_val"] = "?"
                    taskobj["combined_time_val"] = taskobj["initial_time_val"]

            else: # no rev time spent
                taskobj["revision_time_val"] = "?"
                taskobj["combined_time_val"] = taskobj["initial_time_val"]

        rows.append(row)

    aggregate_times = {
        phase: {
            "average": { "project": 0 },
            "median": { "project": 0 },
            "75th": { "project": 0 },
        }
        for phase in ("initial", "revision")
    }
    aggregate_times["all"] = {}
    for phase, times_group in [
        ("initial", initial_task_times),
        ("revision", revision_task_times)
    ]:
        for taskid in times_group:
            times = list(times_group[taskid].values())
            if len(times) == 0:
                avg = None
                med = None
                qrt = None
            elif len(times) == 1:
                avg = times[0]
                med = times[0]
                qrt = times[0]
            else:
                avg = sum(times) / len(times)
                med = percentile(times, 50)
                qrt = percentile(times, 75)

            aggregate_times[phase]["average"][taskid] = avg
            aggregate_times[phase]["median"][taskid] = med
            aggregate_times[phase]["75th"][taskid] = qrt

            if avg is not None:
                aggregate_times[phase]["average"]["project"] += avg
                aggregate_times[phase]["median"]["project"] += med
                aggregate_times[phase]["75th"]["project"] += qrt

    # Compute total times taking zero-revision-times into account
    total_timespent_values = []
    for student in [row["username"] for row in roster.values()]:
        total_timespent = 0
        for taskobj in probj["tasks"]:
            taskid = taskobj["id"]
            this_task_initial_times = initial_task_times.get(taskid, {})
            this_task_revision_times = revision_task_times.get(taskid, {})
            if student in this_task_initial_times:
                total_timespent += this_task_initial_times[student]
            if student in this_task_revision_times:
                total_timespent += this_task_revision_times[student]
        if total_timespent > 0:
            total_timespent_values.append(total_timespent)

    if len(total_timespent_values) == 0:
        avg = 0
        med = 0
        qrt = 0
    elif len(total_timespent_values) == 1:
        avg = total_timespent_values[0]
        med = total_timespent_values[0]
        qrt = total_timespent_values[0]
    else:
        avg = sum(total_timespent_values) / len(total_timespent_values)
        med = percentile(total_timespent_values, 50)
        qrt = percentile(total_timespent_values, 75)

    aggregate_times["all"]["average"] = avg
    aggregate_times["all"]["median"] = med
    aggregate_times["all"]["75th"] = qrt

    # Get the student info
    try:
        student_info = storage.get_student_info(course, semester)
    except Exception as e:
        flask.flash(str(e))
        student_info = None

    return flask.render_template(
        'gradesheet.j2',
        course_name=task_info.get("course_name", course),
        course=course,
        semester=semester,
        username=username,
        is_admin=is_admin,
        masquerade_as=masquerade_as,
        task_info=task_info,
        pr=pr,
        roster=rows,
        student_info=student_info,
        aggregate_times=aggregate_times
    )


@app.route('/<course>/<semester>/deliver', methods=['GET', 'POST'])
def route_deliver(course, semester):
    """
    This route is accessible by anyone without login, because it is
    going to be posted to from Python scripts (see the `potluckDelivery`
    module). We will only accept submissions from users on the roster
    for the specified course/semester, although because there's no
    verification of user IDs, anyone could be sending submissions (TODO:
    Fix that using token-based verification!). Also, submissions may
    include multiple authors (e.g. when pair programming).

    Submitted form data should have the following slots, with all
    strings encoded using utf-8:

    - 'exercise': The ID of the exercise being submitted.
    - 'authors': A JSON-encoded list of usernames that the submission
        should be assigned to.
    - 'outcomes': A JSON-encoded list of `optimism` outcome-triples,
        each containing a boolean indicating success/failure, followed
        by a tag string indicating the file + line number of the check
        and a second string with the message describing the outcome of
        the check.
    - 'code': A JSON-encoded list of 2-element lists, each of which has
        a filename (or other code-source-identifying-string) and a code
        block (as a string).

    If some of the data isn't in the formats specified above, a 400 error
    will be returned with a string describing what's wrong.
    """
    # The potluckDelivery script prints the delivery URL, which may be
    # styled as a link. So we redirect anyone accessing this route with
    # a GET method to the dashboard.
    if flask.request.method == "GET":
        return flask.redirect(
            flask.url_for('route_dash', course=course, semester=semester)
        )

    # Process POST info...
    form = flask.request.form

    # Get exercise ID
    exercise = form.get("exercise", "")
    if exercise == "":
        return ("Delivery did not specify an exercise.", 400)

    # Get authors list, decode the JSON, and ensure it's a list of
    # strings.
    authorsString = form.get("authors", "")
    if authorsString == "":
        return ("Delivery did not specify authors.", 400)

    try:
        authors = json.loads(authorsString)
    except Exception:
        return ("Specified authors list was not valid JSON.", 400)

    if (
        not isinstance(authors, list)
     or any(not isinstance(author, anystr) for author in authors)
    ):
        return ("Specified authors list was not a list of strings.", 400)

    # Get outcomes list, decode the JSON, and ensure it's a list of
    # 3-element lists each containing a boolean and two strings.
    # An empty list of outcomes is not allowed.
    outcomesString = form.get("outcomes", "")
    if outcomesString == "":
        return ("Delivery did not specify any outcomes.", 400)

    try:
        outcomes = json.loads(outcomesString)
    except Exception:
        return ("Specified outcomes list was not valid JSON.", 400)

    if not isinstance(outcomes, list):
        return ("Outcomes object was not a list.", 400)

    for i, outcome in enumerate(outcomes):
        if (
            not isinstance(outcome, list)
         or len(outcome) != 3
         or not isinstance(outcome[0], bool)
         or not isinstance(outcome[1], anystr)
         or not isinstance(outcome[2], anystr)
        ):
            return (
                "Outcome {} was invalid (each outcome must be a list"
                " containing a boolean and two strings)."
            ).format(i)

    # Get code blocks, decode JSON, and ensure it's a list of pairs of
    # strings. It *is* allowed to be an empty list.
    codeString = form.get("code", "")
    if codeString == "":
        return ("Delivery did not specify any code.", 400)

    try:
        codeBlocks = json.loads(codeString)
    except Exception:
        return ("Specified code list was not valid JSON.", 400)

    if not isinstance(codeBlocks, list):
        return ("Code object was not a list.", 400)

    for i, block in enumerate(codeBlocks):
        if (
            not isinstance(block, list)
         or len(block) != 2
         or not all(isinstance(part, anystr) for part in block)
        ):
            return (
                "Code block {} was invalid (each code block must be a"
                " list containing two strings)."
            ).format(i)

    # Check authors against roster
    try:
        roster = storage.get_roster(course, semester)
    except Exception:
        return (
            (
                "Could not fetch roster for course {} {}."
            ).format(course, semester),
            400
        )

    if roster is None:
        return (
            (
                "There is no roster for course {} {}."
            ).format(course, semester),
            400
        )

    for author in authors:
        if author not in roster:
            return (
                (
                    "Author '{}' is not on the roster for {} {}. You"
                    " must use your username when specifying an author."
                ).format(author, course, semester),
                400
            )

    # Grab task info and amend it just to determine egroup phases
    task_info = storage.get_task_info(course, semester)

    # Record the outcomes list for each author (extensions might be
    # different so credit might differ per author)
    shared_status = None
    statuses = {}
    for author in authors:

        # Get exercise info so we can actually figure out what the
        # evaluation would be for these outcomes.
        if task_info is None:
            return (
                "Failed to load tasks.json for {} {}.".format(
                    course,
                    semester
                ),
                400
            )

        # Per-author phase/extension info
        this_author_task_info = copy.deepcopy(task_info)
        amend_exercises(course, semester, this_author_task_info, {}, author)

        einfo = None
        for group in this_author_task_info.get("exercises", []):
            elist = group["exercises"]

            # Make allowances for old format
            if isinstance(elist, dict):
                for eid in elist:
                    elist[eid]['id'] = eid
                elist = list(elist.values())

            for ex in elist:
                if exercise == ex['id']:
                    einfo = ex
                    break
            if einfo is not None:
                break

        if einfo is None:
            return (
                "Exercise '{}' is not listed in {} {}.".format(
                    exercise,
                    course,
                    semester
                ),
                400
            )

        status, ecredit, gcredit = exercise_credit(einfo, outcomes)
        statuses[author] = status

        if shared_status is None:
            shared_status = status
        elif shared_status == "mixed" or shared_status != status:
            shared_status = "mixed"
        # else it remains the same

        storage.save_outcomes(
            course,
            semester,
            author,
            exercise,
            authors,
            outcomes,
            codeBlocks,
            status,
            ecredit,
            gcredit
        )

    if shared_status == "mixed":
        message = (
            "Submission accepted: {}/{} checks passed, but status is"
            " different for different authors:\n{}"
        ).format(
            len([x for x in outcomes if x[0]]),
            len(outcomes),
            '\n'.join(
                "  for {}: {}".format(author, status)
                for (author, status) in statuses.items()
            )
        )
        if any(status != "complete" for status in statuses.values()):
            message += (
                "\nNote: this submission is NOT complete for all authors."
            )
    else:
        message = (
            "Submission accepted: {}/{} checks passed and status is {}."
        ).format(
            len([x for x in outcomes if x[0]]),
            len(outcomes),
            shared_status
        )
        if shared_status != "complete":
            message += "\nNote: this submission is NOT complete."

    return message


@app.route(
    '/<course>/<semester>/exercise/<target_user>/<eid>',
    methods=['GET']
)
@flask_cas.login_required
@augment_arguments
def route_exercise(
    course,
    semester,
    target_user,
    eid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    # Check view permission
    if target_user != effective_user and not is_admin:
        return error_response(
            course,
            semester,
            username,
            "You are not allowed to view exercises for {}.".format(target_user)
        )
    elif target_user != effective_user:
        flask.flash("Viewing exercise for {}.".format(target_user))

    # From here on we treat the effective user as the target user
    effective_user = target_user

    # Check roster and flash a warning if we're viewing feedback for a
    # user who is not on the roster...
    try:
        roster = storage.get_roster(course, semester)
    except Exception as e:
        flask.flash(str(e))
        roster = None

    if roster is None:
        flask.flash(
            "Warning: could not fetch roster to check if this user is on"
            " it."
        )
    elif effective_user not in roster:
        flask.flash("Warning: this user is not on the roster!")

    # Get exercise info:
    einfo = None
    ginfo = None
    for group in task_info.get("exercises", []):
        elist = group["exercises"]

        # Make allowances for old format
        if isinstance(elist, dict):
            for eid in elist:
                elist[eid]['id'] = eid
            elist = list(elist.values())

        for ex in elist:
            if eid == ex['id']:
                ginfo = group
                einfo = ex
                break
        if einfo is not None:
            break

    # Grab best-outcomes info for the exercise in question
    outcomes = fetch_all_best_outcomes(
        course,
        semester,
        effective_user,
        task_info,
        only_exercises={eid}
    )

    # Amend exercises to set statuses
    amend_exercises(course, semester, task_info, outcomes, target_user)

    # Get particular outcome
    results = outcomes.get(
        eid,
        {  # default when exercise hasn't been submitted
            "submitted_at": None,
            "on_time": True,
            "authors": [],
            "outcomes": [],
            "code": [],
            "status": "unsubmitted",
            "credit": None
        }
    )

    # Render override notes as HTML
    if results['code'] == '__override__':
        results['outcomes'] = potluck.render.render_markdown(
            results['outcomes']
        )

    # Grab all attempts by category for the target exercise
    all_submissions = []
    for category in ["override", "full", "partial", "none"]:
        allForCat = storage.fetch_outcomes(
            course,
            semester,
            effective_user,
            eid,
            category
        )
        if allForCat is None:
            allForCat = []
        all_submissions.extend(allForCat)
    legacy = storage.fetch_old_outcomes(course, semester, effective_user, eid)
    if legacy is not None:
        all_submissions.extend(legacy)

    # Get deadline info
    deadline = get_exercise_deadline(
        course,
        semester,
        effective_user,
        task_info,
        ginfo
    )

    # Update all submissions to set on_time & group_credit values
    for sub in all_submissions:
        storage.update_submission_credit(
            sub,
            deadline,
            usual_config_value(
                "LATE_EXERCISE_CREDIT_FRACTION",
                task_info,
                exercise=eid,
                default=0.5
            )
        )
        # Render override notes as HTML
        if sub['code'] == '__override__':
            sub['outcomes'] = potluck.render.render_markdown(
                sub['outcomes']
            )

    # Sort by submission time, with a few fall-backs
    all_submissions.sort(
        key=lambda outcome: (
            outcome.get("submitted_at", "_") == "on_time",
            outcome.get("submitted_at", "_") == "late",
            outcome.get("submitted_at", "_"),
            outcome.get("status", "_"),
            outcome.get("group_credit", "_"),
            outcome.get("credit", "_"),
            outcome.get("code", "_"),
        )
    )

    return flask.render_template(
        'exercise.j2',
        course_name=task_info.get("course_name", course),
        course=course,
        semester=semester,
        username=username,
        is_admin=is_admin,
        masquerade_as=masquerade_as,
        target_user=target_user,
        task_info=task_info,
        eid=eid,
        ginfo=ginfo,
        einfo=einfo,
        results=results,
        all_submissions=all_submissions
    )


@app.route(
    '/<course>/<semester>/ex_override/<target_user>/<eid>',
    methods=['POST']
)
@flask_cas.login_required
@augment_arguments
def route_exercise_override(
    course,
    semester,
    target_user,
    eid,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Accessible by admins only, this route is the form target for the
    exercise and/or exercise group override controls.
    """
    if not is_admin:
        # TODO: Grader role!
        flask.flash("Only admins can set exercise overrides.")
        return goback(course, semester)

    # Get form values:
    try:
        override_for = flask.request.form["override_for"]
    except Exception:
        flask.flash("Override target (exercise vs. group) not specified.")
        return goback(course, semester)

    if override_for not in ["group", "exercise"]:
        flask.flash("Invalid override target '{}'.".format(override_for))
        return goback(course, semester)

    try:
        credit = flask.request.form["credit"]
    except Exception:
        flask.flash("Override credit value not specified.")
        return goback(course, semester)

    if credit != '':
        try:
            credit = float(credit)
        except Exception:
            flask.flash("Invalid credit value '{}'.".format(credit))
            return goback(course, semester)

    try:
        note = flask.request.form["note"]
    except Exception:
        note = "-no explanation provided-"

    try:
        status = flask.request.form["status"]
    except Exception:
        status = "auto"

    if override_for == "group":
        group_id = None
        for egroup in task_info.get("exercises", []):
            egid = egroup["group"]
            for exercise in egroup.get("exercises", []):
                if exercise.get("id") == eid:
                    group_id = egid
                    break
            if group_id is not None:
                break
        if group_id is None:
            flask.flash(
                "Could not find group ID for exercise '{}'.".format(eid)
            )
            return goback(course, semester)

        if status == "auto":
            status = ""
        storage.set_egroup_override(
            course,
            semester,
            target_user,
            group_id,
            override=credit,
            note=note,
            status=status
        )

    else:  # Must be "exercise"

        # check task_info and emit a warning if eid isn't there:
        found = False
        for egroup in task_info.get("exercises", []):
            for exercise in egroup.get("exercises", []):
                if exercise.get("id") == eid:
                    found = True
                    break
            if found:
                break
        if not found:
            flask.flash(
                (
                    "Warning: exercise '{}' is not listed in task info."
                    " Entering override for it anyways."
                ).format(eid)
            )

        try:
            time_override = flask.request.form["time_override"]
        except Exception:
            time_override = None

        if status == "auto":
            if credit >= 1.0:
                status = "complete"
            elif credit > 0:
                status = "partial"
            else:
                status = "incomplete"

        storage.save_outcomes_override(
            course,
            semester,
            target_user,
            eid,
            username,
            note,
            status,
            credit,
            time_override=time_override
        )

    return goback(course, semester)


@app.route('/<course>/<semester>/ex_gradesheet/<group>', methods=['GET'])
@flask_cas.login_required
@augment_arguments
def route_ex_gradesheet(
    course,
    semester,
    group,
    # Augmented arguments
    username,
    is_admin,
    masquerade_as,
    effective_user,
    task_info
):
    """
    Visible by admins only, this route displays an overview of the status
    of every student on the roster, with links to the extensions manager
    and to feedback views for each student.
    """
    if not is_admin:
        flask.flash("You do not have permission to view gradesheets.")
        return goback(course, semester)

    # Create base task info from logged-in user's perspective
    base_task_info = copy.deepcopy(task_info)
    amend_exercises(course, semester, base_task_info, {}, username)

    egroups = base_task_info.get("exercises")
    if egroups is None:
        msg = "No exercises defined in tasks.json."
        flask.flash(msg)
        return error_response(course, semester, username, msg)

    # Get the roster
    try:
        roster = storage.get_roster(course, semester)
    except Exception as e:
        flask.flash(str(e))
        roster = None

    if roster is None:
        msg = "Failed to load <code>roster.csv</code>."
        flask.flash(msg)
        return error_response(course, semester, username, msg)

    # Figure out the index for this group
    group_index = None
    group_obj = None
    for i, group_entry in enumerate(egroups):
        if "timely_by" not in group_entry:
            print(group_entry)
            raise ValueError("HA")
        if group_entry["group"] == group:
            group_index = i
            group_obj = group_entry
            break

    if group_index is None:
        msg = (
            "Exercise group '{}' not found for this course/semester."
        ).format(group)
        flask.flash(msg)
        return error_response(course, semester, username, msg)

    rows = []
    for stid in sorted(
        roster,
        key=lambda stid: (
            roster[stid]["course_section"],
            roster[stid]["sortname"]
        )
    ):
        if roster[stid]["course_section"] == "__hide__":
            continue
        row = roster[stid]
        row_info = copy.deepcopy(task_info)
        row["task_info"] = row_info

        # Grab latest-outcomes info for ALL exercises
        row_outcomes = fetch_all_best_outcomes(
            course,
            semester,
            stid,
            row_info,
            only_groups=[group]
        )
        row["outcomes"] = row_outcomes

        # Amend this row's exercises w/ this student's outcomes
        amend_exercises(course, semester, row_info, row_outcomes, stid)

        # Fetch group from amended task_info via group index
        this_group = row_info["exercises"][group_index]

        row["this_group"] = this_group

        rows.append(row)

    # Get the student info
    try:
        student_info = storage.get_student_info(course, semester)
    except Exception as e:
        flask.flash(str(e))
        student_info = None

    return flask.render_template(
        'exercise_gradesheet.j2',
        course_name=task_info.get("course_name", course),
        course=course,
        semester=semester,
        username=username,
        is_admin=is_admin,
        masquerade_as=masquerade_as,
        task_info=task_info,
        group=group,
        group_obj=group_obj,
        roster=rows,
        student_info=student_info
    )


#---------#
# Helpers #
#---------#

def error_response(course, semester, username, cause):
    """
    Shortcut for displaying major errors to the users so that they can
    bug the support line instead of just getting a pure 404.
    """
    return flask.render_template(
        'error.j2',
        course_name=course,
        course=course,
        semester=semester,
        username=username,
        announcements="",
        support_link=fallback_config_value(
            "SUPPORT_LINK",
            app.config,
            DEFAULT_CONFIG
        ),
        error=cause,
        task_info={}
    )


def get_pr_obj(task_info, prid):
    """
    Gets the project object with the given ID. Raises a ValueError if
    there is no such object, or if there are multiple matches.
    """
    psmatches = [
        pr
        for pr in task_info.get("projects", task_info["psets"])
        if pr["id"] == prid
    ]
    if len(psmatches) == 0:
        raise ValueError("Unknown problem set '{}'".format(prid))
    elif len(psmatches) > 1:
        raise ValueError("Multiple problem sets with ID '{}'!".format(prid))
    else:
        return psmatches[0]


def get_task_obj(task_info, pr_obj, taskid, redirect=Exception):
    """
    Extracts a task object with the given ID from the given task info
    and project objects, merging project-specific fields with universal
    task fields. Raises a ValueError if there is no matching task object
    or if there are multiple matches.
    """
    universal = task_info["tasks"].get(taskid, None)
    taskmatches = [task for task in pr_obj["tasks"] if task["id"] == taskid]
    if len(taskmatches) == 0:
        raise ValueError(
            "Problem set {} has no task '{}'".format(pr_obj["id"], taskid)
        )
    elif universal is None:
        raise ValueError(
            (
                "Problem set {} has a task '{}' but that task has no"
                " universal specification."
            ).format(pr_obj["id"], taskid)
        )
    elif len(taskmatches) > 1:
        raise ValueError(
            "Multiple tasks in problem set {} with ID '{}'!".format(
                pr_obj["id"],
                taskid
            )
        )
    else:
        result = {}
        result.update(universal)
        result.update(taskmatches[0])
        return result


def check_user_privileges(admin_info, username):
    """
    Returns a pair containing a boolean indicating whether a user is an
    admin or not, and either None, or a string indicating the username
    that the given user is masquerading as.

    Requires admin info as returned by get_admin_info.
    """
    admins = admin_info.get("admins", [])
    is_admin = username in admins

    masquerade_as = None
    # Only admins can possibly masquerade
    if is_admin:
        masquerade_as = admin_info.get("MASQUERADE", {}).get(username)
        # You cannot masquerade as an admin
        if masquerade_as in admins:
            flask.flash("Error: You cannot masquerade as another admin!")
            masquerade_as = None
    elif admin_info.get("MASQUERADE", {}).get(username):
        print(
            (
                "Warning: User '{}' cannot masquerade because they are"
              + "not an admin."
            ).format(username)
        )

    return (is_admin, masquerade_as)


def set_pause_time(admin_info, task_info, username, masquerade_as=None):
    """
    Sets the PAUSE_AT value in the given task_info object based on any
    PAUSE_USERS entries for either the given true username or the given
    masquerade username. The pause value for the username overrides the
    value for the masqueraded user, so that by setting PAUSE_AT for an
    admin account plus creating a masquerade entry, you can act as any
    user at any point in time.
    """
    pu = admin_info.get("PAUSE_USERS", {})
    if username in pu:
        task_info["PAUSE_AT"] = pu[username]
    elif masquerade_as in pu:
        task_info["PAUSE_AT"] = pu[masquerade_as]
    elif "PAUSE_AT" in admin_info:
        task_info["PAUSE_AT"] = admin_info["PAUSE_AT"]
    # else we don't set PAUSE_AT at all


def amend_task_info(course, semester, task_info, username):
    """
    Amends task info object with extra keys in each project to indicate
    project state. Also adds summary information to each task of the
    project based on user feedback generated so far. Also checks potluck
    inflight status and adds a "submitted" key to each task where
    appropriate. Template code should be careful not to reveal feedback
    info not warranted by the current project state.
    """
    for project in task_info.get("projects", task_info["psets"]):
        # Add status info to the project object:
        amend_project_and_tasks(
            course,
            semester,
            task_info,
            project,
            username
        )


def amend_project_and_tasks(
    course,
    semester,
    task_info,
    project_obj,
    username
):
    """
    Calls amend_project on the given project object, and then amend_task
    on each task in it, adding "revision" entries to each task w/
    amended revision info.

    Also adds "pool_status" keys to each task indicating the best status
    of any task that's pooled with that one. That will be 'complete' if
    there's a complete task in the pool, 'some_submission' if there's
    any unsubmitted task in the pool, an 'unsubmitted' if there are no
    submitted tasks in the pool.
    """
    amend_project(course, semester, task_info, project_obj, username)
    # Add summary info to each task, and duplicate for revisions and
    # belated versions
    for task in project_obj["tasks"]:
        rev_task = copy.deepcopy(task)
        belated_task = copy.deepcopy(task)
        amend_task(
            course,
            semester,
            task_info,
            project_obj["id"],
            rev_task,
            username,
            "revision"
        )
        task["revision"] = rev_task

        amend_task(
            course,
            semester,
            task_info,
            project_obj["id"],
            belated_task,
            username,
            "belated"
        )
        task["belated"] = belated_task

        amend_task(
            course,
            semester,
            task_info,
            project_obj["id"],
            task,
            username,
            "initial"
        )

    # Figure out best status in each pool
    pool_statuses = {}
    for task in project_obj["tasks"]:
        # Get submission status
        status = task["submission_status"]
        if status not in ("unsubmitted", "complete"):
            status = "some_submission"

        rev_status = task.get("revision", {}).get(
            "submission_status",
            "unsubmitted"
        )
        if rev_status not in ("unsubmitted", "complete"):
            rev_status = "some_submission"
        bel_status = task.get("belated", {}).get(
            "submission_status",
            "unsubmitted"
        )
        if bel_status not in ("unsubmitted", "complete"):
            bel_status = "some_submission"

        # Figure out best status across revision/belated phases
        points = map(
            lambda x: {
                "unsubmitted": 0,
                "some_submission": 1,
                "complete": 2
            }[x],
            [status, rev_status, bel_status]
        )
        status = {
            0: "unsubmitted",
            1: "some_submission",
            2: "complete"
        }[max(points)]

        # Figure out this task's pool and update the score for that pool
        pool = task_pool(task)

        prev_status = pool_statuses.get(pool)
        if (
            prev_status is None
         or prev_status == "unsubmitted"
         or prev_status == "some_submission" and status == "complete"
        ):
            pool_statuses[pool] = status

    # Now assign pool_status slots to each task
    for task in project_obj["tasks"]:
        pool = task_pool(task)
        task["pool_status"] = pool_statuses[pool]


def amend_project(course, semester, task_info, project_obj, username):
    """
    Adds a "status" key to the given problem set object (which should be
    part of the given task info). The username is used to look up
    extension information.
    """
    initial_ext = storage.get_extension(
        course,
        semester,
        username,
        project_obj["id"],
        "initial"
    )
    if initial_ext is None:
        flask.flash(
            "Error fetching initial extension info (treating as 0)."
        )
        initial_ext = 0

    revision_ext = storage.get_extension(
        course,
        semester,
        username,
        project_obj["id"],
        "revision"
    )
    if revision_ext is None:
        flask.flash(
            "Error fetching revision extension info (treating as 0)."
        )
        revision_ext = 0

    project_obj["status"] = project_status_now(
        username,
        task_info,
        project_obj,
        extensions=[initial_ext, revision_ext]
    )


def amend_task(course, semester, task_info, prid, task, username, phase):
    """
    Adds task-state-related keys to the given task object. The following
    keys are added:

    - "feedback_summary": A feedback summary object (see
        `get_feedback_summary`).
    - "time_spent": The time spent info that the user entered for time
        spent when submitting the task (see
        `potluck_app.storage.fetch_time_spent` for the format). Will be
        None if that info isn't available.
    - "submitted": True if the user has attempted submission (even if
        there were problems) or if we have feedback for them (regardless
        of anything else).
    - "submitted_at": A `datetime.datetime` object representing when
        the submission was received, or None if there is no recorded
        submission.
    - "eval_elapsed": A `datetime.timedelta` that represents the time
        elapsed since evaluation was started for the submission (in
        possibly fractional seconds).
    - "eval_timeout": A `datetime.timedelta` representing the number
        of seconds before the evaluation process should time out.
    - "eval_status": The status of the evaluation process (see
        `get_inflight`).
    - "submission_status": A string representing the status of the
        submission overall. One of:
        - "unsubmitted": no submission yet.
        - "inflight": has been submitted; still being evaluated.
        - "unprocessed": evaluated but there's an issue (evaluation
            crashed or elsehow failed to generate feedback).
        - "issue": evaluated but there's an issue (evaluation warning or
            'incomplete' evaluation result.)
        - "complete": Evaluated and there's no major issue (grade may or
            may not be perfect, but it better than "incomplete").
    - "submission_icon": A one-character string used to represent the
        submission status.
    - "submission_desc": A brief human-readable version of the
        submission status.
    - "grade": A numerical grade value, derived from the evaluation via
        the EVALUATION_SCORES dictionary defined in the config file. If
        no grade has been assigned, it will be the string '?' instead of
        a number. Grade overrides are factored in if present.
    - "grade_overridden": A boolean indicating whether the grade was
        overridden or not. Will be true when there's an override active
        even if the override indicates the same score as the automatic
        grade.
    - "timeliness": A numerical score value for timeliness points, only
        present when an override has been issued. Normally, timeliness
        points are computed for an already-augmented task based on the
        initial/revised/belated submission statuses.
    - "timeliness_overridden": A boolean indicating whether the
        timeliness score was overridden or not.
    - "notes": A string indicating the markdown source for custom notes
        applied to the task by an evaluator.
    - "notes_html": A string of HTML code rendered from the notes
        markdown.
    - "max_score": A number representing the maximum score possible
        based on the phase of the submission, either SCORE_BASIS for
        initial submissions, REVISION_MAX_SCORE for revisions, or
        BELATED_MAX_SCORE for belated submissions.
    - "max_revision_score": A number representing the max score possible
        on a revision of this task (regardless of whether this is an
        initial or revised submission)
    - "max_belated_score": A number representing the max score possible
        on a belated submission of this task (regardless of whether this
        is an initial, revised, or belated submission)
    """
    # Fetch basic info
    task["feedback_summary"] = storage.get_feedback_summary(
        course,
        semester,
        task_info,
        username,
        phase,
        prid,
        task["id"]
    )
    task["time_spent"] = storage.fetch_time_spent(
        course,
        semester,
        username,
        phase,
        prid,
        task["id"]
    )

    # Get submitted value
    # Note that we hedge here against the possibility that the feedback
    # summary isn't readable since some kinds of bad crashes of the
    # evaluator can cause that to happen (e.g., student accidentally
    # monkey-patches json.dump so that no report can be written).
    task["submitted"] = (task.get("feedback_summary") or {}).get("submitted")

    # Get inflight info so we know about timeouts
    ts, logfile, reportfile, status = storage.get_inflight(
        course,
        semester,
        username,
        phase,
        prid,
        task["id"]
    )

    # Get current time (IN UTC)
    now = potluck.time_utils.now()

    # Time submitted and time elapsed since submission
    if ts == "error":
        task["submitted_at"] = "unknown"
        task["eval_elapsed"] = "unknown"
    elif ts is not None:
        submit_time = potluck.time_utils.local_time(
            task_info,
            potluck.time_utils.time_from_timestring(ts)
        )
        task["submitted_at"] = submit_time
        task["eval_elapsed"] = now - submit_time
    else:
        try:
            submit_time = potluck.time_utils.local_time(
                task_info,
                potluck.time_utils.time_from_timestring(
                    task["feedback_summary"]["timestamp"]
                )
            )
            task["submitted_at"] = submit_time
            task["eval_elapsed"] = now - submit_time
        except Exception:
            task["submitted_at"] = None
            task["eval_elapsed"] = None

    task["eval_timeout"] = datetime.timedelta(
        seconds=usual_config_value(
            "FINAL_EVAL_TIMEOUT",
            task_info,
            task=task["id"]
        )
    )

    # Set eval_status
    if ts == "error":
        task["eval_status"] = "unknown"
    else:
        task["eval_status"] = status

    # Override submitted value
    if status is not None:
        task["submitted"] = True

    # Add max score info
    max_score = usual_config_value(
        "SCORE_BASIS",
        task_info,
        task=task["id"],
        default=100
    )
    revision_max = usual_config_value(
        "REVISION_MAX_SCORE",
        task_info,
        task=task["id"],
        default=100
    )
    belated_max = usual_config_value(
        "BELATED_MAX_SCORE",
        task_info,
        task=task["id"],
        default=85
    )
    if phase == "revision":
        task["max_score"] = revision_max
    elif phase == "belated":
        task["max_score"] = belated_max
    else:
        task["max_score"] = max_score
    task["max_revision_score"] = revision_max
    task["max_belated_score"] = belated_max

    # Add grade info
    if task["eval_status"] in ("unknown", "initial", "in_progress"):
        task["grade"] = "?"
    elif task["eval_status"] in ("error", "expired"):
        task["grade"] = 0
    elif task["eval_status"] == "completed" or task["submitted"]:
        task["grade"] = usual_config_value(
            [
                "EVALUATION_SCORES",
                task["feedback_summary"]["evaluation"]
            ],
            task_info,
            task=task["id"],
            default=usual_config_value(
                ["EVALUATION_SCORES", "__other__"],
                task_info,
                task=task["id"],
                default="???"
            )
        )
        if task["grade"] == "???":
            flask.flash(
                (
                    "Warning: evaluation '{}' has not been assigned a"
                  + " grade value!"
                ).format(
                    task["feedback_summary"]["evaluation"]
                )
            )
            task["grade"] = None
    else:
        task["grade"] = None

    # Check for a grade override and grading note
    notes, notes_html, override, timeliness_override = get_evaluation_info(
        course,
        semester,
        username,
        phase,
        prid,
        task["id"]
    )
    task["notes"] = notes
    task["notes_html"] = notes_html
    if override == '':
        task["grade_overridden"] = False
    else:
        task["grade_overridden"] = True
        task["grade"] = override

    if timeliness_override == '':
        task["timeliness_overridden"] = False
        # No timeliness slot at all
    else:
        if phase != 'initial':
            flask.flash(
                (
                    "Warning: timeliness override {} for {} {} in phase"
                    " {} will be ignored: only overrides for the"
                    " initial phase are applied."
                ).format(timeliness_override, prid, task["id"], phase)
            )
        task["timeliness_overridden"] = True
        task["timeliness"] = timeliness_override

    # Set detailed submission status along with icon and description
    if task["eval_status"] == "unknown":
        task["submission_status"] = "inflight"
        task["submission_icon"] = "‽"
        task["submission_desc"] = "status unknown"
    if task["eval_status"] in ("initial", "in_progress"):
        task["submission_status"] = "inflight"
        task["submission_icon"] = "?"
        task["submission_desc"] = "evaluation in progress"
    elif task["eval_status"] in ("error", "expired"):
        task["submission_status"] = "unprocessed"
        task["submission_icon"] = "☹"
        task["submission_desc"] = "processing error"
    elif task["eval_status"] == "completed" or task["submitted"]:
        report = task["feedback_summary"]
        if report["warnings"]:
            task["submission_status"] = "issue"
            task["submission_icon"] = "✗"
            task["submission_desc"] = "major issue"
        elif report["evaluation"] == "incomplete":
            task["submission_status"] = "issue"
            task["submission_icon"] = "✗"
            task["submission_desc"] = "incomplete submission"
        elif report["evaluation"] == "not evaluated":
            task["submission_status"] = "unprocessed"
            task["submission_icon"] = "☹"
            task["submission_desc"] = "submission not evaluated"
        else:
            task["submission_status"] = "complete"
            task["submission_icon"] = "✓"
            task["submission_desc"] = "submitted"
    else:
        task["submission_status"] = "unsubmitted"
        task["submission_icon"] = "…"
        task["submission_desc"] = "not yet submitted"


def exercise_credit(exercise_info, outcomes):
    """
    Returns a triple containing a submission status string, a number for
    exercise credit (or None), and a number for group credit (possibly
    0). These are based on whether the given outcomes list matches the
    expected outcomes for the given exercise info (should be an
    individual exercise dictionary). These values will NOT account for
    whether the submission is on-time or late.

    The status string will be one of:

    - "complete" if all outcomes are successful.
    - "partial" if some outcome failed, but at least one non-passive
        outcome succeeded (passive outcomes are those expected to succeed
        even when no code is written beyond the starter code, but which
        may fail if bad code is written).
    - "incomplete" if not enough outcomes are successful for partial
        completeness, or if there's an issue like the wrong number of
        outcomes being reported.

    This function won't return it, but "unsubmitted" is another possible
    status string used elsewhere.
    """
    group_credit = 0
    exercise_credit = None
    n_outcomes = len(outcomes)

    exp_outcomes = exercise_info.get('count')
    if exp_outcomes is None and 'per_outcome' in exercise_info:
        exp_outcomes = len(exercise_info['per_outcome'])

    if exp_outcomes is None:
        # Without info on how many outcomes we're expecting, we currently
        # don't have a way to know if an outcome is passive (or which
        # concept(s) it might deal with).
        # TODO: Less fragile way to associate outcomes w/ concepts!

        # In this case, at least one outcome is required!
        if len(outcomes) == 0:
            submission_status = "incomplete"
        else:
            # Otherwise, all-success -> complete; one+ success -> partial
            passed = [outcome for outcome in outcomes if outcome[0]]
            if len(passed) == len(outcomes):
                submission_status = "complete"
                exercise_credit = 1
            elif len(passed) > 0:
                submission_status = "partial"
                exercise_credit = 0.5
            else:
                submission_status = "incomplete"
                exercise_credit = 0
            # Accumulate credit
            group_credit = exercise_credit
    elif n_outcomes != exp_outcomes:
        # If we have an expectation for the number of outcomes and the
        # actual number doesn't match that, we won't know which outcomes
        # might be passive vs. active, and we don't know how to map
        # outcomes onto per-outcome concepts... so we just ignore the
        # whole exercise and count it as not-yet-submitted.
        # TODO: Less fragile way to associate outcomes w/ concepts!
        submission_status = "incomplete"
        # No group credit accrues in this case
    elif len(outcomes) == 0:
        # this exercise doesn't contribute to any concept
        # statuses, and that's intentional. Since it doesn't
        # have outcomes, any submission counts as complete.
        submission_status = "complete"
        # Here we directly add to group credit but leave
        # exercise_credit as None.
        group_credit = 1
    else:
        # Get list of outcome indices for successes
        passed = [
            i
            for i in range(len(outcomes))
            if outcomes[i][0]
        ]
        # Get list of which outcomes are passive
        passives = exercise_info.get("passive", [])
        if len(passed) == n_outcomes:
            # If everything passed, the overall is a pass
            exercise_credit = 1
            submission_status = "complete"
        elif any(i not in passives for i in passed):
            # at least one non-passive passed -> partial
            exercise_credit = 0.5
            submission_status = "partial"
        else:
            # only passing tests were partial & at least one
            # failed -> no credit
            exercise_credit = 0
            submission_status = "incomplete"

        # Set group credit
        group_credit = exercise_credit

    return (submission_status, exercise_credit, group_credit)


def get_exercise_deadline(
    course,
    semester,
    username,
    task_info,
    egroup
):
    """
    Given a particular course/semester/user, the task_info object, and
    an exercise group dictionary form within the task info, fetches that
    user's extension info for that group and returns a
    `datetime.datetime` object representing that user's deadline for
    that exercise group.
    """
    # Standard extension hours
    standard_ext_hrs = task_info.get("extension_hours", 24)

    # Get extension value
    extension = storage.get_extension(
        course,
        semester,
        username,
        egroup["group"],
        "initial"
    )
    if extension is None:
        flask.flash(
            "Error fetching exercise extension info (treating as 0)."
        )
        extension = 0
    elif extension is True:
        extension = standard_ext_hrs
    elif extension is False:
        extension = 0
    elif not isinstance(extension, (int, float)):
        flask.flash(
            "Ignoring invalid initial extension value '{}'".format(
                extension
            )
        )
        extension = 0

    # Get timely time
    timely_by = potluck.time_utils.task_time__time(
        task_info,
        egroup["timely"],
        default_time_of_day=task_info.get(
            "default_release_time_of_day",
            "23:59"
        )
    )

    # Apply the extension
    return timely_by + datetime.timedelta(hours=extension)


def fetch_all_best_outcomes(
    course,
    semester,
    username,
    task_info,
    only_groups=None,
    only_exercises=None
):
    """
    Fetches a dictionary mapping each individual exercise ID to the best
    outcome for that exercise (omitting keys for exercise IDs where the
    user hasn't submitted anything yet).

    If `only_groups` is supplied, it should be a sequence of groups to
    fetch outcomes for (instead of 'all groups') and if `only_exercises`
    is supplied, it should be a sequence of specific exercises to fetch
    outcomes for. When both are given, exercises not in one of the
    specified groups will not be fetched.
    """
    outcomes = {}
    use_groups = task_info["exercises"]
    if only_groups is not None:
        use_groups = [
            group
            for group in use_groups
            if group["group"] in only_groups
        ]
    for egroup in use_groups:
        deadline = get_exercise_deadline(
            course,
            semester,
            username,
            task_info,
            egroup
        )
        for ex in egroup["exercises"]:
            eid = ex["id"]
            # Filter by eid if we were told to only do some
            if only_exercises is not None and eid not in only_exercises:
                continue
            ebest = storage.fetch_best_outcomes(
                course,
                semester,
                username,
                eid,
                deadline,
                usual_config_value(
                    "LATE_EXERCISE_CREDIT_FRACTION",
                    task_info,
                    exercise=eid,
                    default=0.5
                )
            )
            if ebest is not None:
                outcomes[eid] = ebest

    return outcomes


def amend_exercises(course, semester, task_info, outcomes, username):
    """
    Amends the exercises in the provided task info based on the given
    outcomes. It adds time + submission statuses for each exercise, as
    well as extension info based on the provided
    course/semester/username.

    Each exercise group will gain a "phase" slot with a string
    indicating which time phase it's in (see the "exercises" entry
    above). Each group will also gain an "extension" slot that holds a
    number specifying how many hours of extension the user has been
    granted for that exercise group, and a "timely_by" slot that holds a
    datetime object indicating the deadline with any extension factored
    in.

    Also, each individual exercise which has been submitted will
    gain the following slots:

    - a "status" slot with a submission status string (also see above).
    - a "credit" slot with a numerical credit value, or None for
        unsubmitted exercises.
    - a "group_credit" slot with a numerical credit value towards group
        credit, which is usually the same as "credit".

    Finally, the exercise groups will gain a "credit_fraction" slot
    indicating what fraction of credit has been received, and a "status"
    slot aggregating the statuses of its components, depending on its
    phase. This group status is determined as follows:

    1. If all of the exercises in the group are complete, it counts as
        "perfect".
    2. If at least 80% (configurable as `EXERCISE_GROUP_THRESHOLD`) of
        the exercises in the group are complete (counting
        partially-complete exercises as 1/2) then the group counts as
        "complete".
    3. If at least `EXERCISE_GROUP_PARTIAL_THRESHOLD` (default 2/5) but
        less than the `EXERCISE_GROUP_THRESHOLD` fraction of the
        exercises are complete, and the phase is "due" then the status
        will be "partial".
    4. If a smaller fraction than `EXERCISE_GROUP_PARTIAL_THRESHOLD` of
        the exercises are complete (still counting partial completions
        as 1/2) and the phase is "due" then the status will be
        "incomplete".
    5. If the status would be less than "complete" but the phase is
        "released" instead of "due" then the status will be "pending"
        (including when zero exercises have been submitted yet).
    6. If the phase is "prerelease" then the status will be "unreleased"
        unless submissions to one or more exercises have already
        happened, in which case its status will be one of "pending",
        "complete", or "perfect" depending on how many exercises are
        complete.

    Note: an empty outcomes dictionary may be provided if you only care
    about setting group phase and extension info and are willing to let
    credit info be inaccurate.
    """
    # Get current time:
    if "PAUSE_AT" in task_info and task_info["PAUSE_AT"]:
        now = potluck.time_utils.task_time__time(
            task_info,
            task_info["PAUSE_AT"]
        )
    else:
        now = potluck.time_utils.now()

    # Standard extension hours
    standard_ext_hrs = task_info.get("extension_hours", 24)

    # Amend groups and exercises
    for group in task_info.get("exercises", []):
        # Get extension value
        extension = storage.get_extension(
            course,
            semester,
            username,
            group["group"],
            "initial"
        )
        if extension is None:
            flask.flash(
                "Error fetching exercise extension info (treating as 0)."
            )
            extension = 0
        elif extension is True:
            extension = standard_ext_hrs
        elif extension is False:
            extension = 0
        elif not isinstance(extension, (int, float)):
            flask.flash(
                "Ignoring invalid initial extension value '{}'".format(
                    extension
                )
            )
            extension = 0
        # Now 'extension' is a number so we store it
        group["extension"] = extension

        # Get release + timely times
        release_at = potluck.time_utils.task_time__time(
            task_info,
            group["release"],
            default_time_of_day=task_info.get(
                "default_release_time_of_day",
                "23:59"
            )
        )
        timely_by = potluck.time_utils.task_time__time(
            task_info,
            group["timely"],
            default_time_of_day=task_info.get(
                "default_release_time_of_day",
                "23:59"
            )
        )

        # Apply the extension
        timely_by += datetime.timedelta(hours=extension)

        # Store calculated deadline
        group["timely_by"] = timely_by

        # Figure out and apply time phase to group
        if now < release_at:
            phase = "prerelease"
        elif now < timely_by:
            phase = "released"
        else:
            phase = "due"
        group["phase"] = phase

        # Tracks exercise credit & max for all exercises in the group
        group_credit = 0
        group_max = 0

        # Make allowances for old format
        elist = group["exercises"]
        if isinstance(elist, dict):
            for eid in elist:
                elist[eid]['id'] = eid
            elist = list(elist.values())

        # Consider each individual exercise in the group
        for einfo in elist:
            eid = einfo['id']
            # Add to max credit
            group_max += 1

            # Get info and outcomes
            outcomes_here = outcomes.get(eid, {})
            einfo["status"] = outcomes_here.get('status', "unsubmitted")
            einfo["on_time"] = outcomes_here.get('on_time', True)
            einfo["credit"] = outcomes_here.get('credit', None)
            einfo["group_credit"] = outcomes_here.get(
                'group_credit',
                # Backup in case we're dealing with older data
                outcomes_here.get("credit", 0)
            )

            # Accumulate credit across the whole group
            group_credit += einfo["group_credit"] or 0

        # Now that we know the exercise outcomes for each exercise in
        # this group, calculate a group status based on the exercise
        # outcomes and the group phase.
        credit_fraction = group_credit / float(group_max)
        if credit_fraction == 1:
            status = "perfect"
        elif credit_fraction >= usual_config_value(
            "EXERCISE_GROUP_THRESHOLD",
            task_info,
            exercise=group["group"],
            default=0.8
        ):
            status = "complete"
        elif credit_fraction >= usual_config_value(
            "EXERCISE_GROUP_PARTIAL_THRESHOLD",
            task_info,
            exercise=group["group"],
            default=0.4
        ):
            status = "partial"
        else:
            status = "incomplete"

        if (
            phase in ("prerelease", "released")
        and status not in ("perfect", "complete")
        ):
            status = "pending"

        if phase == "prerelease" and group_credit == 0:
            status = "unreleased"

        group["status"] = status
        group["credit_fraction"] = credit_fraction

        # Look up any override and apply it
        override = storage.get_egroup_override(
            course,
            semester,
            username,
            group["group"]
        )
        if override is not None:
            if override["override"]:
                group["credit_fraction"] = override["override"]
            if override["status"]:
                group["status"] = override["status"]
            if isinstance(override["note"], str) and override["note"] != '':
                group["note"] = potluck.render.render_markdown(
                    override["note"]
                )


def set_concept_statuses(concepts, task_info, outcomes):
    """
    Updates the provided concepts list (whose elements are concept
    dictionaries which might have "facets" slots that have sub-concepts
    in them) with status info based on the given (amended) task info and
    exercise outcomes provided. You must call `amend_task_info`,
    `amend_exercises`, and `augment_concepts` before calling this
    function.

    The concepts dictionary is directly augmented so that each concept
    has the following slots:
    - "status" holding an aggregate status string
    - "outcomes" holding a list of relevant outcomes tuples Each outcome
        tuple has an exercise/task-id, a numeric (0-1) outcome value,
        and string ('task', 'exercise', or 'outcome') specifying whether
        it's an individual outcome or an aggregate outcome from a task
        or exercise.
    - "exercises" holding a dictionary mapping exercise IDs to
        phase/status string pairs for exercises which are relevant to
        this concept. The first string represents phase as one of
        "prerelease", "released", or "due" to specify the exercise's
        release status, and the second is one of "complete", "partial",
        "incomplete", or "unsubmitted" to specify the exercise's
        submission status. Exercise IDs won't even be in this list if
        they haven't been submitted yet.
    """

    # Attach outcomes to concepts based on exercise info
    for group in task_info.get("exercises", []):
        phase = group["phase"]

        # Make allowances for old format
        elist = group["exercises"]
        if isinstance(elist, dict):
            for eid in elist:
                elist[eid]['id'] = eid
            elist = list(elist.values())

        # Consider each individual exercise in the group
        for einfo in elist:
            eid = einfo['id']
            # Get info, tag, and outcomes
            etag = "{}:{}".format(group, eid)
            outcomes_here = outcomes.get(eid, {}).get('outcomes', None)

            submission_status = einfo["status"]
            ecredit = einfo["credit"]

            # Note submission status
            einfo["status"] = submission_status

            # First apply binary credit to each concept for per-outcome
            # concepts, and associate per-outcome exercise statuses as
            # well.
            for i, entry in enumerate(einfo.get("per_outcome", [])):
                # Attach individual outcomes to associated per-outcome
                # concepts
                if ecredit is not None:
                    # Replace True/False with 1/0:
                    outcome = outcomes_here[i][:]
                    outcome[0] = 1 if outcome[0] else 0
                    oinfo = (
                        '{}#{}'.format(etag, i),
                        1 if outcome[0] else 0,
                        "outcome"
                    )
                    # Attach outcome
                    attach_outcome(concepts, oinfo, entry)
                    outcome_status = (
                        "complete"
                        if outcome[0]
                        else "incomplete"
                    )
                else:
                    outcome_status = submission_status

                # Note exercise status for these concepts as well, but
                # with success/failure based on individual outcomes
                note_exercise_status(
                    concepts,
                    eid,
                    (phase, outcome_status),
                    entry
                )

            # Now apply the exercise credit as an outcome to each
            # concept that's set at the exercise level, plus apply
            # individual outcomes to their associated per-outcome
            # concepts.
            for concept_path in einfo.get("concepts", []):
                # Note status, potentially overriding per-outcome
                # statuses that have already been attached
                note_exercise_status(
                    concepts,
                    eid,
                    (phase, submission_status),
                    concept_path
                )

                # Attach exercise-level outcome to exercise-level
                # concepts
                if ecredit is not None:
                    try:
                        attach_outcome(
                            concepts,
                            (
                                "exercise@{}".format(etag),
                                ecredit,
                                "exercise"
                            ),
                            concept_path
                        )
                    except ValueError:
                        raise ValueError(
                            (
                                "In group '{}' exercise '{}' references"
                                " concept '{}' but that concept doesn't"
                                " exist."
                            ).format(group['group'], eid, concept_path)
                        )

    # TODO: Attach outcomes from project tasks!

    # Set concept statuses based on attached outcomes
    # TODO: THIS


def all_parents(concepts, concept_path):
    """
    Yields each parent of the given concept path, including the target
    concept itself, in depth-first order and processing each concept
    only once even if parent-loops occur.

    Raises a `ValueError` if the target concept cannot be found.
    """
    concept = lookup_concept(concepts, concept_path.split(':'))
    if concept is None:
        raise ValueError(
            (
                "Couldn't find parents of concept '{}': that concept"
                " does not exist."
            ).format(concept_path)
        )

    # Process all parents using a stack
    seen = set()
    stack = [ concept ]
    while len(stack) > 0:
        this_concept = stack.pop()

        # Skip if we've already processed this concept
        if this_concept["path"] in seen:
            continue

        # If we didn't skip, note that we are going to process it
        seen.add(this_concept["path"])

        # And yield it
        yield this_concept

        # Extend stack to include each non-None parent concept
        stack.extend(
            filter(lambda x: x, this_concept["parents"].values())
        )


def note_exercise_status(concepts, eid, exercise_status, concept_path):
    """
    Requires an augmented concepts network, an exercise ID, an exercise
    status pair (a tuple containing a time status and a submission
    status as strings), and a concept path.

    Adds to the "exercises" slot for the specified concept to include
    the given exercise status under the given exercise ID, overwriting
    any previously-set status.

    Applies to parent concepts as well.

    Flashes a warning if the target concept cannot be found.
    """
    try:
        parents = list(all_parents(concepts, concept_path))
    except ValueError as e:
        flask.flash(
            "Error recording exercise status: {}".format(e)
        )
        parents = []

    for concept in parents:
        concept.setdefault("exercises", {})[eid] = exercise_status


def attach_outcome(concepts, outcome_info, concept_path):
    """
    Requires an augmented concepts network and an outcome info tuple (a
    string naming the outcome plus a number from 0-1 specifying whether
    the outcome indicates success, failure, or some kind of partial
    success).

    Also needs a concept path specifying the concept to which the
    outcome applies. Adds the outcome to the list of outcomes relevant
    to the target concept, plus the lists for each concept that's a
    parent of the target concept.

    Flashes a warning message if the target concept cannot be found.
    """
    try:
        parents = list(all_parents(concepts, concept_path))
    except ValueError as e:
        flask.flash(
            "Error attaching exercise outcome: {}".format(e)
        )
        parents = []

    for concept in parents:
        # Add this outcome to the outcomes list for this concept,
        # creating it if it hasn't already been created.
        concept.setdefault("outcomes", []).append(outcome_info)


def augment_concepts(concepts):
    """
    Takes a concepts list (where each entry is a concept dictionary with
    an 'id', a 'desc', and possibly 'facets' containing a
    sub-concepts-list, OR has just a 'ref' key naming the id-path to a
    different concept). Augments that concepts list by replacing all
    'ref' entries with actual object references to the named concept,
    and by adding the following keys to each non-reference concept:

    - 'path': The full reference path for this concept from a top-level
        concept, using home concepts over other references to find a way
        to the top level.
    - 'parents': a dictionary mapping full-id-path-strings to actual
        concept dictionaries, with one entry for each concept that
        includes this one as a facet. Will be an empty dictionary for
        concepts at the top-level that aren't referenced anywhere. If a
        concept is at the top level or referenced there, this dictionary
        will have a special entry with key `None` and value `None`.
    - 'home': A concept dictionary for the natural parent of this
        concept: the one parent which included it directly instead of as
        a reference. Will be `None` for top-level concepts, including
        ones that are referenced somewhere (to avoid this, you can make
        a reference at the top level and place the concept you want to
        pull up within the place you'd otherwise reference it).

    If something is contradictory (e.g., a named reference concept
    doesn't exist) a `ValueError` will be raised. Note that all
    references must use canonical paths; they cannot 'go through' other
    references.
    """
    # Create a stack for processing the recursive entries. Each concept
    # entry is paired with its natural parent and the index among that
    # parent's facets it exists at.
    stack = [(concept, None, None) for concept in concepts]

    # Continue until we run out of concepts to process
    while len(stack) > 0:
        # Get the concept + parent + index combo to process
        (concept, home, facet_index) = stack.pop()

        # Are we a reference?
        if 'ref' not in concept:
            # Not a reference; augment things & stack up facets

            # Set the home for this concept
            concept['home'] = home

            # Create an empty parents dictionary, or retrieve an
            # existing dictionary (possibly created due to a
            # previously-processed reference)
            parents = concept.setdefault('parents', {})

            # Set path and update parents differently based on whether
            # we're at the top level or not
            if home is None:
                concept['path'] = concept["id"]
                parents[None] = None
            else:
                concept['path'] = home["path"] + ':' + concept["id"]
                parents[home['path']] = home

            for i, facet in enumerate(concept.get('facets', [])):
                stack.append((facet, concept, i))

        else:  # if we *are* a reference...
            referent = lookup_concept(concepts, concept['ref'].split(':'))

            if referent is None:
                raise ValueError(
                    (
                        "At '{}', one facet is a reference to '{}', but"
                        " that concept does not exist. (Note: all"
                        " references must be via canonical paths, i.e.,"
                        " references may not go through other"
                        " references.)"
                    ).format(home['path'], concept['ref'])
                )

            # We need to replace ourselves with a real object reference,
            # unless we're at the top level
            if home is not None:
                home['facets'][facet_index] = referent

                # We also need to update the parents dictionary of the
                # referent to include the parent concept here.
                referent.setdefault('parents', {})[home['path']] = home
            else:
                # Add a 'None' key if this reference is at the top level
                referent.setdefault('parents', {})[None] = None

            # Note that we *don't* add facets to the stack here! They'll
            # be added later after the natural copy of the referent is
            # processed.


def lookup_concept(concepts, concept_names):
    """
    Based on a sequence of concept-name strings, returns the associated
    concept dictionary from the given top-level concepts list. This will
    only be able to find concepts via their natural parents, unless the
    concepts list has been augmented.

    Returns `None` if there is no such concept.
    """
    first = concept_names[0]
    match = None
    for concept in concepts:
        if concept["id"] == first:
            match = concept
            break

    if match is None:
        return None
    elif len(concept_names) == 1:
        return match
    else:
        return lookup_concept(match.get('facets', []), concept_names[1:])


def percentile(dataset, pct):
    """
    Computes the nth percentile of the dataset by a weighted average of
    the two items on either side of that fractional index within the
    dataset. pct must be a number between 0 and 100 (inclusive).

    Returns None when given an empty dataset, and always returns the
    singular item in the dataset when given a dataset of length 1.
    """
    fr = pct / 100.0
    if len(dataset) == 1:
        return dataset[0]
    elif len(dataset) == 0:
        return None
    srt = sorted(dataset)
    fridx = fr * (len(srt) - 1)
    idx = int(fridx)
    if idx == fridx:
        return srt[idx] # integer index -> no averaging
    leftover = fridx - idx
    first = srt[idx]
    second = srt[idx + 1] # legal index because we can't have hit the end
    return first * (1 - leftover) + second * leftover


def get_feedback_pr_and_task(
    task_info,
    course,
    semester,
    user,
    phase,
    prid,
    taskid
):
    """
    Given a task_info object and a particular
    course/semester/user/phase/project/task we're interested in,
    extracts and augments pr and task objects to make them ready for
    rendering as feedback, returning a tuple of both.

    Returns a ValueError object in cases where the requested
    project/task doesn't exist.
    """

    # Extract pr & task objects
    try:
        pr = get_pr_obj(task_info, prid)
    except ValueError as e:
        return e

    try:
        task = get_task_obj(task_info, pr, taskid)
    except ValueError as e:
        return e

    # Add status & time remaining info to project and objects
    amend_project(course, semester, task_info, pr, user)
    amend_task(course, semester, task_info, prid, task, user, phase)

    # Get full feedback for the task in question if it's available
    task["feedback"] = storage.get_feedback(
        course,
        semester,
        task_info,
        user,
        phase,
        pr["id"],
        task["id"]
    )
    # Get HTML feedback as well
    task["feedback_html"] = storage.get_feedback_html(
        course,
        semester,
        task_info,
        user,
        phase,
        pr["id"],
        task["id"]
    )
    if task["feedback"]["status"] != "missing":
        task["submitted"] = True
        potluck.render.augment_report(task["feedback"])

    return pr, task


def get_evaluation_info(
    course,
    semester,
    target_user,
    phase,
    prid,
    taskid
):
    """
    Fetches notes and override info for the given submission, and returns
    a tuple including the notes markdown source, the notes rendered HTML,
    the grade override value, and the timeliness override value.

    The grade override will be an empty string if no override is active,
    and should be a floating-point value otherwise except in cases where
    a non-numeric value was set.

    The timeliness override is similar, and should only ever be set for
    the 'initial' phase, since it applies across all phases.

    The notes and notes HTML strings will be empty strings if no notes
    have been set.
    """
    # Fetch raw eval info dict
    evaluation = storage.fetch_evaluation(
        course,
        semester,
        target_user,
        phase,
        prid,
        taskid
    )

    if evaluation is None:
        return '', '', '', ''

    # Extract notes and grade override from stored info
    notes = evaluation.get("notes", "")
    override = evaluation.get("override")
    if override is None:
        override = ""
    else:
        try:
            override = float(override)
        except Exception:
            pass

    timeliness = evaluation.get("timeliness")
    if timeliness is None:
        timeliness = ""
    else:
        try:
            timeliness = float(timeliness)
        except Exception:
            pass

    # Render notes as HTML
    notes_html = potluck.render.render_markdown(notes)

    return notes, notes_html, override, timeliness


#----------------#
# Time functions #
#----------------#

ONE_MINUTE = 60
ONE_HOUR = ONE_MINUTE * 60
ONE_DAY = ONE_HOUR * 24
ONE_WEEK = ONE_DAY * 7


def project_status_now(
    username,
    task_info,
    project_obj,
    extensions=(False, False)
):
    """
    Returns the current state of the given project object (also needs
    the task info object and the username). If "PAUSE_AT" is set in the
    task object and non-empty (see set_pause_time), that moment, not the
    current time, will be used. Extensions must contain two values (one
    for the initial phase and one for the revision phase). They may each
    be False for no extension, True for the default extension, or an
    integer number of hours. Those hours will be added to the effective
    initial and revision deadlines.

    Returns a dictionary with 'state', 'initial-extension',
    'revision-extension', 'release', 'due', 'reviewed', and 'finalized',
    keys. Each of the 'release', 'due', 'reviewed', and 'finalized' keys
    will be a sub-dictionary with the following keys:

    - 'at': A dateimte.datetime object specifying absolute timing.
    - 'at_str': A string representation of the above.
    - 'until': A datetime.timedelta representing time until the event (will
        be negative afterwards).
    - 'until_str': A string representation of the above.

    Each of the sub-values will be none if the project doesn't have a
    deadline set.

    The 'state' value will be one of:

    - "unreleased": This project hasn't yet been released; don't display
        any info about it.
    - "released": This project has been released and isn't due yet.
    - "under_review": This project's due time has passed, but the feedback
        review period hasn't expired yet.
    - "revisable": This project's due time is past, and the review period has
        expired, so full feedback should be released, but revisions may
        still be submitted.
    - "final": This project's due time is past, the review period has
        expired, and the revision period is also over, so full feedback
        is available, and no more submissions will be accepted.
    - "unknown": This project doesn't have a due date. The
        seconds_remaining value will be None.

    The 'initial_extension' and 'revision_extension' will both be numbers
    specifying how many hours of extension were granted (these numbers
    are already factored into the deadline information the status
    contains). These numbers will be 0 for students who don't have
    extensions.
    """
    # Get extension/revision durations and grace period from task info:
    standard_ext_hrs = task_info.get("extension_hours", 24)
    review_hours = task_info.get("review_hours", 24)
    grace_mins = task_info.get("grace_minutes", 0)
    revision_hours = task_info.get("revision_hours", 72)

    # Get project-specific review/grace/revision info if it exists
    review_hours = project_obj.get("review_hours", review_hours)
    grace_mins = project_obj.get("grace_minutes", grace_mins)
    revision_hours = project_obj.get("revision_hours", revision_hours)

    # Figure out extension amounts
    initial_extension = 0
    if extensions[0] is True:
        initial_extension = standard_ext_hrs
    elif isinstance(extensions[0], (int, float)):
        initial_extension = extensions[0]
    elif extensions[0] is not False:
        flask.flash(
            "Ignoring invalid initial extension value '{}'".format(
                extensions[0]
            )
        )

    revision_extension = 0
    if extensions[1] is True:
        revision_extension = standard_ext_hrs
    elif isinstance(extensions[1], (int, float)):
        revision_extension = extensions[1]
    elif extensions[1] is not False:
        flask.flash(
            "Ignoring invalid revision extension value '{}'".format(
                extensions[1]
            )
        )

    # The default result
    result = {
        'state': "unknown",
        'release': {
            'at': None,
            'at_str': 'unknown',
            'until': None,
            'until_str': 'at some point (not yet specified)'
        },
        'due': {
            'at': None,
            'at_str': 'unknown',
            'until': None,
            'until_str': 'at some point (not yet specified)'
        },
        'reviewed': {
            'at': None,
            'at_str': 'unknown',
            'until': None,
            'until_str': 'at some point (not yet specified)'
        },
        'finalized': {
            'at': None,
            'at_str': 'unknown',
            'until': None,
            'until_str': 'at some point (not yet specified)'
        },
        'initial_extension': 0,
        'revision_extension': 0,
    }

    # Save extension info
    result['initial_extension'] = initial_extension or 0
    result['revision_extension'] = revision_extension or 0

    # Get current time:
    if "PAUSE_AT" in task_info and task_info["PAUSE_AT"]:
        now = potluck.time_utils.task_time__time(
            task_info,
            task_info["PAUSE_AT"]
        )
    else:
        now = potluck.time_utils.now()

    # Get release date/time:
    release_at = project_obj.get("release", None)
    # if None, we assume release
    if release_at is not None:
        release_at = potluck.time_utils.task_time__time(
            task_info,
            release_at,
            default_time_of_day=task_info.get(
                "default_release_time_of_day",
                "23:59"
            )
        )
        # Fill in release info
        result['release']['at'] = release_at
        result['release']['at_str'] = potluck.time_utils.fmt_datetime(
            release_at
        )
        until_release = release_at - now
        result['release']['until'] = until_release
        result['release']['until_str'] = fuzzy_time(
            until_release.total_seconds()
        )

    # Get due date/time:
    due_at = project_obj.get("due", None)
    if due_at is None:
        # Return empty result
        return result
    else:
        due_at = potluck.time_utils.task_time__time(
            task_info,
            due_at,
            default_time_of_day=task_info.get(
                "default_due_time_of_day",
                "23:59"
            )
        )
        review_end = due_at + datetime.timedelta(hours=review_hours)

    due_string = potluck.time_utils.fmt_datetime(due_at)

    base_deadline = due_at

    # Add extension hours:
    if initial_extension > 0:
        due_at += datetime.timedelta(hours=initial_extension)
        due_string = potluck.time_utils.fmt_datetime(due_at) + (
            ' <span class="extension_taken">'
          + '(after accounting for your {}‑hour extension)'
          + '</span>'
        ).format(initial_extension)

    grace_deadline = due_at + datetime.timedelta(minutes=grace_mins)

    # Fill in due info
    result['due']['at'] = due_at
    result['due']['at_str'] = due_string
    until_due = due_at - now
    result['due']['until'] = until_due
    result['due']['until_str'] = fuzzy_time(until_due.total_seconds())

    # Fill in review info
    result['reviewed']['at'] = review_end
    result['reviewed']['at_str'] = potluck.time_utils.fmt_datetime(
        review_end
    )
    until_reviewed = review_end - now
    result['reviewed']['until'] = until_reviewed
    result['reviewed']['until_str'] = fuzzy_time(
        until_reviewed.total_seconds()
    )

    # Get final date/time:
    # Note: any extension to the initial deadline is ignored. A separate
    # revision extension should be issued when an initial extension eats
    # up too much of the revision period.
    final_at = base_deadline + datetime.timedelta(
        hours=review_hours + revision_hours
    )

    final_string = potluck.time_utils.fmt_datetime(final_at)

    # Add extension hours:
    if revision_extension > 0:
        final_at += datetime.timedelta(hours=revision_extension)
        final_string = potluck.time_utils.fmt_datetime(final_at) + (
            ' <span class="extension_taken">'
          + '(after accounting for your {}‑hour extension)'
          + '</span>'
        ).format(revision_extension)

    grace_final = final_at + datetime.timedelta(minutes=grace_mins)

    # Fill in finalization info
    result['finalized']['at'] = final_at
    result['finalized']['at_str'] = final_string
    until_final = final_at - now
    result['finalized']['until'] = until_final
    result['finalized']['until_str'] = fuzzy_time(until_final.total_seconds())

    # Check release time:
    if release_at and now < release_at:
        result['state'] = "unreleased"
    # Passed release_at point: check if it's due or not
    elif now < grace_deadline:
        # Note time-remaining ignores grace period and may be negative
        result['state'] = "released"
    # Passed due_at point; check if it's still under review:
    elif now < review_end:
        result['state'] = "under_review"
    # Passed review period: are revisions still being accepted?
    elif now < grace_final:
        result['state'] = "revisable"
    # Passed review period: it's final
    else:
        result['state'] = "final"

    return result


#--------------------#
# Filename functions #
#--------------------#

def get_submission_filename(
    course,
    semester,
    task_info,
    username,
    phase,
    prid,
    taskid
):
    """
    Returns the filename for the user's submission for a given
    phase/project/task. Raises a ValueError if the project or task
    doesn't exit.

    TODO: Do we just do zip files for multi-file tasks? How is that
    handled?
    """
    pr = get_pr_obj(task_info, prid)
    task = get_task_obj(task_info, pr, taskid)

    return safe_join(
        storage.submissions_folder(course, semester),
        username,
        "{}_{}_{}".format(
            prid,
            phase,
            task["target"]
        )
    )


#---------------#
# Jinja support #
#---------------#

_sorted = sorted


@app.template_filter()
def sorted(*args, **kwargs):
    """
    Turn builtin sorted into a template filter...
    """
    return _sorted(*args, **kwargs)


@app.template_filter()
def fuzzy_time(seconds):
    """
    Takes a number of seconds and returns a fuzzy time value that shifts
    units (up to weeks) depending on how many seconds there are. Ignores
    the sign of the value.
    """
    if seconds < 0:
        seconds = -seconds

    weeks = seconds / ONE_WEEK
    seconds %= ONE_WEEK
    days = seconds / ONE_DAY
    seconds %= ONE_DAY
    hours = seconds / ONE_HOUR
    seconds %= ONE_HOUR
    minutes = seconds / ONE_MINUTE
    seconds %= ONE_MINUTE
    if int(weeks) > 1:
        if weeks % 1 > 0.75:
            return "almost {:.0f} weeks".format(weeks + 1)
        else:
            return "{:.0f} weeks".format(weeks)
    elif int(weeks) == 1:
        return "{:.0f} days".format(7 + days)
    elif int(days) > 1:
        if days % 1 > 0.75:
            return "almost {:.0f} days".format(days + 1)
        else:
            return "{:.0f} days".format(days)
    elif int(days) == 1:
        return "{:.0f} hours".format(24 + hours)
    elif hours > 4:
        if hours % 1 > 0.75:
            return "almost {:.0f} hours".format(hours + 1)
        else:
            return "{:.0f} hours".format(hours)
    elif int(hours) > 0:
        return "{:.0f}h {:.0f}m".format(hours, minutes)
    elif minutes > 30:
        return "{:.0f} minutes".format(minutes)
    else:
        return "{:.0f}m {:.0f}s".format(minutes, seconds)


@app.template_filter()
def timestamp(value):
    """
    A filter to display a timestamp.
    """
    dt = potluck.time_utils.time_from_timestring(value)
    return potluck.time_utils.fmt_datetime(dt)


@app.template_filter()
def seconds(timedelta):
    """
    Converts a timedelta to a floating-point number of seconds.
    """
    return timedelta.total_seconds()


@app.template_filter()
def integer(value):
    """
    A filter to display a number as an integer.
    """
    if isinstance(value, (float, int)):
        return str(round(value))
    else:
        return str(value)


app.add_template_global(min, name='min')
app.add_template_global(max, name='max')
app.add_template_global(round, name='round')
app.add_template_global(sum, name='sum')
app.add_template_global(enumerate, name='enumerate')
app.add_template_global(potluck.time_utils.now, name='now')

# Custom filename->slug filter from potluck
app.template_filter()(potluck.html_tools.fileslug)

# Time filters from potluck
app.template_filter()(potluck.time_utils.fmt_datetime)


@app.template_filter()
def a_an(h):
    """
    Returns the string 'a' or 'an' where the use of 'a/an' depends on the
    first letter of the name of the first digit of the given number, or
    the first letter of the given string.

    Can't handle everything because it doesn't know phonetics (e.g., 'a
    hour' not 'an hour' because 'h' is not a vowel).
    """
    digits = str(h)
    fd = digits[0]
    if fd in "18aeiou":
        return 'an'
    else:
        return 'a'


@app.template_filter()
def project_combined_grade(project, task_info=None):
    """
    Extracts a full combined grade value from a project object. Respects
    task weights; fills in zeroes for any missing grades, and grabs the
    highest score from each task pool. Includes timeliness points along
    with task grades, re-normalizing to be out of the `SCORE_BASIS`.

    If `task_info` is provided a `SCORE_BASIS` default may be picked up
    from there if the project doesn't define one. If not, only the app
    global config can define `SCORE_BASIS` if one isn't specified within
    the project itself.
    """
    pool_scores = {}
    for task in project["tasks"]:
        # Get a grade & weight
        cg = task_combined_grade(task, task_info)
        tp = task_timeliness_points(task, task_info)
        tw = task.get("weight", 1)
        if cg is None:
            cg = 0

        new_score = float(cg + tp)  # float just in case...

        # Figure out this task's pool and update the score for that pool
        pool = task_pool(task)
        if pool in pool_scores:
            old_score, old_weight = pool_scores[pool]
            if old_weight != tw:
                raise ValueError("Inconsistent weights for pooled tasks!")
            if old_score < new_score:
                pool_scores[pool] = [new_score, tw]
        else:
            pool_scores[pool] = [new_score, tw]

    score_basis = fallback_config_value(
        "SCORE_BASIS",
        project,
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    max_score = score_basis + fallback_config_value(
        "TIMELINESS_POINTS",
        project,
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    weighted_score = sum(
        (grade / float(max_score)) * weight
        for grade, weight in pool_scores.values()
    )
    total_weight = sum(weight for grade, weight in pool_scores.values())

    return score_basis * weighted_score / float(total_weight)


@app.template_filter()
def uses_pools(project):
    """
    Returns True if the project has at least two tasks that are in the same
    pool, and False otherwise.
    """
    pools = set(task_pool(task) for task in project["tasks"])
    return len(pools) < len(project["tasks"])


@app.template_filter()
def task_pool(task):
    """
    Grabs the pool for a task, which defaults to the task ID.
    """
    return task.get("pool", task["id"])


@app.template_filter()
def project_pools(project):
    """
    Returns a list of pairs, each containing a pool ID and a colspan
    integer for that pool.
    """
    seen = set()
    result = []
    for task in project["tasks"]:
        pool = task_pool(task)
        if pool in seen:
            continue
        else:
            seen.add(pool)
            result.append((pool, pool_colspan(project, task["id"])))
    return result


@app.template_filter()
def pool_colspan(project, taskid):
    """
    Returns the column span for the pool of the given task in the given
    project, assuming that the tasks of the project are displayed in order.
    """
    start_at = None
    this_task = None
    for i in range(len(project["tasks"])):
        if project["tasks"][i]["id"] == taskid:
            start_at = i
            this_task = project["tasks"][i]
            break

    if start_at is None:
        raise ValueError(
            "Pset '{}' does not contain a task '{}'.".format(
                project["id"],
                taskid
            )
        )

    this_pool = task_pool(this_task)
    span = 1
    for task in project["tasks"][i + 1:]:
        if task_pool(task) == this_pool:
            span += 1
        else:
            break # span is over

    return span


@app.template_filter()
def task_combined_grade(task, task_info=None):
    """
    Extracts the combined grade value between initial/revised/belated
    submissions for the given task. Returns a point number, or None if
    there is not enough information to establish a grade.

    Timeliness points are not included (see `task_timeliness_points`).

    If `task_info` is provided, then defaults for things like the score
    basis or revision score limits may be pulled from that, but otherwise
    either the task itself or the app config determine these.
    """
    base_grade = task.get("grade")
    options = []
    if base_grade is not None and base_grade != "?":
        options.append(float(base_grade))

    rev_task = task.get("revision", {})
    rev_grade = rev_task.get("grade")
    if isinstance(rev_grade, (int, float)):
        rmax = fallback_config_value(
            "REVISION_MAX_SCORE",
            task,
            task_info or {},
            app.config,
            DEFAULT_CONFIG
        )
        if rmax is NotFound:
            rmax = fallback_config_value(
                "SCORE_BASIS",
                task,
                task_info or {},
                app.config,
                DEFAULT_CONFIG
            )
            if rmax is NotFound:
                rmax = 100
        options.append(min(rev_grade, rev_task.get("max_score", rmax)))

    belated_task = task.get("belated", {})
    belated_grade = belated_task.get("grade")
    if isinstance(belated_grade, (int, float)):
        bmax = fallback_config_value(
            "BELATED_MAX_SCORE",
            task,
            task_info or {},
            app.config,
            DEFAULT_CONFIG
        )
        if bmax is NotFound:
            bmax = fallback_config_value(
                "SCORE_BASIS",
                task,
                task_info or {},
                app.config,
                DEFAULT_CONFIG
            )
            if bmax is NotFound:
                bmax = 100
        options.append(
            min(belated_grade, belated_task.get("max_score", bmax))
        )

    if len(options) > 0:
        return max(options)
    else:
        return None


@app.template_filter()
def task_timeliness_points(task, task_info=None):
    """
    Returns a number indicating how many timeliness points were earned
    for submissions to the given task. The `TIMELINESS_POINTS` value
    determines how many points are available in total; half of these are
    awarded if a submission is made by the initial deadline which earns
    at least `TIMELINESS_ATTEMPT_THRESHOLD` points, and the other half
    are earned if a submission is made by the revision deadline which
    earns at least `TIMELINESS_COMPLETE_THRESHOLD` points.

    Config values are pulled from the provided `task_info` object if
    there is one; otherwise they come from the task itself or from the
    app-wide config, with the `DEFAULT_CONFIG` as a final backup.

    A manual override may also have been provided, and is used if so.

    TODO: This really needs to be upgraded at some point to respect the
    best submission in each phase, rather than just the latest. Students
    who accidentally downgrade their evaluation may lose timeliness
    points that they really should have earned!
    """
    earned = 0
    available = fallback_config_value(
        "TIMELINESS_POINTS",
        task,
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    timely_attempt_threshold = fallback_config_value(
        "TIMELINESS_ATTEMPT_THRESHOLD",
        task,
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if timely_attempt_threshold is NotFound:
        timely_attempt_threshold = fallback_config_value(
            ["EVALUATION_SCORES", "partially complete"],
            task,
            task_info or {},
            app.config,
            DEFAULT_CONFIG
        )
        if timely_attempt_threshold is NotFound:
            timely_attempt_threshold = 75
    completion_threshold = fallback_config_value(
        "TIMELINESS_COMPLETE_THRESHOLD",
        task,
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if timely_attempt_threshold is NotFound:
        timely_attempt_threshold = fallback_config_value(
            ["EVALUATION_SCORES", "almost complete"],
            task,
            task_info or {},
            app.config,
            DEFAULT_CONFIG
        )
        if timely_attempt_threshold is NotFound:
            timely_attempt_threshold = 85

    if available is NotFound:
        available = 0
    attempt_points = available / 2
    if attempt_points == 0:
        attempt_points = available / 2.0
    completion_points = available - attempt_points

    if task.get("timeliness_overridden") and "timeliness" in task:
        return task["timeliness"]

    initial_grade = task.get("grade")
    if initial_grade == "?":
        initial_grade = None
    elif initial_grade is not None:
        initial_grade = float(initial_grade)
        if initial_grade >= timely_attempt_threshold:
            earned += attempt_points

    rev_task = task.get("revision")
    has_rev_grade = (
        rev_task
    and "grade" in rev_task
    and rev_task["grade"] not in (None, "?")
    )

    if (
        (initial_grade is not None and initial_grade >= completion_threshold)
     or (has_rev_grade and float(rev_task["grade"]) >= completion_threshold)
    ):
        earned += completion_points

    return earned


@app.template_filter()
def ex_combined_grade(egroup, task_info=None):
    """
    Extracts a full combined grade value from an amended exercise group
    object. Uses the pre-calculated credit-fraction and adds bonus
    points for reaching partial/complete thresholds.

    Scores are not rounded (use `grade_string` or the like).

    Config values are taken from the given `task_info` object as a backup
    to values in the exercise group itself if one is provided. Otherwise
    only the app config and `DEFAULT_CONFIG` may specify them.
    """
    fraction = egroup["credit_fraction"]

    # free credit bump for hitting each threshold
    bump = fallback_config_value(
        "EXERCISE_GROUP_CREDIT_BUMP",
        egroup,
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if bump is NotFound:
        bump = 0.1

    partial_threshold = fallback_config_value(
        "EXERCISE_GROUP_PARTIAL_THRESHOLD",
        egroup,
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if partial_threshold is NotFound:
        partial_threshold = 0.395

    full_threshold = fallback_config_value(
        "EXERCISE_GROUP_THRESHOLD",
        egroup,
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if full_threshold is NotFound:
        full_threshold = 0.795

    score_basis = fallback_config_value(
        "SCORE_BASIS",
        egroup,
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if score_basis is NotFound:
        score_basis = 100

    if fraction >= partial_threshold:
        fraction += bump
    if fraction >= full_threshold:
        fraction += bump

    # no extra credit
    return min(score_basis, score_basis * fraction)


@app.template_filter()
def grade_string(grade_value, task_info=None, local_info=None):
    """
    Turns a grade value (None, or a number) into a grade string (an HTML
    string w/ a denominator, or 'unknown'). The rounding preference and
    score basis are pulled from the given `task_info` object, or if a
    `local_info` object is provided comes from there preferentially. If
    neither is available, it will pull from the app config or the
    `DEFAULT_CONFIG` values.
    """
    basis = fallback_config_value(
        "SCORE_BASIS",
        local_info or {},
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if basis is NotFound:
        basis = 100

    round_to = fallback_config_value(
        "ROUND_SCORES_TO",
        local_info or {},
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if round_to is NotFound:
        round_to = 1

    if grade_value is None or not isinstance(grade_value, (int, float)):
        return "unknown"
    else:
        rounded = round(grade_value, round_to)
        rdenom = round(basis, round_to)
        if int(rounded) == rounded:
            rounded = int(rounded)
        if int(rdenom) == rdenom:
            rdenom = int(rdenom)
        return "{}&nbsp;/&nbsp;{}".format(rounded, rdenom)


@app.template_filter()
def timeliness_string(grade_value, task_info=None, local_info=None):
    """
    Turns a timeliness points value (None, or a number) into a timeliness
    grade string (an HTML string w/ a denominator, or 'unknown').

    As with `grade_string`, config values are pulled from the given local
    and/or task info if provided.
    """
    timeliness_points = fallback_config_value(
        "TIMELINESS_POINTS",
        local_info or {},
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if timeliness_points is NotFound:
        timeliness_points = 0

    round_to = fallback_config_value(
        "ROUND_SCORES_TO",
        local_info or {},
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if round_to is NotFound:
        round_to = 1

    if grade_value is None or not isinstance(grade_value, (int, float)):
        return "unknown"
    else:
        rounded = round(grade_value, round_to)
        rdenom = round(timeliness_points, round_to)
        if int(rounded) == rounded:
            rounded = int(rounded)
        if int(rdenom) == rdenom:
            rdenom = int(rdenom)
        return "{}&nbsp;/&nbsp;{}".format(rounded, rdenom)


@app.template_filter()
def shorter_grade(grade_string):
    """
    Shortens a grade string.
    """
    divis = "&nbsp;/&nbsp;"
    if divis in grade_string:
        return grade_string[:grade_string.index(divis)]
    elif grade_string == "unknown":
        return "?"
    else:
        return "!"


@app.template_filter()
def grade_category(grade_value, task_info=None, local_info=None):
    """
    Categorizes a grade value (0-100 or None).

    As with `grade_string`, config values are pulled from the given local
    and/or task info if provided.
    """
    low_threshold = fallback_config_value(
        ["GRADE_THRESHOLDS", "low"],
        local_info or {},
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if low_threshold is NotFound:
        low_threshold = 75

    mid_threshold = fallback_config_value(
        ["GRADE_THRESHOLDS", "mid"],
        local_info or {},
        task_info or {},
        app.config,
        DEFAULT_CONFIG
    )
    if mid_threshold is NotFound:
        mid_threshold = 90

    if grade_value is None:
        return "missing"
    elif grade_value < low_threshold:
        return "low"
    elif grade_value < mid_threshold:
        return "mid"
    else:
        return "high"


@app.template_filter()
def timespent(time_spent):
    """
    Handles numerical-or-string-or-None time spent values.
    """
    if isinstance(time_spent, (int, float)):
        if time_spent == 0:
            return '-'
        elif int(time_spent) == time_spent:
            return "{}h".format(int(time_spent))
        else:
            return "{}h".format(round(time_spent, 2))
    elif isinstance(time_spent, str):
        return time_spent
    else:
        return "?"


@app.template_filter()
def initials(full_section_title):
    """
    Reduces a full section title potentially including time information
    and the word 'Prof.' or 'Professor' to just first initials.

    Returns '?' if the input value is `None`.
    """
    if full_section_title is None:
        return '?'
    words = full_section_title.split()
    if len(words) > 1:
        if words[0] in ('Prof', 'Prof.', 'Professor'):
            words.pop(0)
        return words[0][0] + words[1][0]
    else:
        return full_section_title


@app.template_filter()
def pronoun(pronouns):
    """
    Reduces pronoun info to a single pronoun.
    """
    test = '/'.join(re.split(r"[^A-Za-z]+", pronouns.lower()))
    if test in (
        "she",
        "she/her",
        "she/hers",
        "she/her/hers"
    ):
        return "she"
    elif test in (
        "he",
        "he/him",
        "he/his",
        "he/him/his"
    ):
        return "he"
    elif test in (
        "they",
        "they/them",
        "them/them/their"
    ):
        return "they"
    else:
        return pronouns


# Characters that need replacing to avoid breaking strings in JS script
# tags
_JS_ESCAPES = [ # all characters with ord() < 32
    chr(z) for z in range(32)
] + [
    '\\',
    "'",
    '"',
    '>',
    '<',
    '&',
    '=',
    '-',
    ';',
    u'\u2028', # LINE_SEPARATOR
    u'\u2029', # PARAGRAPH_SEPARATOR
]


@app.template_filter()
def escapejs(value):
    """
    Modified from:

    https://stackoverflow.com/questions/12339806/escape-strings-for-javascript-using-jinja2

    Escapes string values so that they can appear inside of quotes in a
    &lt;script&gt; tag and they won't end the quotes or cause any other
    trouble.
    """
    retval = []
    for char in value:
        if char in _JS_ESCAPES:
            retval.append(r'\u{:04X}'.format(ord(char)))
        else:
            retval.append(char)

    return jinja2.Markup(u"".join(retval))


#-----------#
# Main code #
#-----------#

if __name__ == "__main__":
    use_ssl = True
    if app.config.get("NO_DEBUG_SSL"):
        use_ssl = False
    else:
        try:
            import OpenSSL # noqa F811, F401
        except ModuleNotFound_or_Import_Error:
            use_ssl = False

    if use_ssl:
        # Run with an ad-hoc SSL context since OpenSSL is available
        print("Running with self-signed SSL.")
        app.run('localhost', 8787, debug=False, ssl_context='adhoc')
    else:
        # Run without an SSL context (No OpenSSL)
        print("Running without SSL.")
        app.run('localhost', 8787, debug=False)
        # Note: can't enable debugging because it doesn't set __package__
        # when restarting and so relative imports break in 3.x
