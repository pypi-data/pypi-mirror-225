"""
Successor to sync; this is advanced synchronization & caching for Flask
apps, using Redis.

storage.py
"""

# Attempts at 2/3 dual compatibility:
from __future__ import print_function

__version__ = "0.3.2"

import sys, os, shutil, subprocess, threading, copy
import time, datetime
import base64, csv
import shlex

from flask import json

import flask, redis, bs4, werkzeug

import potluck.time_utils, potluck.html_tools, potluck.render


# Python 2/3 dual compatibility
if sys.version_info[0] < 3:
    reload(sys) # noqa F821
    sys.setdefaultencoding('utf-8')
    import socket
    ConnectionRefusedError = socket.error
    IOError_or_FileNotFoundError = IOError
    OSError_or_FileNotFoundError = OSError
else:
    IOError_or_FileNotFoundError = FileNotFoundError
    OSError_or_FileNotFoundError = FileNotFoundError


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

#-----------#
# Constants #
#-----------#

SCHEMA_VERSION = "1"
"""
The version for the schema used to organize information under keys in
Redis. If this changes, all Redis keys will change.
"""


#-----------#
# Utilities #
#-----------#

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


#--------------------#
# Filename functions #
#--------------------#

def unused_filename(target):
    """
    Checks whether the target already exists, and if it does, appends _N
    before the file extension, where N is the smallest positive integer
    such that the returned filename is not the name of an existing file.
    If the target does not exists, returns it.
    """
    n = 1
    backup = target
    base, ext = os.path.splitext(target)
    while os.path.exists(backup):
        backup = base + "_" + str(n) + ext
        n += 1

    return backup


def make_way_for(target):
    """
    Given that we're about to overwrite the given file, this function
    moves any existing file to a backup first, numbering backups starting
    with _1. The most-recent backup will have the largest backup number.

    After calling this function, the given target file will not exist,
    and so new material can be safely written there.
    """
    backup = unused_filename(target)
    if backup != target:
        shutil.move(target, backup)


def evaluation_directory(course, semester):
    """
    The evaluation directory for a particular class/semester.
    """
    return os.path.join(
        _EVAL_BASE,
        course,
        semester
    )


def logs_folder(course, semester, username):
    """
    The logs folder for a class/semester/user.
    """
    return safe_join(
        evaluation_directory(course, semester),
        "logs",
        username
    )


def reports_folder(course, semester, username):
    """
    The reports folder for a class/semester/user.
    """
    return safe_join(
        evaluation_directory(course, semester),
        "reports",
        username
    )


def submissions_folder(course, semester):
    """
    The submissions folder for a class/semester.
    """
    return os.path.join(
        evaluation_directory(course, semester),
        "submissions"
    )


def admin_info_file(course, semester):
    """
    The admin info file for a class/semester.
    """
    return os.path.join(
        evaluation_directory(course, semester),
        _CONFIG["ADMIN_INFO_FILE"]
    )


def task_info_file(course, semester):
    """
    The task info file for a class/semester.
    """
    return os.path.join(
        evaluation_directory(course, semester),
        _CONFIG.get("TASK_INFO_FILE", "tasks.json")
    )


def concepts_file(course, semester):
    """
    The concepts file for a class/semester.
    """
    return os.path.join(
        evaluation_directory(course, semester),
        _CONFIG.get("CONCEPTS_FILE", "pl_concepts.json")
    )


def roster_file(course, semester):
    """
    The roster file for a class/semester.
    """
    return os.path.join(
        evaluation_directory(course, semester),
        _CONFIG["ROSTER_FILE"]
    )


def student_info_file(course, semester):
    """
    The student info file for a class/semester.
    """
    return os.path.join(
        evaluation_directory(course, semester),
        _CONFIG["STUDENT_INFO_FILE"]
    )


#---------------------#
# Redis key functions #
#---------------------#

def redis_key(suffix):
    """
    Given a key suffix, returns a full Redis key which includes
    "potluck:<version>" where version is the schema version (see
    `SCHEMA_VERSION`).
    """
    return "potluck:" + SCHEMA_VERSION + ":" + suffix


def redis_key_suffix(key):
    """
    Returns the part of a Redis key that wasn't added by the `redis_key`
    function.
    """
    return key[len(redis_key("")):]


def inflight_key(course, semester, username, project, task, phase):
    """
    The in-flight key for a class/semester/user/project/task/phase.
    """
    return redis_key(
        ':'.join(
            [
                course,
                semester,
                "inflight",
                username,
                project,
                task,
                phase
            ]
        )
    )


def extension_key(course, semester, username, project, phase):
    """
    The Redis key for the extension for a
    class/semester/user/project/phase.
    """
    return redis_key(
        ':'.join([course, semester, "ext", username, project, phase])
    )


def time_spent_key(course, semester, username, project, phase, task):
    """
    The Redis key for the time-spent info for a
    class/semester/user/project/phase/task.
    """
    return redis_key(
        ':'.join(
            [course, semester, "spent", username, project, phase, task]
        )
    )


def evaluation_key(course, semester, username, project, phase, task):
    """
    The Redis key for the custom evaluation info for a
    class/semester/user/project/phase/task.
    """
    return redis_key(
        ':'.join(
            [course, semester, "eval", username, project, phase, task]
        )
    )


def egroup_override_key(course, semester, username, egroup):
    """
    The Redis key for the grade override info for a
    class/semester/user/egroup
    """
    return redis_key(
        ':'.join(
            [course, semester, "egover", username, egroup]
        )
    )


def old_exercise_key(course, semester, username, exercise):
    """
    Old-format exercises key.
    """
    return redis_key(
        ':'.join(
            [course, semester, "outcomes", username, exercise]
        )
    )


def exercise_key(course, semester, username, exercise, category):
    """
    The Redis key for the outcomes-list-history for a particular
    exercise, submitted by a user for a particular course/semester.
    These are further split by category: no-credit, partial-credit, and
    full-credit exercises are stored in different history lists.
    """
    return redis_key(
        ':'.join(
            [course, semester, "outcomes", username, exercise, category]
        )
    )


#----------------#
# Roster loading #
#----------------#

def get_variable_field_value(titles, row, name_options):
    """
    Extracts info from a CSV row that might be found in different columns
    (or combinations of columns).

    Needs a list of column titles (lowercased strings), plus a name
    options list, and the row to extract from. Each item in the name
    options list is either a string (column name in lowercase), or a
    tuple containing one or more strings followed by a function to be
    called with the values of those columns as arguments whose result
    will be used as the value.

    Returns the value from the row as extracted by the extraction
    function, or simply looked up in the case of a string entry. Tries
    options from the first to the last and returns the value from the
    first one that worked.
    """
    obj = {}
    val = obj
    for opt in name_options:
        if isinstance(opt, str):
            try:
                val = row[titles.index(opt)]
            except ValueError:
                continue
        else:
            try:
                args = [row[titles.index(name)] for name in opt[:-1]]
            except ValueError:
                continue
            val = opt[-1](*args)

        if val is not obj:
            return val

    optitems = [
        "'" + opt + "'"
            if isinstance(opt, str)
            else ' & '.join(["'" + o + "'" for o in opt[:-1]])
        for opt in name_options
    ]
    if len(optitems) == 1:
        optsummary = optitems[0]
    elif len(optitems) == 2:
        optsummary = optitems[0] + " or " + optitems[1]
    else:
        optsummary = ', '.join(optitems[:-1]) + ", or " + optitems[-1]
    raise ValueError(
        "Roster does not have column(s) {}. Columns are:\n  {}".format(
            optsummary,
            '\n  '.join(titles)
        )
    )


def load_roster_from_stream(iterable_of_strings):
    """
    Implements the roster-loading logic given an iterable of strings,
    like an open file or a list of strings. See `AsRoster`.

    Each entry in the dictionary it returns has the following keys:

    - 'username': The student's username
    - 'fullname': The student's full name (as it appears in the roster
        file, so not always what they want to go by).
    - 'sortname': A version of their name with 'last' name first that is
        used to sort students.
    - 'course_section': Which section the student is in.
    """
    reader = csv.reader(iterable_of_strings)

    students = {}
    # [2018/09/16, lyn] Change to handle roster with titles
    # [2019/09/13, Peter] Change to use standard Registrar roster columns
    # by default
    titles = next(reader) # Read first title line of roster
    titles = [x.lower() for x in titles] # convert columns to lower-case

    if "sort name" in titles:
        sortnameIndex = titles.index('sort name')
    elif "sortname" in titles:
        sortnameIndex = titles.index('sortname')
    else:
        sortnameIndex = None

    for row in reader:
        username = get_variable_field_value(
            titles,
            row,
            [
                ('email', lambda e: e.split('@')[0]),
                'username'
            ]
        )
        if 0 < len(username):
            name = get_variable_field_value(
                titles,
                row,
                [
                    'name', 'student name',
                    ('first', 'last', lambda fi, la: fi + ' ' + la),
                    'sort name'
                ]
            )
            section = get_variable_field_value(
                titles,
                row,
                [
                    'section',
                    'lecture section',
                    'lec',
                    'lec sec',
                    'lec section',
                    'course_title',
                ]
            )
            namebits = name.split()
            if sortnameIndex is not None:
                sort_by = row[sortnameIndex]
            else:
                sort_by = ' '.join(
                    [section, namebits[-1]]
                    + namebits[:-1]
                )
            students[username] = {
                'username': username,
                'fullname': name,
                'sortname': sort_by,
                'course_section': section
            }
        pass
    pass
    return students


#-------------------------#
# Info fetching functions #
#-------------------------#

