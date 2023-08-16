from dataclasses import dataclass, field
from typing import List

@dataclass
class Record:
    """ Represents a book from the MLN """

    # The index is found in the first line of a record, make it the only required value
    index: int

    # The remaining fields will be filled in as the rest of the record is read, specify defaults
    titles: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    authors: List[str] = field(default_factory=list)
    edition: str = ""
    pub_info: str = ""
    descriptions: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    subjects: List[str] = field(default_factory=list)
    bib_util: str = ""
    standard: List[str] = field(default_factory=list)
    copies: List[str] = field(default_factory=list)
