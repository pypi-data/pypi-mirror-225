import re
from typing import List, Optional

from .record import Record

DEFAULT_IGNORES = ["ORDERED", "PROCESSED"]


def _loc_str_to_list(loc_str: str) -> List[str]:
    return [loc.strip() for loc in loc_str.split("&")]


def _loc_list_to_str(loc_lst: List[str]) -> str:
    return " & ".join(loc_lst)


def _find_section_start(section: str, line: str) -> Optional[str]:
    sec_match = re.match(f"{section}\\s+(.*)", line)
    if sec_match:
        return sec_match.group(1)


def lines_to_records(
    lines: List[str], keywords_to_ignore: Optional[List[str]] = None
) -> List[Record]:
    """
    Turns a list of lines from a MLN record export into a list of Record objects

    :param lines:
    :type lines: List[str]
    :rtype: Dict[str, Any]
    """
    results: List[Record] = []
    last_field_found = None
    ignore_list = DEFAULT_IGNORES + (keywords_to_ignore or [])

    for line in lines:
        # Start by checking for fields to continue
        last_field_match = re.match(r"\s{12}(.*)", line)
        if last_field_match:
            data = last_field_match.group(1)
            match last_field_found:
                case "locations":
                    results[-1].locations[:] = _loc_str_to_list(
                        _loc_list_to_str(results[-1].locations) + data
                    )
                    continue
                case "title":
                    results[-1].titles[-1] += data
                    continue
                case "pub_info":
                    results[-1].pub_info += data
                    continue
                case "edition":
                    results[-1].edition += data
                case "descript":
                    results[-1].descriptions[-1] += data
                    continue
                case "note":
                    results[-1].notes[-1] += data
                case "subject":
                    results[-1].subjects[-1] += data

        # Check if the line should be skipped
        if any(ignorable in line for ignorable in ignore_list):
            continue

        # Check for start of new record
        last_field_found = None
        index_match = re.match(r"Record (\d+) of \d+", line)
        if index_match:
            last_field_found = "record"
            index = int(index_match.group(1))
            results.append(Record(index=index))
            continue

        # Check for start of LOCATIONS section
        loc_match = _find_section_start("LOCATIONS", line)
        if loc_match:
            last_field_found = "locations"
            results[-1].locations[:] = _loc_str_to_list(loc_match)
            continue

        # Check for start of AUTHOR section
        author_match = _find_section_start("AUTHOR", line)
        if author_match:
            last_field_found = "author"
            results[-1].authors.append(author_match)
            continue

        # Check for start of ADD AUTHOR section
        add_author_match = _find_section_start("ADD AUTHOR", line)
        if add_author_match:
            last_field_found = "author"
            results[-1].authors.append(add_author_match)
            continue

        # Check for start of TITLE section
        title_match = _find_section_start("TITLE", line)
        if title_match:
            last_field_found = "title"
            results[-1].titles.append(title_match)
            continue

        # Check for start of ADD TITLE section
        add_title_match = _find_section_start("ADD TITLE", line)
        if add_title_match:
            last_field_found = "title"
            results[-1].titles.append(add_title_match)
            continue

        # Check for EDITION
        edition_match = _find_section_start("EDITION", line)
        if edition_match:
            last_field_found = "edition"
            results[-1].edition = edition_match
            continue

        # Check for start of PUB INFO section
        pub_info_match = _find_section_start("PUB INFO", line)
        if pub_info_match:
            last_field_found = "pub_info"
            results[-1].pub_info = pub_info_match
            continue

        # Check for start of DESCRIPT section
        descript_match = _find_section_start("DESCRIPT", line)
        if descript_match:
            last_field_found = "descript"
            results[-1].descriptions.append(descript_match)

        # Check for start of NOTE section
        note_match = _find_section_start("NOTE", line)
        if note_match:
            last_field_found = "note"
            results[-1].notes.append(note_match)

        # Check for start of SUBJECT section
        subject_match = _find_section_start("SUBJECT", line)
        if subject_match:
            last_field_found = "subject"
            results[-1].subjects.append(subject_match)

        # Check for start of BIB UTIL # section
        bib_util_match = _find_section_start("BIB UTIL #", line)
        if bib_util_match:
            last_field_found = "bib_util"
            results[-1].bib_util = bib_util_match

        # Check for start of STANDARD # section
        standard_match = _find_section_start("STANDARD #", line)
        if standard_match:
            last_field_found = "standard"
            results[-1].standard.append(standard_match)

        # Check for copy entry
        copy_match = re.match(r'^\d{1,3} > (.*)$', line)
        if copy_match:
            last_field_found = "copy"
            # Location field is at most 28 characters wide
            results[-1].copies.append(copy_match.group(1)[:28].strip())

    return results
