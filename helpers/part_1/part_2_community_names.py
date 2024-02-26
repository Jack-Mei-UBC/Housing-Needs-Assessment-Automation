from typing import List
import re

from helpers.introduction.table2 import get_table2
import report_input

def community_names(geo_codes: List[int]) -> List[str]:
    df = get_table2(geo_codes)
    names = list(df["Geography"])
    pattern = r"(.*)(\s\(CS?D, .*\))"
    for index, name in enumerate(names):
        if report_input.part_2_names[index] is not None:
            names[index] = report_input.part_2_names[index]
            continue
        match = re.search(pattern, name)
        if match:
            names[index] = match.group(1)
    return names
