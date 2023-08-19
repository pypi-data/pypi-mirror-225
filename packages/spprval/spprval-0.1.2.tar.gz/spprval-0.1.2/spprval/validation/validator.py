import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from abc import ABC, abstractmethod

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=RuntimeWarning)


class BaseValidator(ABC):
    def __init__(
        self,
        percent_delta: float = 0.5,
        lower_quantile: float = 0.01,
        upper_quantile: float = 0.99,
    ):
        self.percent_delta = percent_delta
        self.lower_quantile = lower_quantile
        self.upper_quantile = upper_quantile

    @abstractmethod
    def validate(
        self, model_dataset: pd.DataFrame, df_wind_val: pd.DataFrame, act: list
    ):
        pass


class ResourcesValidator(BaseValidator):
    def __init__(self, res: list):
        super().__init__()
        self.res = res

    def validate(
        self, model_dataset: pd.DataFrame, df_wind_val: pd.DataFrame, act: list
    ):
        model_dataset = model_dataset.drop_duplicates()
        act = [c + "_act_fact" for c in act]
        df_perc_agg = pd.DataFrame()
        df_style = pd.DataFrame()
        df_volume = pd.DataFrame()
        fig_dict = dict()
        for i in model_dataset.index:
            c_pair = [ci for ci in act if model_dataset.loc[i, ci] != 0]
            c_act = c_pair
            volume = [model_dataset.loc[i, ci] for ci in c_act]
            delta = [self.percent_delta * volume_i for volume_i in volume]
            not_c = [ci for ci in act if ci not in c_act]
            zero_ind = df_wind_val[not_c][(df_wind_val[not_c] == 0).all(axis=1)].index
            sample_non = df_wind_val.loc[zero_ind, :]

            non_zero = sample_non[c_act][(sample_non[c_act] != 0).all(axis=1)].index
            sample_non = pd.DataFrame(sample_non.loc[non_zero, :])
            sample = pd.DataFrame()
            for j, ci in enumerate(c_act):
                sample = sample_non.loc[
                    (sample_non[ci] >= volume[j] - delta[j])
                    & (sample_non[ci] <= volume[j] + delta[j])
                ]
            sample = pd.DataFrame(sample)

            if sample.shape[0] > 4:
                for r in self.res:
                    value = model_dataset.loc[i, r]
                    q1, q99 = np.quantile(
                        sample[r].values, [self.lower_quantile, self.upper_quantile]
                    )
                    if value < q1 or value > q99:
                        df_style.loc[i, r] = "red"
                        df_volume.loc[i, r] = value
                        for ci in c_act:
                            key, blue_points, black_points, star = self._process_key(
                                c_act, r, ci, sample, sample_non, model_dataset, i
                            )

                            color = "red"
                            fig_dict[key] = {
                                "Blue points": blue_points,
                                "Black points": black_points,
                                "Star": star,
                                "Color": color,
                            }
                    else:
                        df_style.loc[i, r] = "green"
                        df_volume.loc[i, r] = value
                        for ci in c_act:
                            key, blue_points, black_points, star = self._process_key(
                                c_act, r, ci, sample, sample_non, model_dataset, i
                            )

                            color = "green"
                            fig_dict[key] = {
                                "Blue points": blue_points,
                                "Black points": black_points,
                                "Star": star,
                                "Color": color,
                            }
                df_style.loc[i, "Наименование"] = str(c_act)
                df_volume.loc[i, "Наименование"] = str(c_act)
            elif sample.shape[0] <= 4:
                df_style.loc[i, "Наименование"] = str(c_act)
                df_volume.loc[i, "Наименование"] = str(c_act)
                for r in self.res:
                    value = model_dataset.loc[i, r]
                    df_style.loc[i, r] = "grey"
                    df_volume.loc[i, r] = value
        new_df_color = df_style[(df_style != "grey").all(1)]
        not_perc = (
            (
                (df_style.shape[0] * df_style.shape[1])
                - (new_df_color.shape[0] * new_df_color.shape[1])
            )
            / (df_style.shape[0] * df_style.shape[1])
        ) * 100
        j = 0

        for c in act:
            new_sample = new_df_color.loc[
                new_df_color["Наименование"].str.count(c) != 0
            ]
            if new_sample.shape[0] != 0:
                for r in self.res:
                    df_perc_agg.loc[j, "Наименование ресурса"] = r
                    df_perc_agg.loc[j, "Наименование работы"] = c
                    value_dict = new_sample[r].value_counts().to_dict()
                    if "green" in list(value_dict.keys()):
                        df_perc_agg.loc[j, "Соотношение"] = round(
                            ((value_dict["green"]) / new_sample.shape[0]) * 100
                        )
                    else:
                        df_perc_agg.loc[j, "Соотношение"] = 0
                    j += 1
            else:
                for r in self.res:
                    df_perc_agg.loc[j, "Наименование ресурса"] = r
                    df_perc_agg.loc[j, "Наименование работы"] = c
                    df_perc_agg.loc[j, "Соотношение"] = 0
                    j += 1

        norm_perc = df_perc_agg["Соотношение"].mean()
        df_final_volume = pd.DataFrame()
        df_final_style = pd.DataFrame()
        for i, p in enumerate(list(df_volume["Наименование"].unique())):
            sample1 = df_volume.loc[df_volume["Наименование"] == p]
            sample2 = df_style.loc[df_style["Наименование"] == p]
            date = str(sample1.index[0]) + " " + str(sample1.index[-1])
            df_final_volume.loc[i, "Наименование"] = p
            df_final_volume.loc[i, "Даты"] = date
            df_final_volume.loc[i, self.res] = sample1.loc[sample1.index[0], self.res]
            df_final_style.loc[i, "Наименование"] = p
            df_final_style.loc[i, "Даты"] = date
            df_final_style.loc[i, self.res] = sample2.loc[sample2.index[0], self.res]

        return (
            df_perc_agg,
            df_final_volume,
            df_final_style,
            fig_dict,
            not_perc,
            norm_perc,
        )

    @staticmethod
    def _process_key(c_act, r, ci, sample, sample_non, model_dataset, i):
        key = str(c_act) + " " + r + " " + ci
        blue_points = {
            "x": list(sample_non[ci].values),
            "y": list(sample_non[r].values),
        }
        black_points = {
            "x": list(sample[ci].values),
            "y": list(sample[r].values),
        }
        star = {
            "x": model_dataset.loc[i, ci],
            "y": model_dataset.loc[i, r],
        }
        return key, blue_points, black_points, star


