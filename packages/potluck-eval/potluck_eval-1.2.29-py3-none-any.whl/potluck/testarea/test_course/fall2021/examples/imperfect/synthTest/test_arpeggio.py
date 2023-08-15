"""
Names: Peter Mawhorter
Date: 2021-8-28
Purpose: Tests for simple demonstration of wavesynth module (IMPERFECT)
"""

# Tests using printTrack
import optimism as opt

import arpeggio

import wavesynth

m = opt.testFunction(wavesynth.printTrack)

arpeggio.arpeggio(wavesynth.C4, 0.5)
m.case().checkPrintedLines(
    "a 0.5s keyboard note at C4 (60% vol)",
    "and a 0.5s keyboard note at E4 (60% vol)",
    "and a 0.5s keyboard note at G4 (60% vol)",
    "and a 0.5s keyboard note at E4 (60% vol)",
    "and a 0.5s keyboard note at C4",  # missing volume value
)

# Only one test