def get_task_info(course, semester):
    """
    Loads the task info from the JSON file (or returns a cached version
    if the file hasn't been modified since we last loaded it). Needs the
    course and semester to load info for.

    Returns None if the file doesn't exist or can't be parsed.

    Pset and task URLs are added to the information loaded.
    """
    filename = task_info_file(course, semester)
    try:
        result = load_or_get_cached(
            filename,
            assume_fresh=_CONFIG.get("ASSUME_FRESH", 1)
        )
    except Exception:
        flask.flash("Failed to read task info file!")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to read task info file:\n" + tb,
            file=sys.stderr
        )
        result = None

    if result is None:
        return None

    # Augment task info
    prfmt = result.get(
        "project_url_format",
        _CONFIG.get("DEFAULT_PROJECT_URL_FORMAT", "#")
    )
    taskfmt = result.get(
        "task_url_format",
        _CONFIG.get("DEFAULT_TASK_URL_FORMAT", "#")
    )
    for project in result.get("projects", result.get("psets")):
        project["url"] = prfmt.format(
            semester=semester,
            project=project["id"]
        )
        for task in project["tasks"]:
            task["url"] = taskfmt.format(
                semester=semester,
                project=project["id"],
                task=task["id"]
            )
            # Graft static task info into project task entry
            task.update(result["tasks"][task["id"]])

    # Augment exercise info if it's present
    exfmt = result.get(
        "exercise_url_format",
        _CONFIG.get("DEFAULT_EXERCISE_URL_FORMAT", "#")
    )
    if 'exercises' in result:
        for egroup in result["exercises"]:
            if 'url' not in egroup:
                egroup["url"] = exfmt.format(
                    semester=semester,
                    group=egroup["group"]
                )

    return result


def get_concepts(course, semester):
    """
    Loads concepts from the JSON file (or returns a cached version if the
    file hasn't been modified since we last loaded it). Needs the course
    and semester to load info for.

    Returns None if the file doesn't exist or can't be parsed.
    """
    filename = concepts_file(course, semester)
    try:
        return load_or_get_cached(
            filename,
            assume_fresh=_CONFIG.get("ASSUME_FRESH", 1)
        )
    except Exception:
        flask.flash("Failed to read concepts file!")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to read concepts file:\n" + tb,
            file=sys.stderr
        )
        return None


def get_admin_info(course, semester):
    """
    Reads the admin info file to get information about which users are
    administrators and various other settings.
    """
    filename = admin_info_file(course, semester)
    try:
        result = load_or_get_cached(
            filename,
            assume_fresh=_CONFIG.get("ASSUME_FRESH", 1)
        )
    except Exception:
        flask.flash("Failed to read admin info file '{}'!".format(filename))
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to read admin info file:\n" + tb,
            file=sys.stderr
        )
        result = None

    return result # might be None


def get_roster(course, semester):
    """
    Loads and returns the roster file. Returns None if the file is
    missing. Returns a dictionary where usernames are keys and values are
    student info (see `AsRoster`).
    """
    return load_or_get_cached(
        roster_file(course, semester),
        view=AsRoster,
        missing=None,
        assume_fresh=_CONFIG.get("ASSUME_FRESH", 1)
    )


def get_student_info(course, semester):
    """
    Loads and returns the student info file. Returns None if the file is
    missing.
    """
    return load_or_get_cached(
        student_info_file(course, semester),
        view=AsStudentInfo,
        missing=None,
        assume_fresh=_CONFIG.get("ASSUME_FRESH", 1)
    )


def get_extension(course, semester, username, project, phase):
    """
    Gets the extension value (as an integer number in hours) for a user
    on a given phase of a given project. Returns 0 if there is no
    extension info for that user. Returns None if there's an error
    reading the value.
    """
    key = extension_key(course, semester, username, project, phase)
    try:
        result = _REDIS.get(key)
    except Exception:
        flask.flash(
            "Failed to read extension info at '{}'!".format(key)
        )
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to read extension info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return None

    if result is None:
        result = 0
    else:
        result = int(result)

    return result


def set_extension(
    course,
    semester,
    username,
    prid,
    phase,
    duration=True,
    only_from=None
):
    """
    Sets an extension value for the given user on the given phase of the
    given project (in the given course/semester). May be an integer
    number of hours, or just True (the default) for the standard
    extension (whatever is listed in tasks.json). Set to False to remove
    any previously granted extension.

    If only_from is provided, the operation will fail when the extension
    value being updated isn't set to that value (may be a number of
    hours, or True for the standard extension, or False for unset). In
    that case, this function will return False if it fails. Set
    only_from to None to unconditionally update the extension.
    """
    key = extension_key(course, semester, username, prid, phase)
    task_info = get_task_info(course, semester)
    ext_hours = task_info.get("extension_hours", 24)

    if duration is True:
        duration = ext_hours
    elif duration is False:
        duration = 0
    elif not isinstance(duration, (int, bool)):
        raise ValueError(
            (
                "Extension duration must be an integer number of hours,"
                " or a boolean (got {})."
            ).format(repr(duration))
        )

    if only_from is True:
        only_from = ext_hours
    elif (
        only_from not in (False, None)
    and not isinstance(only_from, int)
    ):
        raise ValueError(
            (
                "Only-from must be None, a boolean, or an integer (got"
                " {})."
            ).format(repr(only_from))
        )

    with _REDIS.pipeline() as pipe:
        # Make sure we back off if there's a WatchError
        try:
            pipe.watch(key)
            # Check current value
            current = _REDIS.get(key)
            if current is not None:
                current = int(current) # convert from string

            if duration == current:
                # No need to update!
                return True

            if only_from is not None and (
                (only_from is False and current not in (None, 0))
             or (only_from is not False and current != only_from)
            ):
                # Abort operation because of pre-op change
                flask.flash(
                    (
                        "Failed to write extension info at '{}' (slow"
                        " change)!"
                    ).format(key)
                )
                return False

            # Go ahead and update the value
            pipe.multi()
            pipe.set(key, str(duration))
            pipe.execute()
        except redis.exceptions.WatchError:
            # Update didn't go through
            flask.flash(
                (
                    "Failed to write extension info at '{}' (fast"
                    " change)!"
                ).format(key)
            )
            return False
        except Exception:
            # Some other issue
            flask.flash(
                (
                    "Failed to write extension info at '{}' (unknown)!"
                ).format(key)
            )
            tb = potluck.html_tools.string_traceback()
            print(
                "Failed to write extension info at '{}':\n{}".format(
                    key,
                    tb
                ),
                file=sys.stderr
            )
            return False

    return True


def get_inflight(
    course,
    semester,
    username,
    phase,
    prid,
    taskid
):
    """
    Returns a quadruple containing the timestamp at which processing for
    the given user/phase/project/task was started, the filename of the log
    file for that evaluation run, the filename of the report file that
    will be generated when it's done, and a string indicating the status
    of the run. Reads that log file to check whether the process has
    completed, and updates in-flight state accordingly. Returns (None,
    None, None, None) if no attempts to grade the given task have been
    made yet.

    The status string will be one of:

    - "initial" - evaluation hasn't started yet.
    - "in_progress" - evaluation is running.
    - "error" - evaluation noted an error in the log.
    - "expired" - We didn't hear back from evaluation, but it's been so
         long that we've given up hope.
    - "completed" - evaluation finished.

    When status is "error", "expired", or "completed", it's appropriate
    to initiate a new evaluation run for that file, but in other cases,
    the existing run should be allowed to terminate first.

    In rare cases, when an exception is encountered trying to read the
    file even after a second attempt, the timestamp will be set to
    "error" with status and filename values of None.
    """
    key = inflight_key(course, semester, username, phase, prid, taskid)

    try:
        response = _REDIS.lrange(key, 0, -1)
    except Exception:
        flask.flash(
            "Failed to fetch in-flight info at '{}'!".format(key)
        )
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to fetch in-flight info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return ("error", None, None, None)

    # If the key didn't exist
    if response is None or len(response) == 0:
        return (None, None, None, None)

    # Unpack the response
    timestring, log_filename, report_filename, status = response

    if status in ("error", "expired", "completed"):
        # No need to check the log text again
        return (timestring, log_filename, report_filename, status)

    # Figure out what the new status should be...
    new_status = status

    # Read the log file to see if evaluation has finished yet
    if os.path.isfile(log_filename):
        try:
            with open(log_filename, 'r') as fin:
                log_text = fin.read()
        except Exception:
            flask.flash("Failed to read evaluation log file!")
            tb = potluck.html_tools.string_traceback()
            print(
                "Failed to read evaluation log file:\n" + tb,
                file=sys.stderr
            )
            # Treat as a missing file
            log_text = ""
    else:
        # No log file
        log_text = ""

    # If anything has been written to the log file, we're in progress...
    if status == "initial" and log_text != "":
        new_status = "in_progress"

    # Check for an error
    if potluck.render.ERROR_MSG in log_text:
        new_status = "error"

    # Check for completion message (ignored if there's an error)
    if (
        status in ("initial", "in_progress")
    and new_status != "error"
    and log_text.endswith(potluck.render.DONE_MSG + '\n')
    ):
        new_status = "completed"

    # Check absolute timeout (only if we DIDN'T see a done message)
    if new_status not in ("error", "completed"):
        elapsed = (
            potluck.time_utils.now()
          - potluck.time_utils.time_from_timestring(timestring)
        )
        allowed = datetime.timedelta(
            seconds=_CONFIG["FINAL_EVAL_TIMEOUT"]
        )
        if elapsed > allowed:
            new_status = "expired"

    # Now we've got our result
    result = (timestring, log_filename, report_filename, new_status)

    # Write new status if it has changed
    if new_status != status:
        try:
            with _REDIS.pipeline() as pipe:
                pipe.delete(key) # clear the list
                pipe.rpush(key, *result) # add our new info
                pipe.execute()
        except Exception:
            flask.flash(
                (
                    "Error trying to update in-flight info at '{}'."
                ).format(key)
            )
            tb = potluck.html_tools.string_traceback()
            print(
                "Failed to update in-flight info at '{}':\n{}".format(
                    key,
                    tb
                ),
                file=sys.stderr
            )
            return ("error", None, None, None)

    # Return our result
    return result


