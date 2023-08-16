import json
import pandas as pd
import numpy as np

from tdlc import exceptions
from tdlc.utils import constants
from collections import OrderedDict


def records_to_dataframe(records_text, kind, coerce=None):
    if records_text in ["", "[]"]:
        strings = []
    else:
        strings = records_text.strip().split("\n")
    try:
        data_array = [
            json.JSONDecoder(object_pairs_hook=OrderedDict).decode(s) for s in strings
        ]

        if kind == constants.SESSION_KIND_SPARKR and len(data_array) > 0:
            data_array = data_array[0]

        df = pd.DataFrame(data_array)

        if len(data_array) > 0:
            for data in data_array:
                if len(data.keys()) == len(df.columns):
                    df = df[list(data.keys())]
                    break

        # if coerce is None:
        #     coerce = conf.coerce_dataframe()
        if coerce:
            coerce_pandas_df_to_numeric_datetime(df)

        return df
    except ValueError:
        raise exceptions.DataframeParseException(
            post="Cannot parse object as JSON: '{}'".format(strings)
        )


def coerce_pandas_df_to_numeric_datetime(df):
    for column_name in df.columns:
        coerced = False

        if df[column_name].isnull().all():
            continue

        if not coerced and df[column_name].dtype == np.dtype("object"):
            try:
                df[column_name] = pd.to_datetime(df[column_name], errors="raise")
                coerced = True
            except (ValueError, TypeError, OverflowError):
                pass

        if not coerced and df[column_name].dtype == np.dtype("object"):
            try:
                df[column_name] = pd.to_numeric(df[column_name], errors="raise")
                coerced = True
            except (ValueError, TypeError):
                pass



def contains_all_keywords(content, keywords):
    lcontent = content.lower()
    for word in keywords:
        if lcontent.find(word.lower()) < 0:
            return False
    return True

def contains_any_keywords(content, keywords):
    lcontent = content.lower()
    for word in keywords:
        if lcontent.find(word.lower()) >=0:
            return True
    return False


