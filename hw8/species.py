###############################################################################

## You can import from score, theory, and any python system modules you want.

from .score import Note, Pitch, Rest, Interval, Ratio, Mode, import_score
from .theory import Analysis, Rule, timepoints
from copy import copy
from math import inf

## Settings for a species 1 analysis. Pass this to SpeciesAnalysis() if you
# are analyzing a species 1 score. See also: SpeciesAnalysis.
s1_settings = {
    ## Maximum number of melodic unisons allowed.
    'MAX_UNI': 1,
    ## Maximum number of melodic 4ths allowed.
    'MAX_4TH': 2,
    ## Maximum number of melodic 5ths allowed.
    'MAX_5TH': 1,
    ## Maximum number of melodic 6ths allowed.
    'MAX_6TH': 0,
    ## Maximum number of melodic 7ths allowed.
    'MAX_7TH': 0,
    ## Maximum number of melodic 8vas allowed.
    'MAX_8VA': 0,
    ## Maximum number of leaps larger than a 3rd.
    'MAX_LRG': 2,
    ## Maximum number of consecutive melodic intervals moving in same direction.
    'MAX_SAMEDIR': 3,
    ## Maximum number of parallel consecutive harmonic 3rds/6ths.
    'MAX_PARALLEL': 3,
    ## Maximum number of consecutive leaps of any type.
    'MAX_CONSEC_LEAP': 2,
    ## Smallest leap demanding recovery step in opposite direction.
    'STEP_THRESHOLD': 5,
    # List of allowed starting scale degrees of a CP that is above the CF.
    'START_ABOVE': [1, 5],
    # List of allowed starting scale degrees of a CP that is below the CF.
    'START_BELOW': [1],
    # List of allowed melodic cadence patterns for the CP.
    'CADENCE_PATTERNS': [[2, 1], [7, 1]]
}

## Settings for species 2 analysis. Pass this to SpeciesAnalysis() if you
# are analyzing a second species score. See also: SpeciesAnalysis.
s2_settings = copy(s1_settings)
s2_settings['START_ABOVE'] = [1, 3, 5]
s2_settings['MAX_4TH'] = inf  # no limit on melodic fourths
s2_settings['MAX_5TH'] = inf  # no limit on melodic fifths
s2_settings['MAX_UNI'] = 0  # no melodic unisons allowed

## A list of all the possible result strings your analysis can generate.
# The {} marker in each string will always receive the 1-based integer index
# of the left-side time point that contains the offending issue. For example,
# if the first timepoint (e.g. self.timepoints[0]) contained an illegal
# starting pitch the message would be: 'At 1: forbidden starting pitch'
# Note: the variable result_strings does not need to be used by your code,
# it simply contains the list of all the result strings ;)
result_strings = [
    # VERTICAL RESULTS
    'At #{}: direct unisons',
    'At #{}: direct fifths',
    'At #{}: direct octaves',
    'At #{}: indirect unisons',
    'At #{}: indirect fifths',
    'At #{}: indirect octaves',
    'At #{}: direct unisons in cantus firmus notes',  # if species 2
    'At #{}: direct fifths in cantus firmus notes',  # if species 2
    'At #{}: direct octaves in cantus firmus notes',  # if species 2
    'At #{}: voice overlap',
    'At #{}: voice crossing',
    'At #{}: forbidden weak beat dissonance',  # vertical dissonance
    'At #{}: forbidden strong beat dissonance',  # vertical dissonance
    'At #{}: too many consecutive parallel intervals',  # parallel vertical intervals

    # MELODIC RESULTS
    'At #{}: forbidden starting pitch',
    'At #{}: forbidden rest',
    'At #{}: forbidden duration',
    'At #{}: missing melodic cadence',
    'At #{}: forbidden non-diatonic pitch',
    'At #{}: dissonant melodic interval',
    'At #{}: too many melodic unisons',  # 'MAX_UNI' setting
    'At #{}: too many leaps of a fourth',  # 'MAX_4TH' setting
    'At #{}: too many leaps of a fifth',  # 'MAX_5TH' setting
    'At #{}: too many leaps of a sixth',  # 'MAX_6TH' setting
    'At #{}: too many leaps of a seventh',  # 'MAX_7TH' setting
    'At #{}: too many leaps of an octave',  # 'MAX_8VA' setting
    'At #{}: too many large leaps',  # 'MAX_LRG' setting
    'At #{}: too many consecutive leaps'  # 'MAX_CONSEC_LEAP' setting
    'At #{}: too many consecutive intervals in same direction',  # 'MAX_SAMEDIR' setting
    'At #{}: too many consecutive parallel intervals',  # 'MAX_PARALLEL' setting
    'At #{}: missing reverse by step recovery',  # 'STEP_THRESHOLD' setting
    'At #{}: forbidden compound melodic interval',
]

class BufferRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Description goes here.')

    def apply(self):
        self.analysis.results.append('Hello World!')

class DirectUnisons(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Direct unisons are not allowed.')

    def apply(self):
        intervals = self.analysis.intervals
        illegal_intervals = []
        end_index = len(intervals) - 1
        if self.analysis.species == 2:
            end_index -= 1
        for i in range(end_index):
            if intervals[i] is None:
                continue
            if intervals[i].is_unison() and intervals[i + 1].is_unison():
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 2}: direct unisons')

class DirectFifths(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Direct fifths are not allowed.')

    def apply(self):
        intervals = self.analysis.intervals
        illegal_intervals = []
        end_index = len(intervals) - 1
        if self.analysis.species == 2:
            end_index -= 1
        for i in range(end_index):
            if intervals[i] is None:
                continue
            if intervals[i].is_fifth() and intervals[i + 1].is_fifth():
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 2}: direct fifths')


class DirectOctaves(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Direct octaves are not allowed.')

    def apply(self):
        intervals = self.analysis.intervals
        illegal_intervals = []
        end_index = len(intervals) - 1
        if self.analysis.species == 2:
            end_index -= 1
        for i in range(end_index):
            if intervals[i] is None:
                continue
            if intervals[i].is_octave() and intervals[i + 1].is_octave():
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 2}: direct octaves')


## A class that implements a species counterpoint analysis of a given score.
# A SpeciesAnalysis has at least 5 attributes, you will very likely add more:
#
# * self.score  The score being analyzed.
# * self.species  The integer species number of the analysis, either 1 or 2.
# * self.settings  A settings dict for the analysis, either s1_settings or s2_settings.
# * self.rules  An ordered list of Rules that constitute your analysis.
# * self.results  A list of strings (see below) that constitute your analysis findings.
#
# You should call your analysis like this:
#
#   score = import_score(species1_xmlfile)
#   analysis = SpeciesAnalysis(score, 1, s1_settings)
#   analysis.submit_to_grading()
class SpeciesAnalysis(Analysis):
    ## Initializes a species analysis.
    # @param score A score containing a two-part species composition.
    # @param species A counterpoint species number, either 1 or 2.
    # @param settings A settings dict, either s1_settings or s2_settings.
    def __init__(self, score, species, settings):
        ## Call the superclass and give it the score.
        super().__init__(score)
        if species not in [1, 2]:
            raise ValueError(f"'{species}' is not a valid species number 1 or 2.")
        ## The integer species number for the analysis.
        self.species = species
        ## A local copy of the analysis settings.
        self.settings = copy(settings)
        ## Add your rules to this list.
        self.rules = [DirectUnisons(self),
                      DirectFifths(self),
                      DirectOctaves(self)]
        ## A list of strings that represent the findings of your analysis.
        self.results = []

    ## Use this function to perform whatever setup actions your rules require.
    def setup(self, args, kwargs):
        self.tps = timepoints(self.score, span=True, measures=False)
        self.lower_voice = []
        self.upper_voice = []
        self.intervals = []
        self.partids = [key[: 2] for key in list(self.tps[0].nmap.keys())]
        if self.score.get_part(self.partids[0]).name == 'CF':
            self.cflow = False
        else:
            self.cflow = True

        print(self.cflow)

        for tp in self.tps:
            nmap = tp.nmap
            keys = list(nmap.keys())
            upper_note = nmap.get(keys[0])
            lower_note = nmap.get(keys[1])

            if isinstance(lower_note, Rest):
                self.lower_voice.append(None)
            else:
                self.lower_voice.append(lower_note.pitch)
            if isinstance(upper_note, Rest):
                self.upper_voice.append(None)
            else:
                self.upper_voice.append(upper_note.pitch)
            if not isinstance(upper_note, Rest) and not isinstance(lower_note, Rest):
                self.intervals.append(Interval(lower_note.pitch, upper_note.pitch))
            else:
                self.intervals.append(None)

    ## This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        self.analyze()
        return self.results