class WorksValidator(BaseValidator):
    def validate(
        self, model_dataset: pd.DataFrame, df_wind_val: pd.DataFrame, act: list
    ):
        model_dataset = model_dataset.drop_duplicates()
        df_stat = pd.DataFrame()
        dist_dict = dict()
        j = 0
        for c in act:
            for i in model_dataset.index:
                value = model_dataset.loc[i, c]
                if value != 0:
                    sample = df_wind_val.loc[df_wind_val[c] != 0]
                    if sample.shape[0] != 0:
                        q1, q99 = np.quantile(
                            sample[c].values, [self.lower_quantile, self.upper_quantile]
                        )
                        q1 = int(q1)
                        q99 = int(q99)
                        if value < q1 or value > q99:
                            df_stat.loc[j, "Работа"] = c
                            df_stat.loc[j, "Метка работы"] = "red"
                            key = c
                            line = value
                            color = "red"
                            counts, bins, _ = plt.hist(sample[c].values)
                            dist_dict[key] = {
                                "Line": line,
                                "color": color,
                                "Hight": counts,
                                "Bins": bins,
                                "Q1": q1,
                                "Q99": q99,
                            }
                        else:
                            df_stat.loc[j, "Работа"] = c
                            df_stat.loc[j, "Метка работы"] = "green"
                            key = c
                            line = value
                            color = "green"
                            counts, bins, _ = plt.hist(sample[c].values)
                            dist_dict[key] = {
                                "Line": line,
                                "color": color,
                                "Hight": counts,
                                "Bins": bins,
                                "Q1": q1,
                                "Q99": q99,
                            }
                        j += 1
                    else:
                        df_stat.loc[j, "Работа"] = c
                        df_stat.loc[j, "Метка работы"] = "grey"
        not_grey = df_stat.loc[df_stat["Метка работы"] != "grey"]
        not_perc = ((df_stat.shape[0] - not_grey.shape[0]) / df_stat.shape[0]) * 100
        norm_df = df_stat.loc[df_stat["Метка работы"] == "green"]
        norm_perc = ((not_grey.shape[0] - norm_df.shape[0]) / not_grey.shape[0]) * 100
        df_final_stat = pd.DataFrame()
        for i, c in enumerate(act):
            df_final_stat.loc[i, "Наименование"] = c
            sample = not_grey.loc[not_grey["Работа"] == c]
            count_dict = sample["Метка работы"].value_counts().to_dict()
            if "green" not in list(count_dict.keys()):
                df_final_stat.loc[i, "Среднедневная выработка"] = 0
            else:
                df_final_stat.loc[i, "Среднедневная выработка"] = (
                    count_dict["green"] / sample.shape[0]
                ) * 100
        return df_final_stat, dist_dict, norm_perc, not_perc