def put_inflight(course, semester, username, phase, prid, taskid):
    """
    Picks new log and report filenames for the given
    user/phase/project/task and returns a quad containing a string
    timestamp, the new log filename, the new report filename, and the
    status string "initial", while also writing that information into
    the inflight data for that user so that get_inflight will return it
    until evaluation is finished.

    Returns (None, None, None, None) if there is already an in-flight
    log file for this user/project/task that has a status other than
    "error", "expired", or "completed".

    Returns ("error", None, None, None) if it encounters a situation
    where the inflight key is changed during the update operation,
    presumably by another simultaneous call to put_inflight. This
    ensures that only one simultaneous call can succeed, and protects
    against race conditions on the log and report filenames.
    """
    # The Redis key for inflight info
    key = inflight_key(course, semester, username, phase, prid, taskid)

    with _REDIS.pipeline() as pipe:
        try:
            pipe.watch(key)
            response = pipe.lrange(key, 0, -1)
            if response is not None and len(response) != 0:
                # key already exists, so we need to check status
                prev_ts, prev_log, prev_result, prev_status = response
                if prev_status in ("initial", "in_progress"):
                    # Another evaluation is in-flight; indicate that to
                    # our caller and refuse to re-initiate evaluation
                    return (None, None, None, None)

            # Generate a timestamp for the log file
            timestamp = potluck.time_utils.timestring()

            # Get unused log and report filenames
            istring = "{phase}-{prid}-{taskid}-{timestamp}".format(
                phase=phase,
                prid=prid,
                taskid=taskid,
                timestamp=timestamp
            )

            # Note: unused_filename has a race condition if two
            # put_inflight calls occur simultaneously. However, due to
            # our use of watch, only one of the two calls can make it
            # out of this block without triggering a WatchError, meaning
            # that only the one that makes it out first will make use of
            # a potentially-conflicting filename. That said, *any* other
            # process which might create files with names like the log
            # and report filenames we select would be bad.

            # Select an unused log filename
            log_folder = logs_folder(course, semester, username)
            ensure_directory(log_folder)
            logfile = unused_filename(
                safe_join(log_folder, istring + ".log")
            )

            # Select an unused report filename
            report_folder = reports_folder(course, semester, username)
            ensure_directory(report_folder)
            reportfile = unused_filename(
                safe_join(report_folder, istring + ".json")
            )

            # Gather the info into a tuple
            ifinfo = (
                timestamp,
                logfile,
                reportfile,
                "initial"
            )

            # Rewrite the key
            pipe.multi()
            pipe.delete(key)
            pipe.rpush(key, *ifinfo)
            pipe.execute()
        except redis.exceptions.WatchError:
            flask.flash(
                (
                    "Unable to put task evaluation in-flight: key '{}'"
                    " was changed."
                ).format(key)
            )
            return ("error", None, None, None)
        except Exception:
            flask.flash(
                (
                    "Error trying to write in-flight info at '{}'."
                ).format(key)
            )
            tb = potluck.html_tools.string_traceback()
            print(
                "Failed to write in-flight info at '{}':\n{}".format(
                    key,
                    tb
                ),
                file=sys.stderr
            )
            return ("error", None, None, None)

    # Return the timestamp, filenames, and status that we recorded
    return ifinfo


def fetch_time_spent(course, semester, username, phase, prid, taskid):
    """
    Returns a time-spent record for the given user/phase/project/task.
    It has the following keys:

    - "phase": The phase (a string).
    - "prid": The project ID (a string).
    - "taskid": The task ID (a string).
    - "updated_at": A timestring (see `potluck.time_utils.timestring`)
        indicating when the information was last updated.
    - "time_spent": A floating-point number (as a string) or just a
        string describing the user's description of the time they spent
        on the task.
    - "prev_update": If present, indicates that the time_spent value
        came from a previous entry and was preserved when a newer entry
        would have been empty. Shows the time at which the previous
        entry was entered.
        TODO: preserve across multiple empty entries?

    Returns None if there is no information for that user/project/task
    yet, or if an error is encountered while trying to access that
    information.
    """
    # Redis key to use
    key = time_spent_key(
        course,
        semester,
        username,
        prid,
        phase,
        taskid
    )

    try:
        response = _REDIS.hmget(
            key,
            "updated_at",
            "time_spent",
            "prev_update"
        )
    except Exception:
        flask.flash("Error fetching time-spent info.")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to fetch time spent info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return None

    # Some kind of non-exception error during access, or key is missing
    if response is None or len(response) != 3 or response[0] is None:
        return None

    try:
        spent = float(response[1])
    except ValueError:
        spent = response[1]

    result = {
        "phase": phase,
        "prid": prid,
        "taskid": taskid,
        "updated_at": response[0],
        "time_spent": spent
    }

    if response[2] is not None:
        result["prev_update"] = response[2]

    return result


def record_time_spent(
    course,
    semester,
    username,
    phase,
    prid,
    taskid,
    time_spent
):
    """
    Inserts a time spent entry into the given user's time spent info.

    If called multiple times, the last call will override the
    information set by any previous ones. If called multiple times
    simultaneously, one of the calls will overwrite the other, but it
    may not be able to pull the other call's info to replace a default
    value (which is fine...).
    """
    # Redis key to use
    key = time_spent_key(
        course,
        semester,
        username,
        prid,
        phase,
        taskid
    )

    # Generate a timestamp for the info
    timestring = potluck.time_utils.timestring()

    # Convert to a number if we can
    try:
        time_spent = float(time_spent)
    except Exception:
        pass

    # Here's the info we store
    info = {
        "updated_at": timestring,
        "time_spent": time_spent
    }

    # Check for old info if the new info is missing
    if time_spent == "":
        try:
            response = _REDIS.hmget(
                key,
                "updated_at",
                "time_spent",
                "prev_update"
            )
            if (
                response is None
             or len(response) != 2
            ):
                raise ValueError(
                    "Unable to retrieve previous data from time spent"
                    " info."
                )
            # check for missing key, or no previous info
            if response[0] is not None and response[1] != '':
                if response[2] is None:
                    prev = response[0]
                else:
                    prev = response[2]

                info["prev_update"] = prev
                info["time_spent"] = response[1]
            # else leave info as-is

        except Exception:
            flask.flash("Failed to fetch time spent info!")
            tb = potluck.html_tools.string_traceback()
            print(
                "Failed to fetch time spent info at '{}':\n{}".format(
                    key,
                    tb
                ),
                file=sys.stderr
            )
            # we'll keep going to update new info though

    try:
        success = _REDIS.hmset(key, info)
        if success is not True:
            raise ValueError("Redis result indicated failure.")
    except Exception:
        flask.flash("Failed to write time-spent info!")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to write time spent info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )


def fetch_evaluation(course, semester, username, phase, prid, taskid):
    """
    Fetches the manual evaluation information for the given
    user/phase/project/task. The result will be a dictionary with the
    following keys:

    - "phase": The phase (a string).
    - "prid": The project ID (a string).
    - "taskid": The task ID (a string).
    - "updated_at": A timestring (see `potluck.time_utils.timestring`)
        indicating when the information was last updated.
    - "notes": The markdown source string for custom notes.
    - "override": A numerical score that overrides the automatic
        evaluation. Will be an empty string if there is no override to
        apply.
    - "timeliness": A numerical score for timeliness points to override
        the automatic value. Will be an empty string if there is no
        override, which should always be the case for non-initial phases.

    Returns None instead of a dictionary if there is no information for
    that user/project/task yet, or if an error is encountered while
    trying to access that information.
    """
    # Redis key to use
    key = evaluation_key(
        course,
        semester,
        username,
        prid,
        phase,
        taskid
    )

    try:
        response = _REDIS.hmget(
            key,
            "updated_at",
            "notes",
            "override",
            "timeliness"
        )
    except Exception:
        flask.flash("Error fetching evaluation info.")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to fetch evaluation info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return None

    # Some kind of non-exception error during access, or key is missing
    if (
        response is None
     or len(response) != 4
     or response[0] is None
    ):
        return None

    try:
        override = float(response[2])
    except (TypeError, ValueError):
        override = response[2] or ''

    try:
        timeliness = float(response[3])
    except (TypeError, ValueError):
        timeliness = response[3] or ''

    result = {
        "phase": phase,
        "prid": prid,
        "taskid": taskid,
        "updated_at": response[0],
        "notes": response[1],
        "override": override,
        "timeliness": timeliness,
    }

    return result


