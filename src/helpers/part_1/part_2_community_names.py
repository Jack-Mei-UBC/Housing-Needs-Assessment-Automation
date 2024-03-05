from typing import List

from helpers.introduction.table2 import get_table2
import report_input


def community_names(geo_codes: List[int]) -> List[str]:
    df = get_table2(geo_codes)
    names = list(df["Geography"])
    pattern = r"(.*)(\s\(CS?D, .*\))"
    for index, name in enumerate(names):
        if index < len(report_input.geo_name_list) and report_input.geo_name_list[index] is not None:
            names[index] = report_input.geo_name_list[index]
            continue
        # match = re.search(pattern, name)
        # if match:
        #     names[index] = match.group(1)
    return names


def community_names_string(geo_codes: List[int]) -> str:
    name_list = community_names(geo_codes)
    return ", ".join(name_list)


def single_community_name(geo_code: int) -> str:
    if geo_code == report_input.community_cd and report_input.community_cd_name is not None:
        return report_input.community_cd_name
    elif geo_code in report_input.community_csds:
        i = report_input.community_csds.index(geo_code)
        if len(report_input.geo_name_list) > i and report_input.geo_name_list[i] is not None:
            return report_input.geo_name_list[i]
    df = get_table2([geo_code])
    names = list(df["Geography"])
    # pattern = r"(.*)(\s\(CS?D, .*\))"
    # match = re.search(pattern, names[0])
    # if match:
    #     return match.group(1)
    # return "Community Name Not Found"
    return names[0]
