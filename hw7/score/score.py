###############################################################################

from .ratio import Ratio
from .part import Part


## A class representing a complete musical score. A score has two attributes:
#  self.metadata and self.parts.
#
#  Example: To load a score from a MusicXml file and iterate all its
#  objects you can do something like this:
#  @code
#  import hw7.score as score
#  bach = score.import_score("bach-chorale-001.xml")
#  for part in bach:
#      for staff in part:
#          for bar in staff:
#              for voice in bar:
#                  for note in voice:
#                      pass
#  @endcode
class Score:

    ## Initializes a Score and its two attributes self.metadata and
    # self.parts.
    # @param metadata A dictionary containing non-performance score
    # properties for the score's metadata attribute. Defaults to an
    # empty dictionary. If the score is loaded from a MusicXml file
    # the metadata will include the following keys: 'main_key',
    # 'main_meter', 'melodic_voices', 'static_voices', 'voice_ids',
    # 'work_number', 'work_title', 'composer', 'copyright'.
    # @param parts A list of score parts to initialize score the
    # score's parts attribute. Defaults to an empty list.
    #
    # The method should raise a TypeError If metadata is not a dictionary.
    # If parts are specified they should be added to the score by calling
    # add_part(). See also: Part.
    def __init__(self, metadata={}, parts=[]):
        self.metadata = metadata
        self.parts = parts

    ## Returns a string showing the score's title and the unique
    # id of the instance printed in hex. To find the score title
    # the method should check for a 'work_title' in the the score's
    # metadata and if that does not exist it should check for a
    # 'movement_title'. If neither metadata exists then method
    # should return the string '(untitled)' as the title.
    # Examples:
    # '<Score: "Aus meines Herzens Grunde" 0x103fa5780>'
    # '<Score: "(untitled)" 0x1334b57f0>'
    def __str__(self):
        return f'<Score: "{self.metadata.get("work_title", self.metadata.get("movement_title", "(untitled)"))}" {id(self)}>'

    ## Define __repr__ to be the same as __str__ except there is
    # no hex id included.
    # Example: '<Score: "(untitled)">'
    def __repr__(self):
        return f'<Score: "{self.metadata.get("work_title", self.metadata.get("movement_title", "(untitled)"))}">'

    ## Implements Score iteration by returning an iterator for the score's
    # parts. See: Python's iter() function.
    def __iter__(self):
        return self.parts

    ## Returns a value from the score's metadata for the given key
    # (string), or the default value if the key does not exist.
    # @param key The dictionary key (string) for the data.
    # @param default A default value to return if key is not in the
    # metadata, defaults to None.
    def get_metadata(self, key, default=None):
        return self.metadata.get(key, default)

    ## Assigns a value to the given key in the score's metadata.
    # @param key The dictionary key (string) for the value.
    # @param value The new value to assign in the metadata.
    # @returns The new value in the metadata.
    def set_metadata(self, key, value):
        self.metadata[key] = value
        return value

    ## Appends a Part to the score's part list and assigns
    # itself to the part's score attribute.
    # @param part The part to append to the Score's part list.
    # The method should raise a TypeError if part is not a Part instance.
    def add_part(self, part):
        if isinstance(part, Part):
            self.parts.append(part)
        else:
            raise TypeError("part is not a Part instance")

    ## Returns a list of the scores's part identifiers in the same order
    # that they occur in the parts list.
    def part_ids(self):
        return [part.id for part in self.parts]

    ## Returns the number of parts in the score.
    def num_parts(self):
        return len(self.parts)

    ## Returns the score part with the specified id or None if it cannot be found.
    # @param pid  The id of the part to return.
    # @return The part if it is found else None.
    def get_part(self, pid):
        for part in self.parts:
            if part.id == pid:
                return part

        return None

    ## Returns a list of indented repr() strings. Every string in the list represents
    # one Score/Part/Staff/Bar/Voice/Note/Rest/Chord instance's repr() string
    # with a proper number of indents added at the beginning of that string.
    # When later printed to the terminal (via self.print method, see below),
    # every string in the list is on its own line and
    # indented an additional two spaces for each level.
    # Example:
    # <Score: "Untitled">
    #   <Part: P1>
    #     <Staff: 1>
    #       <Bar: 1 Treble G-Major 4/4 STANDARD>
    #         <Voice: 1>
    #           <Note: F#4 1/4>
    #           <Note: B4 1/4>
    #           <Note: A4 1/4>
    #           <Note: G4 1/4>
    #       <Bar: 2 FINAL_DOUBLE>
    #         <Voice: 1>
    #           <Note: F#4 1/4>
    #           <Note: E4 1/4>
    #           <Note: G4 1/4>
    def print_all_repr(self):
        s = []
        indent = '  '
        s.append(self.__repr__())
        for part in self.parts:
            s.append(indent + part.__repr__())
            for staff in part.staffs:
                s.append(indent * 2 + staff.__repr__())
                for bar in staff.bars:
                    s.append(indent * 3 + bar.__repr__())
                    for voice in bar.voices:
                        s.append(indent * 4 + voice.__repr__())
                        for note in voice.notes:
                            s.append(indent * 5 + note.__repr__())
        return s

    ## Prints the score to the terminal. This function has already been written for you.
    # Do not alter the function, just implement the print_all_reprs() function above.
    def print(self):
        print('\n'.join(self.print_all_repr()))