def set_evaluation(
    course,
    semester,
    username,
    phase,
    prid,
    taskid,
    notes,
    override="",
    timeliness=""
):
    """
    Updates the custom evaluation info for a particular task submitted by
    a particular user for a certain phase of a specific project (in a
    course/semester).

    Completely erases the previous custom evaluation info.

    The notes argument must be a string, and will be treated as Markdown
    and converted to HTML when being displayed to the user. It will be
    displayed on a feedback page and it can thus link to rubric items or
    snippets by their IDs if you want to get fancy.

    The override argument defaults to an empty string, which is how to
    indicate that no override should be applied. Otherwise, it should be
    a floating-point number or integer between 0 and 100; it will be
    stored as a float if convertible.

    The timeliness argument works like the override argument, but
    overrides the timeliness score. It should only be set for the
    'initial' phase.

    Returns True if it succeeds or False if it encounters some sort of
    error.
    """
    # Redis key to use
    key = evaluation_key(
        course,
        semester,
        username,
        prid,
        phase,
        taskid
    )

    # Get task info for this course/semester so we can access per-course
    # config values...
    task_info = get_task_info(course, semester)
    relevant_task = task_info.get("tasks", {}).get(taskid, {})
    relevant_projects = [
        p
        for p in task_info.get("projects", task_info.get("psets", {}))
        if p["id"] == prid
    ]
    if len(relevant_projects) > 0:
        relevant_project = relevant_projects[0]
    else:
        relevant_project = {}

    # Generate a timestamp for the info
    timestring = potluck.time_utils.timestring()

    # Get SCORE_BASIS and TIMELINESS_POINTS values from
    # task/project/task_info/config
    score_basis = relevant_task.get(
        "SCORE_BASIS",
        relevant_project.get(
            "SCORE_BASIS",
            task_info.get(
                "SCORE_BASIS",
                _CONFIG.get("SCORE_BASIS", 100)
            )
        )
    )
    timeliness_basis = relevant_task.get(
        "TIMELINESS_POINTS",
        relevant_project.get(
            "TIMELINESS_POINTS",
            task_info.get(
                "TIMELINESS_POINTS",
                _CONFIG.get("TIMELINESS_POINTS", 10)
            )
        )
    )

    # Convert to a number if we can
    if override != "":
        try:
            override = float(override)
            if 0 < override < 1 and score_basis >= 10:
                flask.flash(
                    (
                        "Warning: you entered '{}' as the grade"
                        " override, but scores should be specified out"
                        " of {}, not out of 1! The override has been"
                        " set as-given but you may want to update it."
                    ).format(override, score_basis)
                )
        except Exception:
            flask.flash(
                (
                    "Warning: you entered '{}' as the grade override,"
                    " but grade overrides should be numbers between 0"
                    " and {}. The override has been set as-given, but"
                    " you may want to update it."
                ).format(override, score_basis)
            )

    # Convert to a number if we can
    if timeliness != "":
        try:
            timeliness = float(timeliness)
            if 0 < timeliness < 1 and timeliness_basis >= 5:
                flask.flash(
                    (
                        "Warning: you entered '{}' as the timeliness"
                        " override, but timeliness scores should be"
                        " specified out of {}, not out of 1! The"
                        " override has been set as-given but you may"
                        " want to update it."
                    ).format(timeliness, timeliness_basis)
                )
        except Exception:
            flask.flash(
                (
                    "Warning: you entered '{}' as the grade override,"
                    " but timeliness overrides should be numbers"
                    " between 0 and {}. The override has been set"
                    " as-given, but you may want to update it."
                ).format(override, timeliness_basis)
            )

    # Here's the info we store
    info = {
        "updated_at": timestring,
        "notes": notes,
        "override": override,
        "timeliness": timeliness,
    }

    try:
        success = _REDIS.hmset(key, info)
        if success is not True:
            raise ValueError("Redis result indicated failure.")
    except Exception:
        flask.flash("Failed to write evaluation info!")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to write evaluation info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return False

    return True


def get_egroup_override(
    course,
    semester,
    username,
    egroup
):
    """
    Returns the score override for a particular exercise group. The
    result is a dictionary with the following keys:

    - "updated_at": A timestring indicating when the override was set.
    - "status": The status string specified by the override.
    - "note": A string specified by the person who set the override.
    - "override": The grade override, as a floating-point value based on
        the exercise group's SCORE_BASIS, or an empty string if there is
        no override.

    In case of an error or when no override is present, the result will
    be `None`.
    """
    # Redis key to use
    key = egroup_override_key(
        course,
        semester,
        username,
        egroup
    )

    try:
        response = _REDIS.hmget(
            key,
            "updated_at",
            "status",
            "note",
            "override"
        )
    except Exception:
        flask.flash(
            (
                "Error fetching exercise group override info for group"
                " '{}'."
            ).format(egroup)
        )
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to fetch exercise group override at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return None

    if response is None or len(response) != 4:
        return None

    try:
        score = float(response[3])
    except (TypeError, ValueError):
        score = ''

    return {
        "updated_at": response[0],
        "status": response[1],
        "note": response[2],
        "override": score
    }


def set_egroup_override(
    course,
    semester,
    username,
    egroup,
    override="",
    note="",
    status=""
):
    """
    Updates the exercise group score override for a particular exercise
    group submitted by a particular user for a specific exercise group
    (in a course/semester).

    Completely erases the previous override info.

    The `note` argument must be a string, and will be treated as Markdown
    and converted to HTML when being displayed to the user. It will be
    displayed on the student's dashboard in the expanded view for the
    exercise group.

    The `override` argument defaults to an empty string, which is how to
    indicate that no override should be applied. Otherwise, it should be
    a floating-point number or integer between 0 and 1 (inclusive),
    indicating the fraction of full credit to award. It will be stored as
    a floating-point number if it's convertible to one. Note that this
    fraction is still subject to the `EXERCISE_GROUP_CREDIT_BUMP` logic
    in `app.ex_combined_grade`.

    The `status` argument defaults to an empty string; in that case the
    status will not be changed. If not empty, it should be one of the
    strings "perfect," "complete," "partial," "incomplete," "pending,"
    or "unreleased."

    Returns True if it succeeds or False if it encounters some sort of
    error.
    """
    # Redis key to use
    key = egroup_override_key(
        course,
        semester,
        username,
        egroup
    )

    # Get task info for this course/semester so we can access per-course
    # config values...
    task_info = get_task_info(course, semester)
    all_egroups = task_info.get("exercises", [])
    this_eginfo = None
    for gr in all_egroups:
        if gr.get('group', '') == egroup:
            if this_eginfo is None:
                this_eginfo = gr
            else:
                flask.flash(
                    "Multiple exercise groups with group ID '{}'".format(
                        egroup
                    )
                )
                print(
                    "Multiple exercise groups with group ID '{}'".format(
                        egroup
                    ),
                    file=sys.stderr
                )
                # We keep using the first-specified group info

    # No info for this egroup?
    if this_eginfo is None:
        flask.flash("No exercise group with group ID '{}'".format(egroup))
        print(
            "No exercise group with group ID '{}'".format(egroup),
            file=sys.stderr
        )
        return False

    # Generate a timestamp for the info
    timestring = potluck.time_utils.timestring()

    # Convert to a number if we can
    if override != "":
        try:
            override = float(override)
            if override > 1 or override < 0:
                flask.flash(
                    (
                        "Warning: you entered '{}' as the grade"
                        " override, but scores should be specified as"
                        " a fraction between 0.0 and 1.0. the override"
                        " has been set as-given but you may want to"
                        " update it."
                    ).format(override)
                )
        except Exception:
            flask.flash(
                (
                    "Warning: you entered '{}' as the grade override,"
                    " but grade overrides should be numbers."
                    " The override has been set as-given, but"
                    " you may want to update it."
                ).format(override)
            )

    # Here's the info we store
    info = {
        "updated_at": timestring,
        "status": status,
        "note": note,
        "override": override
    }

    try:
        success = _REDIS.hmset(key, info)
        if success is not True:
            raise ValueError("Redis result indicated failure.")
    except Exception:
        flask.flash("Failed to write evaluation info!")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to write evaluation info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return False

    return True


def fetch_old_outcomes(course, semester, username, exercise):
    """
    Fetches old outcomes for the given course/semester/username/exercise.
    """
    # Redis key to use
    key = old_exercise_key(course, semester, username, exercise)

    try:
        exists = _REDIS.exists(key)
    except Exception:
        flask.flash("Error checking for outcomes info.")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to check for outcomes info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return None

    # Return None without making a fuss if the key just doesn't exist
    if not exists:
        return None

    try:
        responseJSON = _REDIS.get(key)
        info = json.loads(responseJSON)
    except Exception:
        flask.flash("Error fetching or decoding outcomes info.")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to fetch outcomes info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return None

    return info


def fetch_outcomes(course, semester, username, exercise, category):
    """
    Fetches the outcomes-list information for the given
    user/course/semester/exercise/category. The 'category' should be one
    of the strings 'full', 'partial', or 'none'. The result will be a
    list of dictionaries each representing a single submission, in
    chronological order. Each will have the following keys:

    - "submitted_at" - A time string (see
        `potluck.time_utils.timestring`) indicating when the list of
        outcomes was submitted.
    - "authors" - A list of usernames for participating authors.
    - "outcomes" - A list of 3-tuple outcomes, which contain a boolean
        for success/failure followed by tag and message strings (see
        `optimism.listOutcomesInSuite`)
    - "code": A list of filename, code pairs with any code blocks
        submitted along with the outcomes.
    - "status": A status string indicating the overall exercise status,
        determined by callers to `save_outcomes`.
    - "credit": A number indicating how much credit (0-1) was earned for
        this outcome. May also be `None` in some cases.
    - "group_credit": A credit number that determines how much credit is
        earned towards this exercise group. Will be 0 when "credit" is
        `None`. If the category is 'none', this will always be 0, if the
        category is 'partial' it will be greater than 0 and less than 1,
        and if the category is 'full', it will be 1. This number does NOT
        account for timeliness (yet; see `fetch_best_outcomes`).

    Returns None instead of a list if there is no information for that
    user/exercise/category yet, or if an error is encountered while
    trying to access that information.
    """
    # Redis key to use
    key = exercise_key(course, semester, username, exercise, category)

    try:
        exists = _REDIS.exists(key)
    except Exception:
        flask.flash("Error checking for outcomes info.")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to check for outcomes info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return None

    # Return None without making a fuss if the key just doesn't exist
    if not exists:
        return None

    try:
        responseJSON = _REDIS.get(key)
        info = json.loads(responseJSON)
    except Exception:
        flask.flash("Error fetching or decoding outcomes info.")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to fetch outcomes info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return None

    return info