class TimeValidator(BaseValidator):
    def validate(
        self, df_wind_model: pd.DataFrame, df_wind_val: pd.DataFrame, act: list
    ):
        df_wind_model = df_wind_model.drop_duplicates()
        df_stat = pd.DataFrame()
        dict_fig = {}
        final_df = pd.DataFrame()
        j = 0
        for c in act:
            dict_fig[c] = []
            for i in df_wind_model.index:
                if df_wind_model.loc[i, c] != 0:
                    c_act = [c]
                    volume = [df_wind_model.loc[i, ci] for ci in c_act]
                    delta = [self.percent_delta * volume_i for volume_i in volume]
                    sample = df_wind_val.copy()
                    for k, ci in enumerate(c_act):
                        sample = sample.loc[
                            (sample[ci] >= volume[k] - delta[k])
                            & (sample[ci] <= volume[k] + delta[k])
                        ]
                    if sample.shape[0] > 3:
                        df_stat, dict_for_sample = self.handle_sample(
                            i,
                            c,
                            df_wind_model,
                            sample,
                            df_wind_val,
                            df_stat,
                            j,
                        )
                        dict_fig[c].append(
                            {
                                "volume": volume,
                                "fig_data": dict_for_sample,
                                "color": dict_for_sample["Color"],
                            }
                        )
                    else:
                        df_stat.loc[j, "Работа"] = c
                        df_stat.loc[j, "Метка времени"] = "grey"
                    j += 1

        not_grey = df_stat.loc[df_stat["Метка времени"] != "grey"]
        not_perc = ((df_stat.shape[0] - not_grey.shape[0]) / df_stat.shape[0]) * 100
        norm_df = df_stat.loc[df_stat["Метка времени"] == "green"]
        norm_perc = 0
        if not_perc != 100:
            norm_perc = (
                (not_grey.shape[0] - norm_df.shape[0]) / not_grey.shape[0]
            ) * 100

        final_df = self.finalize_dataframe(act, final_df, not_grey)
        return final_df, dict_fig, norm_perc, not_perc

    def handle_sample(self, i, c, df_wind_model, sample, df_wind_val, df_stat, j):
        value = df_wind_model.loc[i,c.split('_act_fact')[0]+'_real_time_act']
        q1, q99 = np.quantile(sample[c.split('_act_fact')[0]+'_real_time_act'].values, [self.lower_quantile, self.upper_quantile])
        q1 = int(q1)
        q99 = int(q99)
        if value < q1 or value > q99:
            color = "red"
        else:
            color = "green"
        df_stat.loc[j, "Работа"] = c
        df_stat.loc[j, "Метка времени"] = color
        sample_dict = self.create_figure_dict(
            c, color, sample, df_wind_val, df_wind_model, i, q1, q99
        )
        return df_stat, sample_dict

    @staticmethod
    def create_figure_dict(
        c,
        color,
        sample,
        df_wind_val: pd.DataFrame,
        df_wind_model: pd.DataFrame,
        i,
        q1,
        q99,
    ):
        blue_points = {
            "x": list(df_wind_val[c].values),
            "y": list(df_wind_val[c.split('_act_fact')[0]+'_real_time_act'].values),
        }
        black_points = {
            "x": list(sample[c].values),
            "y": list(sample[c.split('_act_fact')[0]+'_real_time_act'].values),
        }
        star = {
            "x": df_wind_model.loc[i, c],
            "y": df_wind_model.loc[i, c.split('_act_fact')[0]+'_real_time_act'],
        }
        return {
            "Blue points": blue_points,
            "Black points": black_points,
            "Star": star,
            "Color": color,
            "Q1": q1,
            "Q99": q99,
        }

    @staticmethod
    def finalize_dataframe(act: list, final_df, not_grey):
        for i, c in enumerate(act):
            final_df.loc[i, "Наименование"] = c
            sample = not_grey.loc[not_grey["Работа"] == c]
            count_dict = sample["Метка времени"].value_counts().to_dict()
            if "green" not in list(count_dict.keys()):
                final_df.loc[i, "Время на ед. объёма"] = 0
            else:
                final_df.loc[i, "Время на ед. объёма"] = (
                    count_dict["green"] / sample.shape[0]
                ) * 100
        return final_df
