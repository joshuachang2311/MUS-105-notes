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
s2_settings['MAX_UNI'] = 0    # no melodic unisons allowed

## A list of all the possible result strings your analysis can generate.
# The {} marker in each string will always receive the 1-based integer index
# of the left-side time point that contains the offending issue. For example,
# if the first timepoint (e.g. self.timepoints[0]) contained an illegal
# starting pitch the message would be: 'At 1: forbidden starting pitch'
# Note: the variable result_strings does not need to be used by your code,
# it simply contains the list of all the result strings ;)
result_strings = [
    # VERTICAL RESULTS
    'At #{}: consecutive unisons',
    'At #{}: consecutive fifths',
    'At #{}: consecutive octaves',
    'At #{}: direct unisons',
    'At #{}: direct fifths',
    'At #{}: direct octaves',
    'At #{}: consecutive unisons in cantus firmus notes',  # if species 2
    'At #{}: consecutive fifths in cantus firmus notes',   # if species 2
    'At #{}: consecutive octaves in cantus firmus notes',  # if species 2
    'At #{}: voice overlap',
    'At #{}: voice crossing',
    'At #{}: forbidden weak beat dissonance',   # vertical dissonance
    'At #{}: forbidden strong beat dissonance', # vertical dissonance
    'At #{}: too many consecutive parallel intervals',  # parallel vertical intervals

    # MELODIC RESULTS
    'At #{}: forbidden starting pitch',
    'At #{}: forbidden rest', 
    'At #{}: forbidden duration',   
    'At #{}: missing melodic cadence',
    'At #{}: forbidden non-diatonic pitch',
    'At #{}: dissonant melodic interval',
    'At #{}: too many melodic unisons',         # 'MAX_UNI' setting
    'At #{}: too many leaps of a fourth',       # 'MAX_4TH' setting
    'At #{}: too many leaps of a fifth',        # 'MAX_5TH' setting
    'At #{}: too many leaps of a sixth',        # 'MAX_6TH' setting
    'At #{}: too many leaps of a seventh',      # 'MAX_7TH' setting
    'At #{}: too many leaps of an octave',      # 'MAX_8VA' setting
    'At #{}: too many large leaps',             # 'MAX_LRG' setting
    'At #{}: too many consecutive leaps'        # 'MAX_CONSEC_LEAP' setting
    'At #{}: too many consecutive intervals in same direction', # 'MAX_SAMEDIR' setting
    'At #{}: missing reverse by step recovery', # 'STEP_THRESHOLD' setting
    'At #{}: forbidden compound melodic interval',
    ]


def is_melodic_dissonance(interval):
    return interval.is_seventh() or not (interval.is_major() or interval.is_minor() or interval.is_perfect())

def is_xlarge(interval):
    return interval.span > 3

def is_large(interval):
    return interval.span > 2

def is_leap(interval):
    return interval.span > 1

def is_dis(interval):
    return interval.is_diminished() or interval.is_augmented()