def update_submission_credit(submission, deadline, late_fraction):
    """
    Helper for updating submission group credit based on timeliness
    given the specified `deadline`. Sets the "on_time" and
    "group_credit" slots of the submission. "on_time" is based on the
    "submitted_at" slot and the specified `deadline`; "group_credit" is
    based on the original "group_credit" value (or "credit" value if
    there is no "group_credit" value) and is multiplied by the
    `late_fraction` if the submission is not on-time.

    Modifies the given submission dictionary; does not return anything.
    """
    # Get base credit value
    submission["group_credit"] = (
        submission.get(
            "group_credit",
            submission.get("credit", 0)
        )
    ) or 0  # this ensures None becomes 0 if there's an explicit None

    # Figure out if it was on time or late
    if submission["submitted_at"] == "on_time":
        on_time = True
    elif submission["submitted_at"] == "late":
        on_time = False
    else:
        when = potluck.time_utils.time_from_timestring(
            submission["submitted_at"]
        )
        on_time = when <= deadline

    # Update submission & possibly credit
    submission["on_time"] = on_time
    if not on_time:
        submission["group_credit"] *= late_fraction


def fetch_best_outcomes(
    course,
    semester,
    username,
    exercise,
    deadline,
    late_fraction
):
    """
    Fetches the best outcome information for a particular
    course/semester/user/exercise. To do that, it needs to know what
    that user's current deadline is, and what credit multiplier to apply
    to late submissions. The deadline should be given as a
    `datetime.datetime` object. If the user has any manual overrides, the
    most recent of those will be returned.

    The result will be a dictionary with the following keys:

    - "submitted_at" - A time string (see
        `potluck.time_utils.timestring`) indicating when the list of
        outcomes was submitted. For overrides, might be the string
        "on_time" or the string "late" to indicate a specific lateness
        value regardless of deadline.
    - "on_time" - A boolean indicating whether the submission came in on
        time or not, based on the deadline given and the submission
        time.
    - "authors" - A list of usernames for participating authors, OR a
        list containing just the person entering the override for an
        override.
    - "outcomes" - A list of 3-tuple outcomes, which contain a boolean
        for success/failure followed by tag and message strings (see
        `optimism.listOutcomesInSuite`). For overrides, this is instead
        a Markdown string explaining things.
    - "code" - A list of filename/code-string pairs indicating any code
        blocks attached to the submission. For overrides, this is the
        special string "__override__" to indicate that they're overrides.
    - "status" - A status string describing the exercise status based on
        the outcomes which passed/failed.
    - "credit" - A number indicating how much credit this exercise is
        worth (higher = better) or possibly `None` if there is some issue
        with the submission (like wrong # of outcomes). This does not take
        timeliness into account.
    - "group_credit" - A credit number that accounts for timeliness, and
        which will always be a number (it's 0 when `credit` would be `None`).

    Returns None if an error is encountered, or if the user has no
    submissions for that exercise.
    """
    best = None
    overrides = fetch_outcomes(
        course,
        semester,
        username,
        exercise,
        'override'
    )
    # Short-circuit and return most-recent override regardless of credit
    # if there is at least one.
    if overrides is None:
        overrides = []
    if len(overrides) > 0:
        update_submission_credit(overrides[-1], deadline, late_fraction)
        return overrides[-1]

    fulls = fetch_outcomes(course, semester, username, exercise, 'full')
    if fulls is None:
        fulls = []
    for submission in reversed(fulls):  # iterate backwards chronologically
        update_submission_credit(submission, deadline, late_fraction)

        if best is None or submission["group_credit"] >= best["group_credit"]:
            best = submission
            # It this one gets full credit; no need to look for better
            if submission["group_credit"] == 1:
                break

    # Only look at partials if we didn't find a full-credit best
    # submission
    if best is None or best["group_credit"] < 1:
        partials = fetch_outcomes(
            course,
            semester,
            username,
            exercise,
            'partial'
        )
        if partials is None:
            partials = []
        for submission in partials:
            update_submission_credit(submission, deadline, late_fraction)

            if (
                best is None
             or submission["group_credit"] >= best["group_credit"]
            ):
                best = submission

    # Only look at no-credit submissions if we have no full or
    # partial-credit submissions at all.
    if best is None:
        nones = fetch_outcomes(
            course,
            semester,
            username,
            exercise,
            'none'
        )
        if nones is not None:
            # Always take chronologically last one; none of these are worth
            # any credit anyways.
            best = nones[-1]
            update_submission_credit(best, deadline, late_fraction)

    # Try legacy info
    if best is None or best["group_credit"] < 1:
        legacy = fetch_old_outcomes(
            course,
            semester,
            username,
            exercise
        )
        if legacy is None:
            legacy = []
        for submission in legacy:
            old_on_time = submission.get("on_time", True)
            # figure out unpenalized credit if it had been marked late
            if old_on_time is False:
                submission["group_credit"] /= late_fraction

            update_submission_credit(submission, deadline, late_fraction)

            if (
                best is None
             or submission["group_credit"] >= best["group_credit"]
            ):
                best = submission

    return best  # might still be None


def save_outcomes(
    course,
    semester,
    username,
    exercise,
    authors,
    outcomes,
    codeBlocks,
    status,
    credit,
    group_credit
):
    """
    Saves a list of outcomes for a specific exercise submitted by a
    particular user who is taking a course in a certain semester. The
    outcomes list should be a list of 3-tuples each consisting of a
    boolean, a tag string, and a message string (e.g., the return value
    from `optimism.listOutcomesInSuite`). The authors value should be a
    list of username strings listing all authors who contributed. The
    `codeBlocks` value should be a list of pairs, each of which has a
    filename string and a code string (the filename could also elsehow
    identify the source code was derived from). The `status` value should
    be a string describing the status of the submission, while the credit
    value should be a number between 0 and 1 (inclusive) where a higher
    number indicates a better submission.

    The list of outcomes and associated code blocks is added to the
    record of all such lists submitted for that exercise by that user,
    categorized as 'none', 'partial', or 'full' depending on whether the
    credit value is 0, between 0 and 1, or 1. It will be stored as a
    dictionary with the following slots:

    - "submitted_at": the current time, as a string (see
        `potluck.time_utils.timestring`).
    - "authors": The list of authors.
    - "outcomes": The list of outcomes.
    - "code": The list of filename/code-string pairs.
    - "status": The status string.
    - "credit": The credit number.
    - "group_credit": The credit number for counting group credit.

    Returns True if it succeeds or False if it encounters some sort of
    error.
    """
    category = 'none'
    if group_credit > 1:
        raise ValueError(
            "Invalid group_credit value '{}' (must be <= 1).".format(
                group_credit
            )
        )
    elif group_credit == 1:
        category = 'full'
    elif group_credit > 0:
        category = 'partial'

    # Redis key to use
    key = exercise_key(course, semester, username, exercise, category)

    # Generate a timestamp for the info
    timestring = potluck.time_utils.timestring()

    # Get old outcomes so we can add to them
    recorded_outcomes = fetch_outcomes(
        course,
        semester,
        username,
        exercise,
        category
    )
    if recorded_outcomes is None:
        recorded_outcomes = []

    # Here's the info we store
    info = {
        "submitted_at": timestring,
        "authors": authors,
        "outcomes": outcomes,
        "code": codeBlocks,
        "status": status,
        "credit": credit,
        "group_credit": group_credit
    }

    recorded_outcomes.append(info)

    new_encoded = json.dumps(recorded_outcomes)

    try:
        success = _REDIS.set(key, new_encoded)
        if success is not True:
            raise ValueError("Redis result indicated failure.")
    except Exception:
        flask.flash("Failed to write outcomes info!")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to write outcomes info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return False

    return True


def save_outcomes_override(
    course,
    semester,
    username,
    exercise,
    overrider,
    note,
    status,
    credit,
    time_override=None
):
    """
    Saves an outcome override for a specific exercise submitted by a
    particular user who is taking a course in a certain semester.

    The `overrider` should be the username of the person entering the
    override. The `note` must be a string, and will be rendered using
    Markdown to appear on the user's detailed view of the exercise in
    question.

    The status and credit values are the same as for `save_outcomes`:
    `status` is a status string and `credit` is a floating-point number
    between 0 and 1 (inclusive).

    If `time_override` is provided, it should be one of the strings
    "on_time" or "late" and the exercise will be marked as such
    regardless of the relationship between the deadline and the
    submission time. Note that the late penalty will be applied to the
    credit value for overrides which are marked as late.

    TODO: Not that?

    Only the most recent outcome override applies to a student's grade,
    but all outcome overrides will be visible to them.
    TODO: Allow for deleting/editing them!

    The outcome override will be stored as a dictionary with the
    following slots:

    - "submitted_at": the current time, as a string (see
        `potluck.time_utils.timestring`) or the provided `time_override`
        value.
    - "authors": A list containing just the `overrider`.
    - "outcomes": The `note` string.
    - "code": The special value `"__override__"` to mark this as an
        override.
    - "status": The provided status string.
    - "credit": The provided credit number.
    - "group_credit": A second copy of the credit number.

    It is always stored in the "override" category outcomes storage.

    Returns True if it succeeds or False if it encounters some sort of
    error.
    """
    # Redis key to use
    key = exercise_key(course, semester, username, exercise, 'override')

    # Generate a timestamp for the info
    if time_override is None:
        timestring = potluck.time_utils.timestring()
    else:
        timestring = time_override

    # Get old outcomes so we can add to them
    recorded_outcomes = fetch_outcomes(
        course,
        semester,
        username,
        exercise,
        'override'
    )
    if recorded_outcomes is None:
        recorded_outcomes = []

    # Here's the info we store
    info = {
        "submitted_at": timestring,
        "authors": [overrider],
        "outcomes": note,
        "code": "__override__",
        "status": status,
        "credit": credit,
        "group_credit": credit
    }

    recorded_outcomes.append(info)

    new_encoded = json.dumps(recorded_outcomes)

    try:
        success = _REDIS.set(key, new_encoded)
        if success is not True:
            raise ValueError("Redis result indicated failure.")
    except Exception:
        flask.flash("Failed to write exercise override info!")
        tb = potluck.html_tools.string_traceback()
        print(
            "Failed to write exercise override info at '{}':\n{}".format(
                key,
                tb
            ),
            file=sys.stderr
        )
        return False

    return True


