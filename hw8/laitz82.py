###############################################################################

## You can import from score, theory and any python module you want to use.

from .score import Pitch, Interval, Mode, import_score
from .theory import Analysis, Rule, timepoints
from copy import copy


## A template dictionary whose keys represent analytical checks performed on
# a melody. Your analysis will copy this dictionary into its self.results
# attribute and then run its rules to update the value of each check in the
# dictionary. When a rule is run and it determines a check is successful, the
# rule will set the dictionary value (e.g. self.analysis['MEl_START_NOTE'])
# to True and if its not successful it will set it to a list of zero or more
# values as described below.
melodic_checks = {
    
    # Pitch checks

    ## Starting note must be tonic, mediant, or dominant. If the melody
    # starts correctly set this value to True, otherwise set it to an empty
    # list [].
    'MEL_START_NOTE': None,

    ## Last two notes must be melodic cadence (2-1 or 7-1). If the
    # melody ends correctly set this value to True, otherwise set
    # it to an empty list [].
    'MEL_CADENCE': None,

    ## At least 75% of notes must be within the tessitura (central Major
    # 6th of the melody's range). If the check is successful set this value
    # to true, otherwise set it to an empty list [].
    'MEL_TESSITURA': None,

    ## All pitches must be diatonic. If the check is successful set
    # this value to True, otherwise set it to a list containing the
    # note positions of each note that fails. Note positions start
    # on 1 not 0.
    'MEL_DIATONIC': None,

    # Melodic interval checks

    ## At least 51% of notes must be stepwise.  If the check is successful
    # set this value to True, otherwise set it to an empty list [].
    'INT_STEPWISE': None,

    ## All intervals must be consonant (P4 is consonant). If the check
    # is successful set this value to True, otherwise set it to a list
    # containing the note positions of each note that fails. Note
    # positions start on 1 not 0. Since this check involves an interval
    # between two notes, use the position of the note to the left
    # of the offending interval.
    'INT_CONSONANT': None,

    ## All intervals must be an octave or less. If the check is successful
    # set this value to True, otherwise set it to a list containing the
    # note positions of each note that fails. Note positions start on 1
    # not 0. Since this check involves an interval between two notes, use
    # the position of the note to the left of the offending interval.
    'INT_SIMPLE': None,

    ## Max number of large leaps is 1. A large leap is defined as a perfect
    # fifth or more. If the check is successful set this value to True,
    # otherwise set it to a list containing the note positions of each
    # interval after the first one.
    'INT_NUM_LARGE': None,

    ## Max number of unisons is 1. If the check is successful set this
    # value to True, otherwise set it to a list containing the note
    # positions of each unison after the first one.
    'INT_NUM_UNISON': None,

    ## Max number of consecutive intervals moving in same direction is 3
    # (i.e four consecutive notes). If the check is successful set this
    # value to True, otherwise set it to a list containing the note
    # positions of each interval after the third one.
    'INT_NUM_SAMEDIR': None,

    # Leap checks

    ## Leap of 4th must reverse direction, leap of 5th or more must reverse
    # by step. The leap can be the result of a single interval or by multiple
    # consecutive leaps in the same direction. For multiple leaps in the same
    # direction, the total size of the leap should be the sum of all the leaps
    # in the same direction. If the check is successful set this value to True,
    # otherwise set it to a list containing the note positions of each interval
    # that fails. To mark a leap spanning a 5th or greater that did not reverse
    # by step, set its note index to be negative.
    'LEAP_RECOVERY': None,

    ## Max number of consecutive leaps in a row is 2 (three notes). If the
    # check is successful set this value to True, otherwise set it to a list
    # containing the note positions of each interval after the second leap.
    'LEAP_NUM_CONSEC': None,

    # Shape checks

    ## Max number of climax notes is 1.  If the check is successful set
    # this value to True, otherwise set it to a list containing the note
    # positions of each climax after the first.
    'SHAPE_NUM_CLIMAX': None,

    ## Climax note must be located within the center third of melody.  If
    # the check is successful set this value to True, otherwise set it to a
    # list containing the note positions of all climaxes outside it.
    'SHAPE_ARCHLIKE': None,

    ## A set of intervals with at least one direct repetition cannot
    # occupy more than 50% of melody. If the check is successful set this
    # value to True, otherwise set it to a list containing the set of
    # interval motions (e.g [2, 2, -3].
    'SHAPE_UNIQUE': None
}

