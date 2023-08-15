"""
Names: Peter Mawhorter
Date: 2021-8-28
Purpose: Tests for simple demonstration of wavesynth module.
"""

# Tests using printTrack
import optimism as opt

import arpeggio

import wavesynth

m = opt.testFunction(wavesynth.printTrack)

wavesynth.resetTracks()
arpeggio.arpeggio(wavesynth.C4, 0.5)
m.case().checkPrintedLines(
    "a 0.5s keyboard note at C4 (60% vol)",
    "and a 0.5s keyboard note at E4 (60% vol)",
    "and a 0.5s keyboard note at G4 (60% vol)",
    "and a 0.5s keyboard note at E4 (60% vol)",
    "and a 0.5s keyboard note at C4 (60% vol)",
)


wavesynth.resetTracks()
arpeggio.arpeggio(wavesynth.B3, 0.3)
m.case().checkPrintedLines(
    "a 0.3s keyboard note at B3 (60% vol)",
    "and a 0.3s keyboard note at Eb4 (60% vol)",
    "and a 0.3s keyboard note at Gb4 (60% vol)",
    "and a 0.3s keyboard note at Eb4 (60% vol)",
    "and a 0.3s keyboard note at B3 (60% vol)",
)