def default_feedback_summary():
    """
    Returns a default summary object. The summary is a pared-down version
    of the full feedback .json file that stores the result of
    `potluck.render.render_report`, which in turn comes mostly from
    `potluck.rubrics.Rubric.evaluate`.
    """
    return {
        "submitted": False, # We didn't find any feedback file!
        "timestamp": "(not evaluated)",
        "partner_username": None,
        "evaluation": "not evaluated",
        "warnings": [ "We found no submission for this task." ],
        "is_default": True
    }


def get_feedback_summary(
    course,
    semester,
    task_info,
    username,
    phase,
    prid,
    taskid
):
    """
    This retrieves just the feedback summary information that appears on
    the dashboard for a given user/phase/project/task. That much info is
    light enough to cache, so we do cache it to prevent hitting the disk
    a lot for each dashboard view.
    """
    ts, log_file, report_file, status = get_inflight(
        course,
        semester,
        username,
        phase,
        prid,
        taskid
    )
    fallback = default_feedback_summary()
    if ts in (None, "error"):
        return fallback
    try:
        return load_or_get_cached(
            report_file,
            view=AsFeedbackSummary,
            missing=fallback,
            assume_fresh=_CONFIG.get("ASSUME_FRESH", 1)
        )
    except Exception:
        flask.flash("Failed to summarize feedback file.")
        return fallback


def get_feedback(
    course,
    semester,
    task_info,
    username,
    phase,
    prid,
    taskid
):
    """
    Gets feedback for the user's latest pre-deadline submission for the
    given phase/project/task. Instead of caching these values (which
    would be expensive memory-wise over time) we hit the disk every
    time.

    Returns a dictionary with at least a 'status' entry. This will be
    'ok' if the report was read successfully, or 'missing' if the report
    file could not be read or did not exist. If the status is
    'missing', a 'log' entry will be present with the contents of the
    associated log file, or the string 'missing' if that log file could
    also not be read.

    Weird stuff could happen if the file is being written as we make the
    request. Typically a second attempt should not re-encounter such an
    error.
    """
    result = { "status": "unknown" }
    ts, log_file, report_file, status = get_inflight(
        course,
        semester,
        username,
        phase,
        prid,
        taskid
    )
    if ts is None: # No submission
        result["status"] = "missing"
    elif ts == "error": # Failed to read inflight file
        flask.flash(
            "Failed to fetch in-flight info; please refresh the page."
        )
        result["status"] = "missing"

    if result["status"] != "missing":
        try:
            if not os.path.exists(report_file):
                result["status"] = "missing"
            else:
                with open(report_file, 'r') as fin:
                    result = json.load(fin)
                    result["status"] = "ok"
        except Exception:
            flask.flash("Failed to read feedback file.")
            tb = potluck.html_tools.string_traceback()
            print(
                "Failed to read feedback file '{}':\n{}".format(
                    report_file,
                    tb
                ),
                file=sys.stderr
            )
            result["status"] = "missing"

    if result["status"] == "ok":
        # Polish up warnings/evaluation a tiny bit
        warnings = result.get("warnings", [])
        evaluation = result.get("evaluation", "not evaluated")
        if evaluation == "incomplete" and len(warnings) == 0:
            warnings.append(
                "Your submission is incomplete"
              + " (it did not satisfy even half of the core goals)."
            )
        result["evaluation"] = evaluation
        result["warnings"] = warnings
        result["submitted"] = True

    # Try to read log file if we couldn't get a report
    if result["status"] == "missing":
        if log_file is None:
            result["log"] = "no submission was made"
        else:
            try:
                if not os.path.exists(log_file):
                    result["log"] = "missing"
                else:
                    with open(log_file, 'r') as fin:
                        result["log"] = fin.read()
            except Exception:
                flask.flash("Error reading log file.")
                tb = potluck.html_tools.string_traceback()
                print(
                    "Failed to read log file '{}':\n{}".format(log_file, tb),
                    file=sys.stderr
                )
                result["log"] = "missing"

    return result


def get_feedback_html(
    course,
    semester,
    task_info,
    username,
    phase,
    prid,
    taskid
):
    """
    Gets feedback for the user's latest pre-deadline submission for the
    given phase/project/task, as html instead of as json (see
    `get_feedback`). Instead of caching these values (which would be
    expensive memory-wise over time) we hit the disk every time.

    Returns the string "missing" if the relevant feedback file does not
    exist, or if some kind of error occurs trying to access the file.

    Might encounter an error if the file is being written as we try to
    read it.
    """
    result = None
    ts, log_file, report_file, status = get_inflight(
        course,
        semester,
        username,
        phase,
        prid,
        taskid
    )
    if ts is None: # No submission
        result = "missing"
    elif ts == "error": # Failed to read inflight file
        flask.flash(
            "Failed to read in-flight info; please refresh the page."
        )
        result = "missing"

    if result != "missing":
        html_file = report_file[:-5] + ".html"
        try:
            if os.path.exists(html_file):
                # These include student code, instructions, etc., so it
                # would be expensive to cache them.
                with open(html_file, 'r') as fin:
                    result = fin.read()
                result = AsFeedbackHTML.decode(result)
            else:
                result = "missing"
        except Exception:
            flask.flash("Failed to read feedback report.")
            tb = potluck.html_tools.string_traceback()
            print(
                "Failed to read feedback report '{}':\n{}".format(
                    html_file,
                    tb
                ),
                file=sys.stderr
            )
            result = "missing"

    return result


#-------#
# Views #
#-------#

class View:
    """
    Abstract View class to organize decoding/encoding of views. Each View
    must define encode and decode class methods which are each others'
    inverse. The class name is used as part of the cache key. For
    read-only views, a exception (e.g., NotImplementedError) should be
    raised in the encode method.

    Note that the decode method may be given None as a parameter in
    situations where a file doesn't exist, and in most cases should
    simply pass that value through.
    """
    @staticmethod
    def encode(obj):
        """
        The encode function of a View must return a string (to be written
        to a file).
        """
        raise NotImplementedError("Don't use the base View class.")

    @staticmethod
    def decode(string):
        """
        The encode function of a View must accept a string, and if given
        a string produced by encode, should return an equivalent object.
        """
        raise NotImplementedError("Don't use the base View class.")


class AsIs(View):
    """
    A pass-through view that returns strings unaltered.
    """
    @staticmethod
    def encode(obj):
        """Returns the object it is given unaltered."""
        return obj

    @staticmethod
    def decode(string):
        """Returns the string it is given unaltered."""
        return string


class AsJSON(View):
    """
    A view that converts objects to JSON for file storage and back on
    access. It passes through None.
    """
    @staticmethod
    def encode(obj):
        """Returns the JSON encoding of the object."""
        return json.dumps(obj)

    @staticmethod
    def decode(string):
        """
        Returns a JSON object parsed from the string.
        Returns None if it gets None.
        """
        if string is None:
            return None
        return json.loads(string)


def build_view(name, encoder, decoder, pass_none=True):
    """
    Function for building a view given a name, an encoding function, and
    a decoding function. Unless pass_none is given as False, the decoder
    will be skipped if the decode argument is None and the None will pass
    through, in which case the decoder will *always* get a string as an
    argument.
    """
    class SyntheticView(View):
        """
        View class created using build_view.
        """
        @staticmethod
        def encode(obj):
            return encoder(obj)

        @staticmethod
        def decode(string):
            if pass_none and string is None:
                return None
            return decoder(string)

    SyntheticView.__name__ = name
    SyntheticView.__doc__ = (
        "View that uses '{}' for encoding and '{}' for decoding."
    ).format(encoder.__name__, decoder.__name__)
    SyntheticView.encode.__doc__ = encoder.__doc__
    SyntheticView.decode.__doc__ = decoder.__doc__

    return SyntheticView


class AsStudentInfo(View):
    """
    Encoding and decoding for TSV student info files, which are cached.
    The student info structure is a dictionary mapping usernames to
    additional student info.
    """
    @staticmethod
    def encode(obj):
        """
        Student info *cannot* be encoded, because we are not interested
        in writing it to a file.
        TODO: Student info editing in-app?
        """
        raise NotImplementedError(
            "Cannot encode student info: student info is read-only."
        )

    @staticmethod
    def decode(string):
        """
        Extra student info is read from a student info file by extracting
        the text, loading it as Excel-TSV data, and turning it into a
        dictionary where each student ID maps to a dictionary containing
        the columns as keys with values from that column as values.
        """
        reader = csv.DictReader(
            (line for line in string.strip().split('\n')),
            dialect="excel-tab"
        )
        result = {}
        for row in reader:
            entry = {}
            # TODO: Get this remap on a per-course basis!!!
            for key in _CONFIG["REMAP_STUDENT_INFO"]:
                entry[_CONFIG["REMAP_STUDENT_INFO"][key]] = row.get(key)
            entry["username"] = entry["email"].split('@')[0]
            result[entry['username']] = entry
        return result