class ConsecutiveUnisons(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Consecutive unisons are not allowed.')

    def apply(self):
        species = self.analysis.species
        intervals = self.analysis.intervals
        lower_voice = self.analysis.lower_voice
        illegal_intervals = []
        end_index = len(intervals) - 1
        for i in range(end_index):
            if intervals[i] is None:
                continue
            if intervals[i].is_unison() and intervals[i + 1].is_unison():
                if i != end_index or species == 1:
                    illegal_intervals.append(i)
                elif lower_voice[i] != lower_voice[i + 1]:
                    illegal_intervals.append(i)
        for i in illegal_intervals:
            if f'At #{i + 1}: forbidden duration' in self.analysis.results:
                pass
            elif f'At #{i + 2}: forbidden duration' in self.analysis.results:
                pass
            else:
                self.analysis.results.append(f'At #{i + 1}: consecutive unisons')

class ConsecutiveFifths(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Consecutive fifths are not allowed.')

    def apply(self):
        species = self.analysis.species
        intervals = self.analysis.intervals
        lower_voice = self.analysis.lower_voice
        illegal_intervals = []
        end_index = len(intervals) - 1
        for i in range(end_index):
            if intervals[i] is None:
                continue
            if intervals[i].is_fifth() and intervals[i + 1].is_fifth():
                if i != end_index or species == 1:
                    illegal_intervals.append(i)
                elif lower_voice[i] != lower_voice[i + 1]:
                    illegal_intervals.append(i)
        for i in illegal_intervals:
            if f'At #{i + 1}: forbidden duration' in self.analysis.results:
                pass
            elif f'At #{i + 2}: forbidden duration' in self.analysis.results:
                pass
            else:
                self.analysis.results.append(f'At #{i + 1}: consecutive fifths')

class ConsecutiveOctaves(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Consecutive octaves are not allowed.')

    def apply(self):
        species = self.analysis.species
        intervals = self.analysis.intervals
        lower_voice = self.analysis.lower_voice
        illegal_intervals = []
        end_index = len(intervals) - 1
        for i in range(end_index):
            if intervals[i] is None:
                continue
            if intervals[i].is_octave() and intervals[i + 1].is_octave():
                if i != end_index or species == 1:
                    illegal_intervals.append(i)
                elif lower_voice[i] != lower_voice[i + 1]:
                    illegal_intervals.append(i)
        for i in illegal_intervals:
            if f'At #{i + 1}: forbidden duration' in self.analysis.results:
                pass
            elif f'At #{i + 2}: forbidden duration' in self.analysis.results:
                pass
            else:
                self.analysis.results.append(f'At #{i + 1}: consecutive octaves')


class DirectUnisons(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Direct unisons are not allowed.')

    def apply(self):
        intervals = self.analysis.intervals
        lower_voice = self.analysis.lower_voice
        upper_voice = self.analysis.upper_voice
        illegal_intervals = []
        end_index = len(intervals) - 1
        for i in range(1, end_index):
            if intervals[i] is None:
                continue
            if intervals[i].is_unison():
                lower_interval = Interval(lower_voice[i - 1], lower_voice[i])
                upper_interval = Interval(upper_voice[i - 1], upper_voice[i])
                if not is_leap(upper_interval):
                    pass
                elif lower_interval.sign != upper_interval.sign:
                    pass
                elif lower_interval.span == upper_interval.span:
                    pass
                elif not lower_interval.is_unison():
                    illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i}: direct unisons')

class DirectFifths(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Direct fifths are not allowed.')

    def apply(self):
        intervals = self.analysis.intervals
        lower_voice = self.analysis.lower_voice
        upper_voice = self.analysis.upper_voice
        illegal_intervals = []
        end_index = len(intervals) - 1
        for i in range(1, end_index):
            if intervals[i] is None:
                continue
            if intervals[i].is_fifth():
                lower_interval = Interval(lower_voice[i - 1], lower_voice[i])
                upper_interval = Interval(upper_voice[i - 1], upper_voice[i])
                if not is_leap(upper_interval):
                    pass
                elif lower_interval.sign != upper_interval.sign:
                    pass
                elif lower_interval.span == upper_interval.span:
                    pass
                elif not lower_interval.is_unison():
                    illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i}: direct fifths')

class DirectOctaves(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Direct octaves are not allowed.')

    def apply(self):
        intervals = self.analysis.intervals
        lower_voice = self.analysis.lower_voice
        upper_voice = self.analysis.upper_voice
        illegal_intervals = []
        end_index = len(intervals) - 1
        for i in range(1, end_index):
            if intervals[i] is None:
                continue
            if intervals[i].is_octave():
                lower_interval = Interval(lower_voice[i - 1], lower_voice[i])
                upper_interval = Interval(upper_voice[i - 1], upper_voice[i])
                if not is_leap(upper_interval):
                    pass
                elif lower_interval.sign != upper_interval.sign:
                    pass
                elif lower_interval.span == upper_interval.span:
                    pass
                elif not lower_interval.is_unison():
                    illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i}: direct octaves')


class CfConsecUnisons(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Consecutive unisons in cantus firmus notes are not allowed.')

    def apply(self):
        species = self.analysis.species
        intervals = self.analysis.intervals
        cp_dur = self.analysis.cp_dur
        illegal_intervals = []
        start_index = 0
        end_index = len(intervals) - 2
        if species == 1:
            return
        if cp_dur[0] == Ratio(1, 1):
            start_index = 1
            if intervals[0] is None:
                pass
            elif intervals[0].is_unison() and intervals[1].is_unison():
                illegal_intervals.append(0)
        for i in range(start_index, end_index, 2):
            if intervals[i] is None:
                continue
            if intervals[i].is_unison() and intervals[i + 2].is_unison():
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: consecutive unisons in cantus firmus notes')

class CfConsecFifths(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Consecutive fifths in cantus firmus notes are not allowed.')

    def apply(self):
        species = self.analysis.species
        intervals = self.analysis.intervals
        cp_dur = self.analysis.cp_dur
        illegal_intervals = []
        start_index = 0
        end_index = len(intervals) - 2
        if species == 1:
            return
        if cp_dur[0] == Ratio(1, 1):
            start_index = 1
            if intervals[0] is None:
                pass
            elif intervals[0].is_fifth() and intervals[1].is_fifth():
                illegal_intervals.append(0)
        for i in range(start_index, end_index, 2):
            if intervals[i] is None:
                continue
            if intervals[i].is_fifth() and intervals[i + 2].is_fifth():
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: consecutive fifths in cantus firmus notes')

class CfConsecOctaves(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Consecutive octaves in cantus firmus notes are not allowed.')

    def apply(self):
        species = self.analysis.species
        intervals = self.analysis.intervals
        cp_dur = self.analysis.cp_dur
        illegal_intervals = []
        start_index = 0
        end_index = len(intervals) - 2
        if species == 1:
            return
        if cp_dur[0] == Ratio(1, 1):
            start_index = 1
            if intervals[0] is None:
                pass
            elif intervals[0].is_octave() and intervals[1].is_octave():
                illegal_intervals.append(0)
        for i in range(start_index, end_index, 2):
            if intervals[i] is None:
                continue
            if intervals[i].is_octave() and intervals[i + 2].is_octave():
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: consecutive octaves in cantus firmus notes')


class VoiceOverlap(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Voice overlap is not allowed.')

    def apply(self):
        illegal_intervals = []
        lower_voice = self.analysis.lower_voice
        upper_voice = self.analysis.upper_voice
        end_index = len(lower_voice) - 1
        for i in range(end_index):
            if lower_voice[i] is None or upper_voice[i] is None:
                continue
            if lower_voice[i + 1] > upper_voice[i] or upper_voice[i + 1] < lower_voice[i]:
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 2}: voice overlap')

class VoiceCrossing(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Voice overlap is not allowed.')

    def apply(self):
        illegal_intervals = []
        lower_voice = self.analysis.lower_voice
        upper_voice = self.analysis.upper_voice
        end_index = len(lower_voice)
        for i in range(end_index):
            if lower_voice[i] is None or upper_voice[i] is None:
                continue
            if lower_voice[i] > upper_voice[i]:
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: voice crossing')


class WeakBeatDissonance(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Weak beat dissonance has to be a passing tone.')

    def apply(self):
        illegal_intervals = []
        intervals = self.analysis.intervals
        cp_voice = self.analysis.cp_voice
        cp_dur = self.analysis.cp_dur
        end_index = len(intervals)
        species = self.analysis.species
        start_index = 1
        if species == 1:
            return
        if cp_dur[0] == Ratio(1, 1):
            start_index = 2
        for i in range(start_index, end_index, species):
            if intervals[i] is None:
                continue
            if intervals[i].span not in [0, 2, 4, 5, 7]:
                interval1 = Interval(cp_voice[i - 1], cp_voice[i])
                interval2 = Interval(cp_voice[i], cp_voice[i + 1])
                if not interval1.is_second() or not interval2.is_second():
                    illegal_intervals.append(i)
                elif interval1.sign != interval2.sign:
                    illegal_intervals.append(i)
            elif is_dis(intervals[i]):
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: forbidden weak beat dissonance')

class StrongBeatDissonance(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Strong beat dissonance is not allowed.')

    def apply(self):
        illegal_intervals = []
        intervals = self.analysis.intervals
        cp_dur = self.analysis.cp_dur
        end_index = len(intervals)
        species = self.analysis.species
        start_index = 0
        if species == 2 and cp_dur[0] == Ratio(1, 1):
            start_index = 1
            if intervals[0] is None:
                pass
            elif intervals[0].span not in [0, 2, 4, 5, 7] or is_dis(intervals[0]):
                illegal_intervals.append(0)
        for i in range(start_index, end_index, species):
            if intervals[i] is None:
                continue
            if intervals[i].span not in [0, 2, 4, 5, 7] or is_dis(intervals[i]):
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: forbidden strong beat dissonance')

class ConsecParallels(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many consecutive parallel intervals are not allowed.')

    def apply(self):
        max_consec = self.analysis.settings['MAX_PARALLEL']
        combo = 0
        current_span = None
        illegal_intervals = []
        intervals = self.analysis.intervals
        end_index = len(intervals)
        for i in range(0, end_index):
            if intervals[i] is None:
                continue
            if current_span is None:
                combo = 1
                current_span = intervals[i].span
            elif intervals[i].span != current_span:
                combo = 1
                current_span = intervals[i].span
            else:
                combo += 1
            if combo > max_consec and current_span in [2, 5]:
                illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: too many consecutive parallel intervals')


class ForbiddenStartingPitch(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Strong beat dissonance is not allowed.')

    def apply(self):
        species = self.analysis.species
        scale = self.analysis.key.scale()
        tonic = self.analysis.tonic
        lower_voice = self.analysis.lower_voice
        upper_voice = self.analysis.upper_voice
        if species == 1:
            lower_pnum = lower_voice[0].pnum()
            upper_pnum = upper_voice[0].pnum()
            if lower_pnum != tonic:
                self.analysis.results.append(f'At #{1}: forbidden starting pitch')
            elif scale.index(upper_pnum) not in [i - 1 for i in self.analysis.settings['START_ABOVE']]:
                self.analysis.results.append(f'At #{1}: forbidden starting pitch')
        else:
            has_rest = False
            lower_pnum = None
            upper_pnum = None
            for lower_pitch in lower_voice:
                if lower_pitch is None:
                    has_rest = True
                    continue
                lower_pnum = lower_pitch.pnum()
                break
            for upper_pitch in upper_voice:
                if upper_pitch is None:
                    has_rest = True
                    continue
                upper_pnum = upper_pitch.pnum()
                break
            if lower_pnum != tonic:
                self.analysis.results.append(f'At #{2 if has_rest else 1}: forbidden starting pitch')
            elif scale.index(upper_pnum) not in [i - 1 for i in self.analysis.settings['START_ABOVE']]:
                self.analysis.results.append(f'At #{2 if has_rest else 1}: forbidden starting pitch')

class ForbiddenRest(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Rest in cantus firmus notes or after the first beat of counterpoint is not allowed.')

    def apply(self):
        illegal_intervals = []
        species = self.analysis.species
        cflow = self.analysis.cflow
        lower_voice = self.analysis.lower_voice
        upper_voice = self.analysis.upper_voice
        if species == 1:
            end_index = len(lower_voice)
            for i in range(end_index):
                if lower_voice[i] is None or upper_voice[i] is None:
                    illegal_intervals.append(i)
        else:
            cf = []
            cp = []
            if cflow:
                cf = lower_voice
                cp = upper_voice
            else:
                cf = upper_voice
                cp = lower_voice
            end_index = len(lower_voice)
            if cf[0] is None:
                illegal_intervals.append(0)
            for i in range(1, end_index):
                if cf[i] is None or cp[i] is None:
                    illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: forbidden rest')

class ForbiddenDuration(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Durations that are not whole notes in 1st species or half notes in 2nd species'
                                   'counterpoint notes is not allowed.')

    def apply(self):
        illegal_intervals = []
        species = self.analysis.species
        cp_dur = self.analysis.cp_dur
        if species == 1:
            end_index = len(cp_dur)
            for i in range(end_index):
                if cp_dur[i] != Ratio(1, 1):
                    illegal_intervals.append(i)
        else:
            end_index = len(cp_dur)
            for i in range(end_index):
                if i < end_index - 2:
                    if cp_dur[i] != Ratio(1, 2):
                        illegal_intervals.append(i)
                elif i == end_index - 2:
                    if cp_dur[i] not in [Ratio(1, 1), Ratio(1, 2)]:
                        illegal_intervals.append(i)
                elif i == end_index - 1:
                    if cp_dur[i] != Ratio(1, 1):
                        illegal_intervals.append(i)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: forbidden duration')


class MelodicCadence(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Melodic cadence is required.')

    def apply(self):
        illegal_intervals = []
        tonic = self.analysis.tonic
        cp_voice = self.analysis.cp_voice
        if cp_voice[-1].pnum() != tonic:
            illegal_intervals.append(len(cp_voice) - 2)
        else:
            interval = Interval(cp_voice[-2], cp_voice[-1])
            if interval.is_ascending() and interval != Interval('m2'):
                illegal_intervals.append(len(cp_voice) - 2)
            elif interval.is_descending() and interval != Interval('-M2'):
                illegal_intervals.append(len(cp_voice) - 2)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: missing melodic cadence')

class NonDiatonicPitch(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Non-diatonic pitch is not allowed.')

    def apply(self):
        illegal_intervals = []
        cp_voice = self.analysis.cp_voice
        scale = self.analysis.key.scale()
        tonic = self.analysis.tonic

        end_index = len(cp_voice)
        for i in range(end_index):
            if cp_voice[i] is None:
                continue
            if i == end_index - 2:
                if cp_voice[i].pnum() not in scale and Interval('m2').transpose(cp_voice[i].pnum()) != tonic:
                    illegal_intervals.append(i)
            elif i == end_index - 3:
                if cp_voice[i].pnum() not in scale and Interval('m3').transpose(cp_voice[i].pnum()) != tonic:
                    illegal_intervals.append(i)
            else:
                if cp_voice[i].pnum() not in scale:
                    illegal_intervals.append(i)

        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: forbidden non-diatonic pitch')

class DissonantMelodicInterval(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Dissonant melodic interval is not allowed.')

    def apply(self):
        illegal_intervals = []
        cf = []
        cp = []
        cflow = self.analysis.cflow
        if cflow:
            cf = self.analysis.lower_voice
            cp = self.analysis.upper_voice
        else:
            cf = self.analysis.upper_voice
            cp = self.analysis.lower_voice
        end_index = len(cf) - 1
        for i in range(end_index):
            if cp[i] is None:
                continue
            interval1 = Interval(cf[i], cf[i + 1])
            interval2 = Interval(cp[i], cp[i + 1])
            if is_melodic_dissonance(interval1) or is_melodic_dissonance(interval2):
                illegal_intervals.append(i + 1)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i}: dissonant melodic interval')


class MaxUni(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many melodic unisons are not allowed.')

    def apply(self):
        illegal_intervals = []
        max_unisons = self.analysis.settings['MAX_UNI']
        n_unisons = 0
        cp_voice = self.analysis.cp_voice
        end_index = len(cp_voice) - 1
        for i in range(end_index):
            if cp_voice[i] is None:
                continue
            interval = Interval(cp_voice[i], cp_voice[i + 1])
            if interval == Interval('P1'):
                n_unisons += 1
                if n_unisons > max_unisons:
                    illegal_intervals.append(i)

        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: too many melodic unisons')

class Max4th(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many leaps of a fourth are not allowed.')

    def apply(self):
        illegal_intervals = []
        max_fourths = self.analysis.settings['MAX_4TH']
        n_fourths = 0
        cp_voice = self.analysis.cp_voice
        end_index = len(cp_voice) - 1
        for i in range(end_index):
            if cp_voice[i] is None:
                continue
            interval = Interval(cp_voice[i], cp_voice[i + 1])
            if interval.is_fourth():
                n_fourths += 1
                if n_fourths > max_fourths:
                    illegal_intervals.append(i)

        for i in illegal_intervals:
            if f'At #{i + 1}: too many large leaps' not in self.analysis.results:
                self.analysis.results.append(f'At #{i + 1}: too many leaps of a fourth')

class Max5th(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many leaps of a fifth are not allowed.')

    def apply(self):
        illegal_intervals = []
        max_fifths = self.analysis.settings['MAX_5TH']
        n_fifths = 0
        cp_voice = self.analysis.cp_voice
        end_index = len(cp_voice) - 1
        for i in range(end_index):
            if cp_voice[i] is None:
                continue
            interval = Interval(cp_voice[i], cp_voice[i + 1])
            if interval.is_fifth():
                n_fifths += 1
                if n_fifths > max_fifths:
                    illegal_intervals.append(i)
        for i in illegal_intervals:
            if f'At #{i + 1}: too many large leaps' not in self.analysis.results:
                self.analysis.results.append(f'At #{i + 1}: too many leaps of a fifth')

class Max6th(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many leaps of a sixth are not allowed.')

    def apply(self):
        illegal_intervals = []
        max_sixths = self.analysis.settings['MAX_6TH']
        n_sixths = 0
        cp_voice = self.analysis.cp_voice
        end_index = len(cp_voice) - 1
        for i in range(end_index):
            if cp_voice[i] is None:
                continue
            interval = Interval(cp_voice[i], cp_voice[i + 1])
            if interval.is_sixth():
                n_sixths += 1
                if n_sixths > max_sixths:
                    illegal_intervals.append(i)

        for i in illegal_intervals:
            if f'At #{i + 1}: too many large leaps' not in self.analysis.results:
                self.analysis.results.append(f'At #{i + 1}: too many leaps of a sixth')

class Max7th(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many leaps of a seventh are not allowed.')

    def apply(self):
        illegal_intervals = []
        max_sevenths = self.analysis.settings['MAX_7TH']
        n_sevenths = 0
        cp_voice = self.analysis.cp_voice
        end_index = len(cp_voice) - 1
        for i in range(end_index):
            if cp_voice[i] is None:
                continue
            interval = Interval(cp_voice[i], cp_voice[i + 1])
            if interval.is_seventh():
                n_sevenths += 1
                if n_sevenths > max_sevenths:
                    illegal_intervals.append(i)

        for i in illegal_intervals:
            if f'At #{i + 1}: too many large leaps' not in self.analysis.results:
                self.analysis.results.append(f'At #{i + 1}: too many leaps of a seventh')

class Max8va(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many leaps of an octave are not allowed.')

    def apply(self):
        illegal_intervals = []
        max_octaves = self.analysis.settings['MAX_8VA']
        n_octaves = 0
        cp_voice = self.analysis.cp_voice
        end_index = len(cp_voice) - 1
        for i in range(end_index):
            if cp_voice[i] is None:
                continue
            interval = Interval(cp_voice[i], cp_voice[i + 1])
            if interval.is_octave():
                n_octaves += 1
                if n_octaves > max_octaves:
                    illegal_intervals.append(i)

        for i in illegal_intervals:
            if f'At #{i + 1}: too many large leaps' not in self.analysis.results:
                self.analysis.results.append(f'At #{i + 1}: too many leaps of an octave')

class MaxLrg(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many large leaps are not allowed.')

    def apply(self):
        illegal_intervals = []
        max_larges = self.analysis.settings['MAX_LRG']
        n_larges = 0
        cp_voice = self.analysis.cp_voice
        end_index = len(cp_voice) - 1
        for i in range(end_index):
            if cp_voice[i] is None:
                continue
            interval = Interval(cp_voice[i], cp_voice[i + 1])
            if is_large(interval):
                n_larges += 1
                if n_larges > max_larges:
                    illegal_intervals.append(i)

        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: too many large leaps')


class MaxConsecLeap(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many consecutive leaps are not allowed.')

    def apply(self):
        illegal_intervals = []
        max_consec_leaps = self.analysis.settings['MAX_CONSEC_LEAP']
        consec_leaps = 0
        cf = []
        cp = []
        cp_dur = []
        species = self.analysis.species
        cflow = self.analysis.cflow
        if cflow:
            cf = self.analysis.lower_voice
            cp = self.analysis.upper_voice
            cp_dur = self.analysis.upper_dur
        else:
            cf = self.analysis.upper_voice
            cp = self.analysis.lower_voice
            cp_dur = self.analysis.lower_dur
        end_index = len(cf) - 1
        for i in range(end_index):
            interval = Interval(cf[i], cf[i + 1])
            if is_leap(interval):
                consec_leaps += 1
                if consec_leaps > max_consec_leaps:
                    illegal_intervals.append(i + 1)
            else:
                consec_leaps = 0
        for i in range(end_index):
            if cp[i] is None:
                continue
            interval = Interval(cp[i], cp[i + 1])
            if is_leap(interval):
                consec_leaps += 1
                if consec_leaps > max_consec_leaps:
                    if i + 1 not in illegal_intervals:
                        illegal_intervals.append(i + 1)
            else:
                consec_leaps = 0
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i}: too many consecutive leaps')

class MaxSameDir(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Too many consecutive intervals in same direction is not allowed.')

    def apply(self):
        illegal_intervals = []
        max_samedir = self.analysis.settings['MAX_SAMEDIR']
        consec_dir = 1
        cf = []
        cp = []
        cp_dur = []
        species = self.analysis.species
        cflow = self.analysis.cflow
        if cflow:
            cf = self.analysis.lower_voice
            cp = self.analysis.upper_voice
            cp_dur = self.analysis.upper_dur
        else:
            cf = self.analysis.upper_voice
            cp = self.analysis.lower_voice
            cp_dur = self.analysis.lower_dur
        if species == 1:
            end_index = len(cf) - 1
            for i in range(1, end_index):
                interval1 = Interval(cp[i - 1], cp[i])
                interval2 = Interval(cp[i], cp[i + 1])
                if interval1.sign == interval2.sign:
                    consec_dir += 1
                    if consec_dir > max_samedir:
                        illegal_intervals.append(i + 1)
                else:
                    consec_dir = 1
            consec_dir = 1
            for i in range(1, end_index):
                interval1 = Interval(cf[i - 1], cf[i])
                interval2 = Interval(cf[i], cf[i + 1])
                if interval1.sign == interval2.sign:
                    consec_dir += 1
                    if consec_dir > max_samedir:
                        if i + 1 not in illegal_intervals:
                            illegal_intervals.append(i + 1)
                else:
                    consec_dir = 1
        else:
            end_index = len(cf) - 1
            for i in range(1, end_index):
                if cp[i - 1] is None:
                    continue
                interval1 = Interval(cp[i - 1], cp[i])
                interval2 = Interval(cp[i], cp[i + 1])
                if interval1.sign == interval2.sign:
                    consec_dir += 1
                    if consec_dir > max_samedir:
                        if i + 1 not in illegal_intervals:
                            illegal_intervals.append(i + 1)
                else:
                    consec_dir = 1
            end_index = len(cf) - 2
            consec_dir = 1
            for i in range(2, end_index, 2):
                interval1 = Interval(cf[i - 2], cf[i])
                interval2 = Interval(cf[i], cf[i + 2])
                if interval1.sign == interval2.sign:
                    consec_dir += 1
                    if consec_dir > max_samedir:
                        if i + 2 not in illegal_intervals:
                            illegal_intervals.append(i + 2)
                else:
                    consec_dir = 1
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i}: too many consecutive intervals in same direction')

class StepRecovery(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Missing reverse by step recovery is not allowed.')

    def apply(self):
        illegal_intervals = []
        max_leap = self.analysis.settings['STEP_THRESHOLD'] - 1
        cf_voice = self.analysis.cf_voice
        cp_voice = self.analysis.cp_voice
        end_index = len(cf_voice) - 1
        for i in range(end_index):
            if cp_voice[i] is None:
                continue
            interval = Interval(cp_voice[i], cp_voice[i + 1])
            if interval.span >= max_leap:
                if i == end_index - 1:
                    illegal_intervals.append(i)
                else:
                    interval2 = Interval(cp_voice[i + 1], cp_voice[i + 2])
                    if not interval2.is_second() or interval2.sign == interval.sign:
                        illegal_intervals.append(i)

        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: missing reverse by step recovery')

class CompoundInterval(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Compound melodic interval is not allowed.')

    def apply(self):
        illegal_intervals = []
        cf = []
        cp = []
        cp_dur = []
        species = self.analysis.species
        cflow = self.analysis.cflow
        if cflow:
            cf = self.analysis.lower_voice
            cp = self.analysis.upper_voice
            cp_dur = self.analysis.upper_dur
        else:
            cf = self.analysis.upper_voice
            cp = self.analysis.lower_voice
            cp_dur = self.analysis.lower_dur
        if species == 1:
            end_index = len(cf) - 1
            for i in range(end_index):
                interval1 = Interval(cf[i], cf[i + 1])
                interval2 = Interval(cp[i], cp[i + 1])
                if interval1.is_compound() or interval2.is_compound():
                    illegal_intervals.append(i)
        else:
            end_index = len(cf) - 2
            for i in range(end_index):
                if cp[i] is not None:
                    interval = Interval(cp[i], cp[i + 1])
                    if interval.is_compound() and cp_dur[i] != Ratio(1, 1):
                        if i + 1 not in illegal_intervals:
                            illegal_intervals.append(i + 1)
                if i % 2 == 0:
                    interval = Interval(cf[i], cf[i + 2])
                    if interval.is_compound():
                        illegal_intervals.append(i + 2)
        for i in illegal_intervals:
            self.analysis.results.append(f'At #{i + 1}: forbidden compound melodic interval')



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
    def __init__(self, score, species):
        ## Call the superclass and give it the score.
        super().__init__(score)
        if species not in [1, 2]:
            raise ValueError(f"'{species}' is not a valid species number 1 or 2.")
        ## The integer species number for the analysis.
        self.species = species
        ## A local copy of the analysis settings.
        self.settings = copy(s1_settings) if species == 1 else copy(s2_settings)
        ## Add your rules to this list.
        self.rules = [ForbiddenStartingPitch(self),
                      ForbiddenRest(self),
                      ForbiddenDuration(self),
                      ConsecutiveUnisons(self),
                      ConsecutiveFifths(self),
                      ConsecutiveOctaves(self),
                      DirectUnisons(self),
                      DirectFifths(self),
                      DirectOctaves(self),
                      CfConsecUnisons(self),
                      CfConsecFifths(self),
                      CfConsecOctaves(self),
                      VoiceOverlap(self),
                      VoiceCrossing(self),
                      WeakBeatDissonance(self),
                      StrongBeatDissonance(self),
                      ConsecParallels(self),
                      MelodicCadence(self),
                      NonDiatonicPitch(self),
                      DissonantMelodicInterval(self),
                      MaxLrg(self),
                      MaxUni(self),
                      Max4th(self),
                      Max5th(self),
                      Max6th(self),
                      Max7th(self),
                      Max8va(self),
                      MaxConsecLeap(self),
                      MaxSameDir(self),
                      StepRecovery(self),
                      CompoundInterval(self)]
        ## A list of strings that represent the findings of your analysis.
        self.results = []

    ## Use this function to perform whatever setup actions your rules require.
    def setup(self, args, kwargs):
        self.tps = timepoints(self.score, span=True, measures=False)
        self.key = self.score.parts[0].staffs[0].bars[0].key
        self.tonic = self.key.tonic()
        self.lower_voice = []
        self.upper_voice = []
        self.lower_dur = []
        self.upper_dur = []
        self.intervals = []
        self.partids = [key[: 2] for key in list(self.tps[0].nmap.keys())]

        for tp in self.tps:
            nmap = tp.nmap
            keys = list(nmap.keys())
            lower_note = nmap.get(keys[1])
            upper_note = nmap.get(keys[0])
            self.lower_dur.append(lower_note.dur)
            self.upper_dur.append(upper_note.dur)

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

        if self.score.get_part(self.partids[0]).name == 'CF':
            self.cflow = False
            self.cf_voice = self.upper_voice
            self.cf_dur = self.upper_dur
            self.cp_voice = self.lower_voice
            self.cp_dur = self.lower_dur
        else:
            self.cflow = True
            self.cf_voice = self.lower_voice
            self.cf_dur = self.lower_dur
            self.cp_voice = self.upper_voice
            self.cp_dur = self.upper_dur

    ## This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed.
    def submit_to_grading(self):
        self.analyze()
        ## When you return your results to the autograder make sure you convert
        # it to a Python set, like this:
        self.results.sort()
        print('{')
        for result in self.results[:-1]:
            print(f"'{result}',")
        print(f"'{self.results[-1]}'")
        print('}')
        return set(self.results)
    
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

