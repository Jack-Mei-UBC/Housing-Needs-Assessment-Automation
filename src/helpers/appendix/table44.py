import report_input
from helpers.part_1.figure5 import figure5_helper


def get_table44(geo_code):
    df = figure5_helper(geo_code, True)
    # Move "total by structural type" to the end
    total = "total by structural type"
    total_vals = df[total]
    df = df.drop(columns=[total])
    df[total] = total_vals
    df = df.astype(int).astype(str)
    df = df.T
    df = df.rename(
        index={
            total: "Total by Structural Type",
        },
        columns={
            "total by construction period": "Total by Construction Period",
        }
    )
    return df


# get_table44(report_input.community_cd)