class AsRoster(View):
    """
    Encoding and decoding for CSV rosters, which are cached. The roster
    structure is a dictionary mapping usernames to student info (see
    `load_roster_from_stream`).
    """
    @staticmethod
    def encode(obj):
        """
        A roster *cannot* be encoded, because we are not interested in
        writing it to a file.
        TODO: Roster editing in-app?
        """
        raise NotImplementedError(
            "Cannot encode a roster: rosters are read-only."
        )

    @staticmethod
    def decode(string):
        """
        A roster is read from a roaster file by extracting the text and
        running it through `load_roster_from_stream`.
        """
        lines = string.strip().split('\n')
        return load_roster_from_stream(lines)


class AsFeedbackHTML(View):
    """
    Encoding and decoding for feedback HTML files (we extract the body
    contents).
    """
    @staticmethod
    def encode(obj):
        """
        Feedback HTML *cannot* be encoded, because we want it to be
        read-only: it's produced by running potluck_eval, and the server
        won't edit it.
        """
        raise NotImplementedError(
            "Cannot encode feedback HTML: feedback is read-only."
        )

    @staticmethod
    def decode(string):
        """
        Feedback HTML is read from the raw HTML file by extracting the
        innerHTML of the body tag using Beautiful Soup. Returns a default
        string if the file wasn't found.
        """
        if string is None: # happens when the target file doesn't exist
            return "no feedback available"
        soup = bs4.BeautifulSoup(string, "html.parser")
        body = soup.find("body")
        return str(body)


class AsFeedbackSummary(View):
    """
    Encoding and decoding for feedback summaries, which are cached.
    """
    @staticmethod
    def encode(obj):
        """
        A feedback summary *cannot* be encoded, because it cannot be
        written to a file. Feedback summaries are only read from full
        feedback files, never written.
        """
        raise NotImplementedError(
            "Cannot encode a feedback summary: summaries are read-only."
        )

    @staticmethod
    def decode(string):
        """
        A feedback summary is read from a feedback file by extracting the
        full JSON feedback and then paring it down to just the essential
        information for the dashboard view.
        """
        if string is None: # happens when the target file doesn't exist
            return default_feedback_summary()
        # Note taskid is nonlocal here
        raw_report = json.loads(string)
        warnings = raw_report.get("warnings", [])
        evaluation = raw_report.get("evaluation", "not evaluated")
        if evaluation == "incomplete" and len(warnings) == 0:
            warnings.append(
                "Your submission is incomplete"
              + " (it did not satisfy even half of the core goals)."
            )
        return {
            "submitted": True,
            "partner_username": raw_report.get("partner_username"),
            "timestamp": raw_report.get("timestamp"),
            "evaluation": evaluation,
            "warnings": warnings,
            "is_default": False
            # report summary, files, table, and contexts omitted
        }


#------------------------#
# Read-only file caching #
#------------------------#

# Note: by using a threading.RLock and a global variable here, we are not
# process-safe, which is fine, because this is just a cache: each process
# in a multi-process environment can safely maintain its own cache which
# will waste a bit of memory but not lead to corruption. As a corollary,
# load_or_get_cached should be treated as read-only, otherwise one
# process might write to a file that's being read leading to excessively
# interesting behavior.

# TODO: We should probably have some kind of upper limit on the cache
# size, and maintain staleness so we can get rid of stale items...
_CACHE_LOCK = threading.RLock() # Make this reentrant just in case...
_CACHE = {}
"""
Cache of objects returned by view functions on cache keys.
"""


_FRESH_AT = {}
"""
Mapping from cache keys to tuples of seconds-since-epoch floats
representing the most recent time-span during which the file was found to
be unchanged. The first element of each tuple represents the earliest time
at which a freshness check succeeded with no subsequent failed checks,
and the second element represents the most recent time another successful
check was performed. Whenever a check is performed and succeeds, the
second element is updated, and whenever a check is performed and fails,
the value is set to None. When the value is None and a check succeeds,
both elements of the tuple are set to the current time.
"""


def build_file_freshness_checker(
    missing=Exception,
    assume_fresh=0,
    cache={}
):
    """
    Builds a freshness checker that checks the mtime of a filename, but
    if that file doesn't exist, it returns AbortGeneration with the given
    missing value (unless missing is left as the default of Exception, in
    which case it lets the exception bubble out).

    If assume_fresh is set to a positive number, and less than that many
    seconds have elapsed since the most recent mtime check, the mtime
    check is skipped and the file is assumed to be fresh.
    """
    ck = (id(missing), assume_fresh)
    if ck in cache:
        return cache[ck]

    def check_file_is_changed(cache_key, ts):
        """
        Checks whether a file has been modified more recently than the given
        timestamp.
        """
        global _FRESH_AT
        now = time.time()
        cached_fresh = _FRESH_AT.get(cache_key)
        if cached_fresh is not None:
            cached_start, cached_end = cached_fresh
            if (
                ts is not None
            and ts >= cached_start
                # Note we don't check ts <= cached_end here
            and (now - cached_end) < _CONFIG.get("ASSUME_FRESH", 1)
            ):
                return False  # we assume it has NOT changed

        filename = cache_key_filename(cache_key)
        try:
            mtime = os.path.getmtime(filename)
        except OSError_or_FileNotFoundError:
            if missing == Exception:
                raise
            else:
                return AbortGeneration(missing)

        # File is changed if the mtime is after the given cache
        # timestamp, or if the timestamp is None
        result = ts is None or mtime >= ts
        if result:
            # If we find that a specific time was checked, and that time
            # was after the beginning of the current cached fresh period,
            # we erase the cached fresh period, since result being true
            # means the file HAS changed.
            if (
                ts is not None
            and (
                    cached_fresh is not None
                and ts > cached_start
                )
            ):
                _FRESH_AT[cache_key] = None
        else:
            # If the file WASN'T changed, we extend the cache freshness
            # (In this branch ts is NOT None and it's strictly greater
            # than mtime)
            if cached_fresh is not None:
                # If an earlier-time-point was checked and the check
                # succeeded, we can extend the fresh-time-span backwards
                if ts < cached_start:
                    cached_start = ts

                # Likewise, we might be able to extend it forwards
                if ts > cached_end:
                    cached_end = ts

                # Update the time-span
                _FRESH_AT[cache_key] = (cached_start, cached_end)
            else:
                # If we didn't have cached freshness, initialize it
                _FRESH_AT[cache_key] = (ts, ts)

        return result

    cache[ck] = check_file_is_changed
    return check_file_is_changed


def build_file_reader(view=AsJSON):
    """
    Builds a file reader function which returns the result of the given
    view on the file contents.
    """
    def read_file(cache_key):
        """
        Reads a file and returns the result of calling a view's decode
        function on the file contents. Returns None if there's an error,
        and prints the error unless it's a FileNotFoundError.
        """
        filename = cache_key_filename(cache_key)
        try:
            with open(filename, 'r') as fin:
                return view.decode(fin.read())
        except IOError_or_FileNotFoundError:
            return None
        except Exception as e:
            sys.stderr.write(
                "[sync module] Exception viewing file:\n" + str(e) + '\n'
            )
            return None

    return read_file


#--------------------#
# File I/O functions #
#--------------------#

def cache_key_for(target, view):
    """
    Builds a hybrid cache key value with a certain target and view. The
    target filename must not include '::'.
    """
    if '::' in target:
        raise ValueError(
            "Cannot use a filename with a '::' in it as the target"
            " file."
        )
    return target + '::' + view.__name__


def cache_key_filename(cache_key):
    """
    Returns just the filename given a cache key.
    """
    filename = None
    for i in range(len(cache_key) - 1):
        if cache_key[i:i + 2] == '::':
            filename = cache_key[:i]
            break
    if filename is None:
        raise ValueError("Value '{}' is not a cache key!".format(cache_key))

    return filename


def load_or_get_cached(
    filename,
    view=AsJSON,
    missing=Exception,
    assume_fresh=0
):
    """
    Reads the given file, returning its contents as a string. Doesn't
    actually do that most of the time. Instead, it will return a cached
    value. And instead of returning the contents of the file as a
    string, it returns the result of running the given view function on
    the file's contents (decoded as a string). And actually, it caches
    the view result, not the file contents, to save time reapplying the
    view. The default view is AsJSON, which loads the file contents as
    JSON and creates a Python object.

    The __name__ of the view class will be used to compute a cache key
    for that view; avoid view name collisions.

    If the file on disk is newer than the cache, re-reads and re-caches
    the file. If assume_fresh is set to a positive number, then the file
    time on disk isn't even checked if the most recent check was
    performed less than that many seconds ago.

    If the file is missing, an exception would normally be raised, but
    if the `missing` value is provided as something other than
    `Exception`, a deep copy of that value will be returned instead.

    Note: On a cache hit, a deep copy of the cached value is returned, so
    modifying that value should not affect what is stored in the cache.
    """

    # Figure out our view object (& cache key):
    if view is None:
        view = AsIs

    cache_key = cache_key_for(filename, view)

    # Build functions for checking freshness and reading the file
    check_mtime = build_file_freshness_checker(missing, assume_fresh)
    read_file = build_file_reader(view)

    return _gen_or_get_cached(
        _CACHE_LOCK,
        _CACHE,
        cache_key,
        check_mtime,
        read_file
    )


