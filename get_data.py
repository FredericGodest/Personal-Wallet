"""
This module is gathering data from a Google Sheet file.
"""

# IMPORTS
import pandas as pd
from dotenv import dotenv_values
import os
import numpy as np

def Clean_Googlesheet(df: object, column: str)-> object:
    """
    This function is cleaning data from google sheet to pandas dataframe.

    :param df: Pandas dataframe
    :param column: Column name to clean up
    :return df: Cleaned pandas dataframe
    """

    df[column] = df[column].str.replace(',', '.')
    df[column] = df[column].str.replace('€', '')
    df[column] = df[column].str.replace("\u202f", '')
    df[column] = df[column].str.replace("/", ' & ')
    df[column] = df[column].str.replace("NaN", "0")
    try:
        df[column] = pd.to_numeric(df[column])
    except ValueError:
        pass

    return df

def GoogleSheet_Connection(sheet_name: str)-> object:
    """
    This function is gathering data from google sheet, cleaning it and export it as pandas dataframe.

    :param sheet_name: Google Sheet name to import.
    :return df: pandas dataframe
    """

    # PROD MOD
    if os.environ.get("ENV") == "PROD":
        id = os.environ.get("SHEET_ID")

    # TEST MOD
    else:
        config = dotenv_values(".env")
        id = config["SHEET_ID"]

    url = f"https://docs.google.com/spreadsheets/d/{id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)

    if sheet_name == "Dividende":
        column_list = [
            "Titre",
            "Type",
            "Courtier",
            "cours",
            "PRU",
            "Valorisation",
            "Dividende/an"
        ]

        df = df[column_list].dropna()

        for column in list(df.columns):
            df = Clean_Googlesheet(df, column)

        df["Name"] = df["Titre"] + "-" + df["Courtier"]
        df = df.set_index("Name")
        df["Percent"] = round(df["Valorisation"] / df["Valorisation"].sum() * 100, 2)

    elif sheet_name == "Patrimoine":
        df = df.T
        df.columns = df.iloc[0]
        df = df[1:]

        for column in list(df.columns):
            df = Clean_Googlesheet(df, column)

        df = df.replace(np.nan, 0)


    else:
        for column in list(df.columns):
            if df[column].dtype == object:
                df = Clean_Googlesheet(df, column)

        df = df.replace(np.nan, 0)
        df["Final Abs"] = df["Valeur finale"].abs()


    return df

def Getdata()-> dict:
    """
    This function is gathering all the google sheet files to several pandas dataframe combine in a dictionnary.

    :return dict: dictionnary of pandas dataframe.
    """

    sheet_names = ["Dividende", "Patrimoine", "Cash_Flow"]
    dict_df = {}

    for sheet_name in sheet_names:
        dict_df[sheet_name] = GoogleSheet_Connection(sheet_name)

    return dict_df