def to_direction(interval):
    if interval.is_unison():
        return 0
    else:
        return interval.sign

# Here is an example of a rule. You can define as many rules as you want.
# The purpose of running a rule is to perform some analytical check(s) and
# then update the self.analysis.results dictionary with its findings.
class MyFirstRule(Rule):

    ## Rule initializer.
    def __init__(self, analysis):
        ## Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "My very first rule.")
        # Now initialize whatever attributes your rule defines.
        # ...

    ## This is where your rule does all its work. When the work is done you
    # should update the analysis results with whatever checks it is doing.
    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

#    ## Uncomment this code if you want your rule to print information to the
#    # the terminal just after it runs...
#    def display(self, index):
#        print('-------------------------------------------------------------------')
#        print(f"Rule {index+1}: {self.title}")
#        print("I'm here!")


# ...ADD MORE RULES HERE!....
class MelStartNote(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Starting note should be scale degree 1, 3, or 5.")

    def apply(self):
        pnum = self.analysis.melody[0].pnum()
        scale = self.analysis.key.scale()
        if pnum in scale:
            if scale.index(pnum) in [0, 2, 4]:
                self.analysis.results['MEL_START_NOTE'] = True
            else:
                self.analysis.results['MEL_START_NOTE'] = []
        else:
            self.analysis.results['MEL_START_NOTE'] = []

class MelCadence(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Last two notes must be melodic cadence (2-1 or 7-1).")

    def apply(self):
        second_last_pnum = self.analysis.melody[-2].pnum()
        last_pnum = self.analysis.melody[-1].pnum()
        scale = self.analysis.key.scale()
        if second_last_pnum in scale and last_pnum in scale:
            if scale.index(second_last_pnum) in [1, 6] and scale.index(last_pnum) == 0:
                self.analysis.results['MEL_CADENCE'] = True
            else:
                self.analysis.results['MEL_CADENCE'] = []
        else:
            self.analysis.results['MEL_CADENCE'] = []

class MelTessitura(Rule):
    def __init__(self, analysis, percentage):
        super().__init__(analysis, "At least 75% of notes must be within the tessitura (central Major 6th of the "
                                   "melody's range).")
        self.percentage = percentage

    def apply(self):
        low_note = min(self.analysis.melody)
        high_note = max(self.analysis.melody)
        medium = low_note.keynum() + high_note.keynum()
        range_min = int(medium / 2) - 4
        range_max = int(medium / 2) + 5

        in_range_count = 0
        for pitch in self.analysis.melody:
            if pitch.keynum() >= range_min and pitch.keynum() <= range_max:
                in_range_count += 1

        if in_range_count >= len(self.analysis.melody) * self.percentage:
            self.analysis.results['MEL_TESSITURA'] = True
        else:
            self.analysis.results['MEL_TESSITURA'] = []

class MelDiatonic(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "All pitches must be diatonic.")

    def apply(self):
        illegal_notes = []
        scale = self.analysis.key.scale()
        if self.analysis.key.mode == Mode.MINOR:
            scale.append(Pitch.pnums(scale[-1].value + 1))
            scale.append(Pitch.pnums(scale[-3].value + 1))

        for i, pitch in enumerate(self.analysis.melody):
            if pitch.pnum() not in scale:
                illegal_notes.append(i)

        if illegal_notes == []:
            self.analysis.results['MEL_DIATONIC'] = True
        else:
            self.analysis.results['MEL_DIATONIC'] = illegal_notes

class IntStepwise(Rule):
    def __init__(self, analysis, percentage):
        super().__init__(analysis, "At least 51% of notes must be stepwise.")
        self.percentage = percentage

    def apply(self):
        step_count = 0
        for interval in self.analysis.intervals:
            if interval.is_second():
                step_count += 1

        if step_count >= len(self.analysis.intervals) * self.percentage:
            self.analysis.results['INT_STEPWISE'] = True
        else:
            self.analysis.results['INT_STEPWISE'] = []

class IntConsonant(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "All intervals must be consonant (P4 is consonant).")

    def apply(self):
        illegal_intervals = []
        for i, interval in enumerate(self.analysis.intervals):
            if not interval.is_seventh() and (interval.is_perfect() or interval.is_major() or interval.is_minor()):
                pass
            else:
                illegal_intervals.append(i + 1)

        if illegal_intervals == []:
            self.analysis.results['INT_CONSONANT'] = True
        else:
            self.analysis.results['INT_CONSONANT'] = illegal_intervals

class IntSimple(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "All intervals must be an octave or less.")

    def apply(self):
        illegal_intervals = []
        for i, interval in enumerate(self.analysis.intervals):
            if not interval.is_simple():
                illegal_intervals.append(i + 1)

        if illegal_intervals == []:
            self.analysis.results['INT_SIMPLE'] = True
        else:
            self.analysis.results['INT_SIMPLE'] = illegal_intervals

class IntNumLarge(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "All intervals must be an octave or less.")

    def apply(self):
        illegal_intervals = []
        for i, interval in enumerate(self.analysis.intervals):
            if interval >= Interval('P5'):
                illegal_intervals.append(i + 1)

        if len(illegal_intervals) <= 1:
            self.analysis.results['INT_NUM_LARGE'] = True
        else:
            self.analysis.results['INT_NUM_LARGE'] = illegal_intervals[1 : ]

class IntNumUnison(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Max number of unisons is 1.")

    def apply(self):
        illegal_intervals = []
        for i, interval in enumerate(self.analysis.intervals):
            if interval.is_unison():
                illegal_intervals.append(i + 1)

        if len(illegal_intervals) <= 1:
            self.analysis.results['INT_NUM_UNISON'] = True
        else:
            self.analysis.results['INT_NUM_UNISON'] = illegal_intervals[1 : ]

class IntNumSameDir(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Max number of consecutive intervals moving in same direction is 3 (i.e four "
                                   "consecutive notes).")

    def apply(self):
        consecutive_count = 1
        last_direction = to_direction(self.analysis.intervals[0])
        illegal_intervals = []
        for i, interval in enumerate(self.analysis.intervals[1 : ]):
            if to_direction(interval) == last_direction:
                consecutive_count += 1
            else:
                consecutive_count = 1
            last_direction = to_direction(interval)

            if consecutive_count > 3:
                illegal_intervals.append(i + 3)

        if not illegal_intervals:
            self.analysis.results['INT_NUM_SAMEDIR'] = True
        else:
            self.analysis.results['INT_NUM_SAMEDIR'] = illegal_intervals

class LeapRecovery(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Leap of 4th must reverse direction, leap of 5th or more must reverse by step.")

    def apply(self):
        total_leap = Interval('P1')
        current_direction = to_direction(total_leap)
        illegal_intervals = []

        for i, interval in enumerate(self.analysis.intervals):
            if total_leap.is_fourth():
                if to_direction(interval) != -1 * current_direction:
                    illegal_intervals.append(i + 1)
            elif total_leap.span >= 4:
                if not interval.is_second():
                    illegal_intervals.append(-i - 1)
                elif to_direction(interval) != -1 * current_direction:
                    illegal_intervals.append(-i - 1)

            if interval.is_unison() or interval.is_second():
                total_leap = Interval('P1')
            elif to_direction(interval) == -1 * current_direction:
                new_interval = Interval(interval.string())
                new_interval.sign = 1
                total_leap = new_interval
            else:
                new_interval = Interval(interval.string())
                new_interval.sign = 1
                total_leap = total_leap.add(new_interval)

            current_direction = to_direction(interval)

        if total_leap.is_fourth():
            illegal_intervals.append(len(self.analysis.intervals) + 1)
        elif total_leap.span >= 4:
            illegal_intervals.append(-len(self.analysis.intervals) - 1)

        if not illegal_intervals:
            self.analysis.results['LEAP_RECOVERY'] = True
        else:
            self.analysis.results['LEAP_RECOVERY'] = illegal_intervals

class LeapNumConsec(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Max number of consecutive leaps in a row is 2 (three notes).")

    def apply(self):
        consec_count = 0
        illegal_intervals = []

        for i, interval in enumerate(self.analysis.intervals):
            if interval.span >= 2:
                consec_count += 1
            else:
                consec_count = 0

            if consec_count > 2:
                illegal_intervals.append(i + 1)

        if not illegal_intervals:
            self.analysis.results['LEAP_NUM_CONSEC'] = True
        else:
            self.analysis.results['LEAP_NUM_CONSEC'] = illegal_intervals

class ShapeNumClimax(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Max number of consecutive leaps in a row is 2 (three notes).")

    def apply(self):
        to_return = [i + 1 for i, pitch in enumerate(self.analysis.melody) if pitch == max(self.analysis.melody)]
        self.analysis.results['SHAPE_NUM_CLIMAX'] = True if len(to_return) <= 1 else to_return[1 : ]

class ShapeArchlike(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Max number of consecutive leaps in a row is 2 (three notes).")

    def apply(self):
        to_return = [i + 1 for i, pitch in enumerate(self.analysis.melody) if pitch == max(self.analysis.melody) and (i < int(len(self.analysis.melody) / 3) or i >= len(self.analysis.melody) - int(len(self.analysis.melody) / 3))]
        self.analysis.results['SHAPE_ARCHLIKE'] = True if not to_return else to_return

## A class representing a melodic analysis of a voice in a score. The class
# has three attributes to being with, you will likely add more attributes.
# * self.score: The score passed into the analysis
# * self.rules: A list of rules that you define to implement the analysis
# * self.results: A dictionary containing the set of analytical checks your
# analysis performs. Your rules will update specific checks in this dictionary.
class MelodicAnalysis(Analysis):
    def __init__(self, score):
        ## Call the superclass and give it the score. Don't change this line.
        super().__init__(score)
        ## Copy the empty result checks template to this analysis. Don't
        # change this line
        self.results = copy(melodic_checks)
        ## Create the list of rules this analysis runs. This example just
        # uses the demo Rule defined above.
        self.rules = [MyFirstRule(self),
                      MelStartNote(self),
                      MelCadence(self),
                      MelTessitura(self, 0.75),
                      MelDiatonic(self),
                      IntStepwise(self, 0.51),
                      IntConsonant(self),
                      IntSimple(self),
                      IntNumLarge(self),
                      IntNumUnison(self),
                      IntNumSameDir(self),
                      LeapRecovery(self),
                      LeapNumConsec(self),
                      ShapeNumClimax(self),
                      ShapeArchlike(self)]

    ## You can define a cleanup function if you want.
    def cleanup(self):
        self.melody, self.intervals, self.motions = [], [], []

    ## You MUST define a setup function! A first few steps are
    # done for you, you can add more steps as you wish.
    def setup(self, args, kwargs):
        assert len(args) == 1, "Call: analyze('pvid')"
        # melodic_id is the voice to analyze passed in by the caller.
        # you will want to use this when you access the timepoints
        self.melodic_id = args[0]
        self.tps = timepoints(self.score, span=True, measures=False)
        self.melody = [tp.nmap.get(self.melodic_id, None).pitch for tp in self.tps]
        self.intervals = [Interval(self.melody[i], self.melody[i + 1]) for i in range(len(self.melody) - 1)]
        self.key = self.score.parts[0].staffs[0].bars[0].key

    ## This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results