#----------------------#
# Core caching routine #
#----------------------#

class AbortGeneration:
    """
    Class to signal that generation of a cached item should not proceed.
    Holds a default value to return instead.
    """
    def __init__(self, replacement):
        self.replacement = replacement


class NotInCache:
    """
    Placeholder for recognizing that a value is not in the cache (when
    e.g., None might be a valid cache value).
    """
    pass


def _gen_or_get_cached(
    lock,
    cache,
    cache_key,
    check_dirty,
    result_generator
):
    """
    Common functionality that uses a reentrant lock and a cache
    dictionary to return a cached value if the cached value is fresh. The
    value from the cache is deep-copied before being returned, so that
    any modifications to the returned value shouldn't alter the cache.
    Parameters are:

        lock: Specifies the lock to use. Should be a threading.RLock.
        cache: The cache dictionary.
        cache_key: String key for this cache item.
        check_dirty: Function which will be given the cache_key and a
            timestamp and must return True if the cached value (created
            at that instant) is dirty (needs to be updated) and False
            otherwise. May also return an AbortGeneration instance with a
            default value inside to be returned directly. If there is no
            cached value, check_dirty will be given a timestamp of None.
        result_generator: Function to call to build a new result if the
            cached value is stale. This new result will be cached. It
            will be given the cache_key as a parameter.
    """
    with lock:
        # We need to read the file contents and return them.
        cache_ts, cached = cache.get(cache_key, (None, NotInCache))
        safe_cached = copy.deepcopy(cached)

    # Use the provided function to check if this cache key is dirty.
    # No point in story the missing value we return since the dirty
    # check would presumably still come up True in the future.
    is_dirty = check_dirty(cache_key, cache_ts)
    if isinstance(is_dirty, AbortGeneration):
        # check_fresh calls for an abort: return replacement value
        return is_dirty.replacement
    elif not is_dirty and cached != NotInCache:
        # Cache is fresh: return cached value
        return safe_cached
    else:
        # Cache is stale

        # Get timestamp before we even start generating value:
        ts = time.time()

        # Generate reuslt:
        result = result_generator(cache_key)

        # Safely store new result value + timestamp in cache:
        with lock:
            cache[cache_key] = (ts, result)
            # Don't allow outside code to mess with internals of
            # cached value (JSON results could be mutable):
            safe_result = copy.deepcopy(result)

        # Return fresh deep copy of cached value:
        return safe_result


#-----------------#
# Setup functions #
#-----------------#

_REDIS = None
"""
The connection to the REDIS server.
"""

_CONFIG = None
"""
The flask app's configuration object.
"""


def init(config, key=None):
    """
    `init` should be called once per process, ideally early in the life of
    the process, like right after importing the module. Calling
    some functions before `init` will fail. A file named 'redis-pw.conf'
    should exist unless a key is given (should be a byte-string). If
    'redis-pw.conf' doesn't exist, it will be created.
    """
    global _REDIS, _CONFIG, _EVAL_BASE

    # Store config object
    _CONFIG = config

    # Compute evaluation base directory based on init-time CWD
    _EVAL_BASE = os.path.join(os.getcwd(), _CONFIG["EVALUATION_BASE"])

    # Grab port from config
    port = config.get("STORAGE_PORT", 51723)

    # Redis configuration filenames
    rconf_file = "potluck-redis.conf"
    ruser_file = "potluck-redis-user.acl"
    rport_file = "potluck-redis-port.conf"
    rpid_file = "potluck-redis.pid"
    rlog_file = "potluck-redis.log"

    # Check for redis config file
    if not os.path.exists(rconf_file):
        raise IOError_or_FileNotFoundError(
            "Unable to find Redis configuration file '{}'.".format(
                rconf_file
            )
        )

    # Check that conf file contains required stuff
    # TODO: More flexibility about these things?
    with open(rconf_file, 'r') as fin:
        rconf = fin.read()
        adir = 'aclfile "{}"'.format(ruser_file)
        if adir not in rconf:
            raise ValueError(
                (
                    "Redis configuration file '{}' is missing an ACL"
                    " file directive for the ACL file. It needs to use"
                    " '{}'."
                ).format(rconf_file, adir)
            )

        incl = "include {}".format(rport_file)
        if incl not in rconf:
            raise ValueError(
                (
                    "Redis configuration file '{}' is missing an include"
                    " for the port file. It needs to use '{}'."
                ).format(rconf_file, incl)
            )

        pdecl = 'pidfile "{}"'.format(rpid_file)
        if pdecl not in rconf:
            raise ValueError(
                (
                    "Redis configuration file '{}' is missing the"
                    " correct PID file directive '{}'."
                ).format(rconf_file, pdecl)
            )

        ldecl = 'logfile "{}"'.format(rlog_file)
        if ldecl not in rconf:
            raise ValueError(
                (
                    "Redis configuration file '{}' is missing the"
                    " correct log file directive '{}'."
                ).format(rconf_file, ldecl)
            )

    # Get storage key:
    if key is None:
        try:
            if os.path.exists(ruser_file):
                with open(ruser_file, 'r') as fin:
                    key = fin.read().strip().split()[-1][1:]
            else:
                print(
                    "Creating new Redis user file '{}'.".format(
                        ruser_file
                    )
                )
                # b32encode here makes it more readable
                key = base64.b32encode(os.urandom(64)).decode("ascii")
                udecl = "user default on +@all ~* >{}".format(key)
                with open(ruser_file, 'w') as fout:
                    fout.write(udecl)
        except Exception:
            raise IOError_or_FileNotFoundError(
                "Unable to access user file '{}'.".format(ruser_file)
            )

    # Double-check port, or write port conf file
    if os.path.exists(rport_file):
        with open(rport_file, 'r') as fin:
            portstr = fin.read().strip().split()[1]
        try:
            portconf = int(portstr)
        except Exception:
            portconf = portstr

        if portconf != port:
            raise ValueError(
                (
                    "Port was specified as {}, but port conf file"
                    " already exists and says port should be {}."
                    " Delete the port conf file '{}' to re-write it."
                ).format(repr(port), repr(portconf), rport_file)
            )
    else:
        # We need to write the port into the config file
        with open(rport_file, 'w') as fout:
            fout.write("port " + str(port))

    _REDIS = redis.Redis(
        'localhost',
        port,
        password=key,
        decode_responses=True
    )
    # Attempt to connect; if that fails, attempt to start a new Redis
    # server and attempt to connect again. Abort if we couldn't start
    # the server.
    print("Attempting to connect to Redis server...")
    try:
        _REDIS.exists('test') # We just want to not trigger an error
        print("...connected successfully.")
    except redis.exceptions.ConnectionError: # nobody to connect to
        _REDIS = None
    except redis.exceptions.ResponseError: # bad password
        raise ValueError(
            "Your authentication key is not correct. Make sure"
            " you're not sharing the port you chose with another"
            " process!"
        )

    if _REDIS is None:
        print("...failed to connect...")
        if os.path.exists(rpid_file):
            print(
                (
                    "...a Redis PID file already exists at '{}', but we"
                    " can't connect. Please shut down the old Redis"
                    " server first, or clean up the PID file if it"
                    " crashed."
                ).format(rpid_file)
            )
            raise ValueError(
                "Aborting server startup due to existing PID file."
            )

        # Try to start a new redis server...
        print("...starting Redis...")
        try:
            subprocess.Popen(["redis-server", rconf_file])
        except OSError:
            # If running through e.g. Apache and this command fails, you
            # can try to start it manually, so we point that out
            if len(shlex.split(rconf_file)) > 1:
                rconf_arg = "'" + rconf_file.replace("'", r"\'") + "'"
            else:
                rconf_arg = rconf_file
            sys.stdout.write(
                (
                    "Note: Failed to start redis-server with an"
                    " OSError.\nYou could try to manually launch the"
                    " server by running:\nredis-server {}"
                ).format(rconf_arg)
            )
            raise
        time.sleep(0.2) # try to connect pretty quickly
        print("...we hope Redis is up now...")

        if not os.path.exists(rpid_file):
            print(
                (
                    "...looks like Redis failed to launch; check '{}'..."
                ).format(rlog_file)
            )

        # We'll try a second time to connect
        _REDIS = redis.Redis(
            'localhost',
            port,
            password=key,
            decode_responses=True
        )
        print("Reattempting connection to Redis server...")
        try:
            _REDIS.exists('test') # We just want to not get an error
            print("...connected successfully.")
        except redis.exceptions.ConnectionError: # Not ready yet
            print("...not ready on first attempt...")
            _REDIS = None
        except redis.exceptions.ResponseError: # bad password
            raise ValueError(
                "Your authentication key is not correct. Make sure"
                " you're not sharing the port you chose with another"
                " process!"
            )

        # We'll make one final attempt
        if _REDIS is None:
            time.sleep(2) # Give it plenty of time

            # Check for PID file
            if not os.path.exists(rpid_file):
                print(
                    (
                        "...looks like Redis is still not running;"
                        " check '{}'..."
                    ).format(rlog_file)
                )

            # Set up connection object
            _REDIS = redis.Redis(
                'localhost',
                port,
                password=key,
                decode_responses=True
            )
            # Attempt to connect
            print(
                "Reattempting connection to Redis server (last"
                " chance)..."
            )
            try:
                _REDIS.exists('test') # We just want to not get an error
                print("...connected successfully.")
            except redis.exceptions.ResponseError: # bad password
                raise ValueError(
                    "Your authentication key is not correct. Make sure"
                    " you're not sharing the port you chose with another"
                    " process!"
                )
            # This time, we'll let a connection error bubble out

    # At this point, _REDIS is a working connection.
