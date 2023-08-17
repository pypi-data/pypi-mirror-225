import numpy as np
from functools import reduce
import warnings
from typing import Dict

from model_monitoring.utils import check_metrics_sets
from model_monitoring.config import read_config

from model_monitoring.fairness_drift.fairness_drift import (
    fair_from_dict,
    add_absolute_alert_columns,
    add_relative_alert_columns,
    check_fairness_groups,
)

standard_threshold = read_config(config_dir="config", name_params="fairness_drift_threshold.yml")


class FairnessDrift:
    """Fairness Drift Class."""

    def __init__(self, fair_metrics_curr, config_threshold=None):
        """Fairness Drift Class.

        Args:
            fair_metrics_curr (dict): dictionary containing current fairness metrics perfomances
            config_threshold (dict, optional): dictionary containing threshold settings. Defaults to None.
        """
        if not isinstance(fair_metrics_curr, Dict):
            raise ValueError(
                "Fairness metrics in input has not a valid format. It should be a dictionary containing functions as keys and values as values."
            )
        if config_threshold is None:
            config_threshold = standard_threshold

        check_metrics = [i for i in fair_metrics_curr.keys() if i not in config_threshold.keys()]
        if len(check_metrics) > 0:
            warnings.warn(f"{check_metrics} do not have threshold settings in config_threshold")

        list_com_metrics = list(set(fair_metrics_curr.keys()).intersection(set(config_threshold.keys())))

        # initialize report
        report_df = fair_from_dict(
            {x: fair_metrics_curr[x] for x in list_com_metrics}, label=["Curr_perf", "Curr_Perc_label"]
        )

        # for output report columns ordering according to current percentage label
        ordered_columns = (
            report_df.loc[:, (slice(None), slice(None), "Curr_Perc_label")]
            .max()
            .reset_index()
            .sort_values(["level_0", 0], ascending=[True, False])
            .values
        )
        self.report = report_df.reindex([""] + [x[1] for x in ordered_columns], axis=1, level=1)

        self.fair_metrics_curr = fair_metrics_curr
        self.config_threshold = config_threshold
        self.perf_metrics_stor = None
        self.absolute = False
        self.relative = False

    def get_absolute(self):
        """Load on the report the absolute alert on current fairness metrics perfomances."""
        # Regenerate Multiindex report with Absolute_warning columns
        self.report = add_absolute_alert_columns(self.report, absolute=self.absolute)

        # Generation Alert
        if not self.absolute:
            for a in self.report.Metric.values:
                absolute_red = self.config_threshold[a]["absolute"]["red"]
                absolute_yellow = self.config_threshold[a]["absolute"]["yellow"]

                if self.config_threshold[a]["logic"] == "decrease":
                    if absolute_red != "None":
                        for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                            for y in np.unique(self.report[x].columns.get_level_values(0)):
                                curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                                if curr_perf < absolute_red:
                                    self.report.loc[self.report.Metric == a, (x, y, "Absolute_warning")] = "Red Alert"
                                else:
                                    if absolute_yellow != "None":
                                        if (curr_perf > absolute_red) and (curr_perf < absolute_yellow):
                                            self.report.loc[
                                                self.report.Metric == a, (x, y, "Absolute_warning")
                                            ] = "Yellow Alert"
                    else:
                        if absolute_yellow != "None":
                            for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                                for y in np.unique(self.report[x].columns.get_level_values(0)):
                                    curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                                    if curr_perf < absolute_yellow:
                                        self.report.loc[
                                            self.report.Metric == a, (x, y, "Absolute_warning")
                                        ] = "Yellow Alert"

                elif self.config_threshold[a]["logic"] == "increase":
                    if absolute_red != "None":
                        for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                            for y in np.unique(self.report[x].columns.get_level_values(0)):
                                curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                                if curr_perf > absolute_red:
                                    self.report.loc[self.report.Metric == a, (x, y, "Absolute_warning")] = "Red Alert"
                                else:
                                    if absolute_yellow != "None":
                                        if (curr_perf < absolute_red) and (curr_perf > absolute_yellow):
                                            self.report.loc[
                                                self.report.Metric == a, (x, y, "Absolute_warning")
                                            ] = "Yellow Alert"
                    else:
                        if absolute_yellow != "None":
                            for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                                for y in np.unique(self.report[x].columns.get_level_values(0)):
                                    curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                                    if curr_perf > absolute_yellow:
                                        self.report.loc[
                                            self.report.Metric == a, (x, y, "Absolute_warning")
                                        ] = "Yellow Alert"

                elif self.config_threshold[a]["logic"] == "axial":
                    if absolute_red != "None":
                        for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                            for y in np.unique(self.report[x].columns.get_level_values(0)):
                                curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                                if (curr_perf > max(absolute_red)) or (curr_perf < min(absolute_red)):
                                    self.report.loc[self.report.Metric == a, (x, y, "Absolute_warning")] = "Red Alert"
                                else:
                                    if absolute_yellow != "None":
                                        if ((curr_perf < max(absolute_red)) and (curr_perf > min(absolute_red))) and (
                                            (curr_perf > max(absolute_yellow)) or (curr_perf < min(absolute_yellow))
                                        ):
                                            self.report.loc[
                                                self.report.Metric == a, (x, y, "Absolute_warning")
                                            ] = "Yellow Alert"
                    else:
                        if absolute_yellow != "None":
                            for x in [x for x in self.report.columns.levels[0] if x != "Metric"]:
                                for y in self.report[x].columns.get_level_values(0):
                                    curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                                    if (curr_perf > max(absolute_yellow)) or (curr_perf < min(absolute_yellow)):
                                        self.report.loc[
                                            self.report.Metric == a, (x, y, "Absolute_warning")
                                        ] = "Yellow Alert"

                else:
                    raise ValueError(
                        f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease','axial']."
                    )

        self.absolute = True

        # for output report columns ordering according to current percentage label
        ordered_columns = (
            self.report.loc[:, (slice(None), slice(None), "Curr_Perc_label")]
            .max()
            .reset_index()
            .sort_values(["level_0", 0], ascending=[True, False])
            .values
        )
        self.report = self.report.reindex([""] + [x[1] for x in ordered_columns], axis=1, level=1)

        # for output report columns ordering
        if self.relative:
            self.report = self.report.reindex(
                [
                    "",
                    "Curr_perf",
                    "Curr_Perc_label",
                    "Absolute_warning",
                    "Stor_perf",
                    "Stor_Perc_label",
                    "Drift(%)",
                    "Relative_warning",
                ],
                axis=1,
                level=2,
            )

    def get_relative(self, fair_metrics_stor):
        """Load on the report the historichal fairness metrics performances, drift compared to the current fairness performances and relative alert on drift.

        Args:
            fair_metrics_stor (dict): dictionary containing historichal fairness metrics perfomances.
        """
        # re-initialize report
        if self.relative:
            list_drop = reduce(
                lambda l, y: l.append(y) or l if y not in l else l,
                [
                    (x[0], x[1], x[2])
                    for x in self.report.columns
                    if x[2] in ["Stor_perf", "Stor_Perc_label", "Drift(%)", "Relative_warning"]
                ],
                [],
            )
            self.report = self.report.drop(columns=list_drop)

        # Check if the metrics are the same
        check_metrics_sets(metrics_1=fair_metrics_stor, metrics_2=self.fair_metrics_curr)

        list_com_metrics = list(set(fair_metrics_stor.keys()).intersection(set(self.fair_metrics_curr.keys())))
        self.fair_metrics_stor = {x: fair_metrics_stor[x] for x in list_com_metrics}
        stor_fair_df = fair_from_dict(self.fair_metrics_stor, label=["Stor_perf", "Stor_Perc_label"])

        # Check if the fairness group are the same
        list_no_join = check_fairness_groups(self.report, stor_fair_df)

        # Update the report with historical fairness performances and limit to common fairness groups
        self.report = (
            self.report.merge(stor_fair_df, how="outer", on="Metric")
            .sort_index(axis=1, level=1, ascending=False)[
                reduce(lambda l, y: l.append(y) or l if y not in l else l, [x[0] for x in self.report.columns], [])
            ]
            .drop(columns=list_no_join)
        )

        # Regenerate Multiindex report with Drift and columns
        self.report = add_relative_alert_columns(self.report)

        # Generation Drift
        for a in self.report.Metric.values:
            if self.config_threshold[a]["logic"] in ["decrease", "increase"]:
                for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                    for y in np.unique(self.report[x].columns.get_level_values(0)):
                        stor_perf = self.report.loc[self.report.Metric == a, x][y]["Stor_perf"].values[0]
                        curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                        if stor_perf > 0:
                            self.report.loc[self.report.Metric == a, (x, y, "Drift(%)")] = (
                                (curr_perf - stor_perf) / stor_perf * 100
                            )
                        else:
                            self.report.loc[self.report.Metric == a, (x, y, "Drift(%)")] = (
                                (stor_perf - curr_perf) / stor_perf * 100
                            )
            elif self.config_threshold[a]["logic"] == "axial":
                axial_point = self.config_threshold[a]["axial_point"]
                for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                    for y in np.unique(self.report[x].columns.get_level_values(0)):
                        stor_perf = self.report.loc[self.report.Metric == a, x][y]["Stor_perf"].values[0]
                        curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                        self.report.loc[self.report.Metric == a, (x, y, "Drift(%)")] = (
                            (abs(curr_perf - axial_point) - abs(stor_perf - axial_point))
                            / abs(stor_perf - axial_point)
                            * 100
                        )
            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease','axial']."
                )

        # Generation Alert
        for a in self.report.Metric.values:
            relative_red = self.config_threshold[a]["relative"]["red"]
            relative_yellow = self.config_threshold[a]["relative"]["yellow"]
            absolute_tol = self.config_threshold[a]["relative"]["absolute_tol"]

            if self.config_threshold[a]["logic"] == "decrease":
                if relative_red != "None":
                    for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                        for y in np.unique(self.report[x].columns.get_level_values(0)):
                            # check absolute tollerance for relative alert
                            stor_perf = self.report.loc[self.report.Metric == a, x][y]["Stor_perf"].values[0]
                            curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                            if abs(curr_perf - stor_perf) >= absolute_tol:
                                drift_perf = self.report.loc[self.report.Metric == a, x][y]["Drift(%)"].values[0]
                                if drift_perf < relative_red * 100:
                                    self.report.loc[self.report.Metric == a, (x, y, "Relative_warning")] = "Red Alert"
                                else:
                                    if relative_yellow != "None":
                                        if (drift_perf > relative_red * 100) and (drift_perf < relative_yellow * 100):
                                            self.report.loc[
                                                self.report.Metric == a, (x, y, "Relative_warning")
                                            ] = "Yellow Alert"
                else:
                    if relative_yellow != "None":
                        for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                            for y in np.unique(self.report[x].columns.get_level_values(0)):
                                # check absolute tollerance for relative alert
                                stor_perf = self.report.loc[self.report.Metric == a, x][y]["Stor_perf"].values[0]
                                curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                                if abs(curr_perf - stor_perf) >= absolute_tol:
                                    drift_perf = self.report.loc[self.report.Metric == a, x][y]["Drift(%)"].values[0]
                                    if drift_perf < relative_yellow * 100:
                                        self.report.loc[
                                            self.report.Metric == a, (x, y, "Relative_warning")
                                        ] = "Yellow Alert"

            elif self.config_threshold[a]["logic"] in ["increase", "axial"]:
                if relative_red != "None":
                    for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                        for y in np.unique(self.report[x].columns.get_level_values(0)):
                            # check absolute tollerance for relative alert
                            stor_perf = self.report.loc[self.report.Metric == a, x][y]["Stor_perf"].values[0]
                            curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                            if abs(curr_perf - stor_perf) >= absolute_tol:
                                drift_perf = self.report.loc[self.report.Metric == a, x][y]["Drift(%)"].values[0]
                                if drift_perf > relative_red * 100:
                                    self.report.loc[self.report.Metric == a, (x, y, "Relative_warning")] = "Red Alert"
                                else:
                                    if relative_yellow != "None":
                                        if (drift_perf < relative_red * 100) and (drift_perf > relative_yellow * 100):
                                            self.report.loc[
                                                self.report.Metric == a, (x, y, "Relative_warning")
                                            ] = "Yellow Alert"
                else:
                    if relative_yellow != "None":
                        for x in np.unique([x for x in self.report.columns.levels[0] if x != "Metric"]):
                            for y in np.unique(self.report[x].columns.get_level_values(0)):
                                # check absolute tollerance for relative alert
                                stor_perf = self.report.loc[self.report.Metric == a, x][y]["Stor_perf"].values[0]
                                curr_perf = self.report.loc[self.report.Metric == a, x][y]["Curr_perf"].values[0]
                                if abs(curr_perf - stor_perf) >= absolute_tol:
                                    drift_perf = self.report.loc[self.report.Metric == a, x][y]["Drift(%)"].values[0]
                                    if drift_perf > relative_yellow * 100:
                                        self.report.loc[
                                            self.report.Metric == a, (x, y, "Relative_warning")
                                        ] = "Yellow Alert"

            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease','axial']."
                )

        self.relative = True

        # for output report columns ordering according to current percentage label
        ordered_columns = (
            self.report.loc[:, (slice(None), slice(None), "Curr_Perc_label")]
            .max()
            .reset_index()
            .sort_values(["level_0", 0], ascending=[True, False])
            .values
        )
        self.report = self.report.reindex([""] + [x[1] for x in ordered_columns], axis=1, level=1)

        # for output report columns ordering
        if self.absolute:
            self.report = self.report.reindex(
                [
                    "",
                    "Curr_perf",
                    "Curr_Perc_label",
                    "Absolute_warning",
                    "Stor_perf",
                    "Stor_Perc_label",
                    "Drift(%)",
                    "Relative_warning",
                ],
                axis=1,
                level=2,
            )
        else:
            self.report = self.report.reindex(
                ["", "Curr_perf", "Curr_Perc_label", "Stor_perf", "Stor_Perc_label", "Drift(%)", "Relative_warning"],
                axis=1,
                level=2,
            )

    def get_report(self):
        """Return the report.

        Returns:
            pd.DataFrame: report of the class.
        """
        return self.report
