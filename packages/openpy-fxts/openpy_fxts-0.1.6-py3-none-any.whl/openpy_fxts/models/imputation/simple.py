# -*- coding: utf-8 -*-
# @Time    : 25/03/2023
# @Author  : Ing. Jorge Lara
# @Email   : jlara@iee.unsj.edu.ar
# @File    : ------------
# @Software: PyCharm

import pandas as pd
from sklearn.impute import SimpleImputer
from openpy_fxts.mdits.utilities.Utils import Metrics, Utils
from openpy_fxts.mdits.base_lib import init_models
import impyute as impy
import numpy as np

mt = Metrics()


class imp_basic(init_models):
    
    def __init__(
            self,
            df_miss: pd.DataFrame = None,
            df_true: pd.DataFrame = None
    ):
        super().__init__(df_miss, df_true)
        self.df_miss = df_miss
        self.df_true = df_true

    def constan(
            self,
            method: list
    ):
        """
        :param self.df_miss:
        :param method:
        :param self.df_true:
        :return:
        """
        dict_skelarn, dict_metrics = dict(), dict()
        # imputing with a constan
        for kk in method:
            df_imputation = self.df_miss.copy(deep=True)
            model = SimpleImputer(strategy=kk)
            df_imputation.iloc[:, :] = model.fit_transform(df_imputation)
            dict_skelarn[kk] = df_imputation
            dict_metrics = mt.add_dict_metrics(
                self.df_true,
                df_imputation,
                dict_metrics,
                kk
            )

        return dict_skelarn, dict_metrics

    def fillna(
            self,
            list_method: list = None,
            aux: str = 'mean'
    ):
        """
        :param list_fillna:
        :return:
        """
        dict_fillna, dict_metrics = dict(), dict()
        for i in list_method:
            df_imp = self.df_miss.copy(deep=True)
            df_imp.fillna(method=i, inplace=True)
            if Utils(df_imp).check_missing():
                model = SimpleImputer(strategy=aux)
                df_imp.iloc[:, :] = model.fit_transform(df_imp)
            dict_fillna[i] = df_imp
            dict_metrics = mt.add_dict_metrics(
                self.df_true,
                df_imp,
                dict_metrics,
                i
            )
        return dict_fillna, dict_metrics

    def moving_window(
            self,
            nindex=None,
            wsize=3,
            errors="coerce",
            func=np.mean,
            inplace=False,
            **kwargs
    ):
        list_aux = Utils(self.df_miss).list_column_missing()
        X_imp = self.df_miss.copy()
        while X_imp.isnull().sum().sum() > 0:
            X_imp = impy.moving_window(
                X_imp.to_numpy(),
                nindex=nindex,
                wsize=wsize,
                errors=errors,
                func=func,
                inplace=inplace
            )
            X_imp = pd.DataFrame(X_imp, columns=self.df_miss.columns)
            X_imp['datetime'] = self.df_miss.index
            X_imp.set_index('datetime', inplace=True)
        if self.df_true is None:
            return X_imp
        else:
            dict_aux = dict()
            dict_aux = mt.add_dict_metrics(self.df_true[list_aux], X_imp[list_aux], dict_aux, 'moving_window')
            return X_imp, dict_aux['moving_window']

        return

    def interpolate(
            self,
            method: list,
            axis=0,
            limit=None,
            inplace=True,
            limit_direction=None,
            limit_area=None,
            downcast=None,
            order=2,
            aux: str = 'mean'
    ):
        """
        :param list_methods:
        :param axis:
        :param limit:
        :param inplace:
        :param limit_direction:
        :param limit_area:
        :param downcast:
        :param order:
        :return:
        """
        dict_interpolate, dict_metrics = dict(), dict()
        for kk in method:
            df_imp = self.df_miss.copy(deep=True)
            df_imp.interpolate(
                method=kk,
                axis=axis,
                limit=limit,
                inplace=inplace,
                limit_direction=limit_direction,
                limit_area=limit_area,
                downcast=downcast,
                order=order
            )
            if Utils(df_imp).check_missing():
                model = SimpleImputer(strategy=aux)
                df_imp.iloc[:, :] = model.fit_transform(df_imp)
            dict_interpolate[kk] = df_imp
            dict_metrics = mt.add_dict_metrics(
                self.df_true,
                df_imp,
                dict_metrics,
                kk
            )
        return dict_interpolate, dict_metrics
