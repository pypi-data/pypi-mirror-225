import pandas as pd


def bg_red_yellow(df):
    """Color report of Class Performance Drift based on Alert.

    Args:
        df (pd.DataFrame): report in input

    Returns:
        pd.DataFrame: color-mapping report
    """
    ret = pd.DataFrame("", index=df.index, columns=df.columns)
    if "Absolute_warning" in df.columns:
        ret.loc[df.Absolute_warning == "Red Alert", ["Curr_perf", "Absolute_warning"]] = "background-color: red"
        ret.loc[df.Absolute_warning == "Yellow Alert", ["Curr_perf", "Absolute_warning"]] = "background-color: yellow"

    ret.loc[df.Relative_warning == "Red Alert", ["Drift(%)", "Relative_warning"]] = "background-color: red"
    ret.loc[df.Relative_warning == "Yellow Alert", ["Drift(%)", "Relative_warning"]] = "background-color: yellow"
    return ret