###############################################################################

# A short list of files that contain lots of issues (see comments below)

samples = ['2-034-A_zawang2.musicxml', '2-028-C_hanzhiy2.musicxml', '2-000-B_sz18.musicxml',
           '2-003-A_cjrosas2.musicxml', '2-021-B_erf3.musicxml', '1-018-C_ajyanez2.musicxml',
           '2-003_A_chchang6.musicxml', '1-019-A_ajyanez2.musicxml', '2-009-C_mamn2.musicxml',
           '1-005-A_hanzhiy2.musicxml', '2-010-B_mamn2.musicxml', '1-008-C_davidx2.musicxml',
           '1-030_C_chchang6.musicxml', '2-034-C_zawang2.musicxml', '1-011-B_weikeng2.musicxml',
           '2-029-A_hanzhiy2.musicxml', '1-037-A_sz18.musicxml', '1-012-B_erf3.musicxml',
           '1-030-C_cjrosas2.musicxml', '2-009-B_mamn2.musicxml', '2-021-C_erf3.musicxml']

## Direct (parallel) 5ths, 8vas and unisons:
#     '1-037-A_sz18.musicxml'
#     '1-030-C_cjrosas2.musicxml'
#     '2-000-B_sz18.musicxml'
## Direct motion measure to measure (species 2):
#     '2-034-C_zawang2.musicxml'
#     '2-021-C_erf3.musicxml'
## Indirect (hidden) 5ths and 8vas:
#     '1-030_C_chchang6.musicxml'
#     '1-008-C_davidx2.musicxml'
#     '1-030-C_cjrosas2.musicxml'
#     '1-011-B_weikeng2.musicxml'
## Voice overlap:
#     '1-005-A_hanzhiy2.musicxml'
#     '1-019-A_ajyanez2.musicxml'
## Maximum parallel interval:
#     '1-037-A_sz18.musicxml'
## Voice crossing:
#     '1-019-A_ajyanez2.musicxml'
## Disjunction:
#     '1-008-C_davidx2.musicxml'
## Weak beat dissonance not passing tone (species 2):
#     '2-000-B_sz18.musicxml'
#     '2-034-C_zawang2.musicxml'
#     '2-021-C_erf3.musicxml'
## Strong beat dissonance (species 1 and 2):
#     '2-000-B_sz18.musicxml'
#     '2-034-C_zawang2.musicxml'
## Wrong durations:
#     '2-009-C_mamn2.musicxml'
#     '2-034-A_zawang2.musicxml'
#     '2-021-B_erf3.musicxml'
#     '2-009-B_mamn2.musicxml'
#     '2-021-C_erf3.musicxml'
## Not diatonic:
#     '1-018-C_ajyanez2.musicxml'
#     '2-003-A_cjrosas2.musicxml'
#     '2-003_A_chchang6.musicxml'
## Starting pitch:
#     '2-028-C_hanzhiy2.musicxml'
#     '1-012-B_erf3.musicxml'
## Melodic cadence:
#     '1-018-C_ajyanez2.musicxml'
#     '1-030_C_chchang6.musicxml'
#     '2-034-A_zawang2.musicxml'
## Too many 'x':
#     '2-029-A_hanzhiy2.musicxml'
#     '2-003_A_chchang6.musicxml'
#     '2-010-B_mamn2.musicxml'
## Reverse after leap:
#     '2-029-A_hanzhiy2.musicxml'
#     '2-010-B_mamn2.musicxml'