"""
sceneTest rubric specification

Peter Mawhorter 2021-6-28
"""

from potluck import specifications as spec

# Require some kind of turtleBeads import (since this will also pull in
# turtle stuff, we don't require a separate turtle import.
spec.Import("turtleBeads", 'any')

for fcn in [
    ["forward", "fd", "backward", "bk", "back"],
    ["left", "lt", "right", "rt"],
]:
    spec.FunctionCall(fcn, limits=[1, None])

for fcn in [
    "drawCircle",
    ["pencolor", "color"],
    "begin_fill",
    "end_fill"
]:
    spec.FunctionCall(fcn, limits=[1, None], category="extra")


# Misc goals

spec.NoParseErrors()

# Construct our rubric
rubric = spec.rubric()


# Specifications tests using the meta module:
from potluck import meta # noqa E402

meta.example("perfect")

meta.example("imperfect")

meta.expect("failed", "import the turtleBeads module")
meta.expect("failed", "call left")
meta.expect("failed", "call drawCircle")
meta.expect("failed", "call begin_fill")
meta.expect("failed", "call end_fill")
