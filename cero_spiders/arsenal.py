# coding=utf-8
"""
title: 
author: cero
Create on: 2018/7/2
"""
import os
import pandas as pd
import numpy as np
from pandas.io import sql
from sqlalchemy import create_engine

from .settings import BASE_DIR

CONN = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'dota2.db'))


def df2tbl(df, tbl, conn):
    """
    insert into ...
    :param df:
    :param tbl: tbl_name
    :param conn:
    :return:
    """
    if df.empty:
        return
    df = df.astype(object).where(pd.notnull(df), None)
    columns = df.columns.tolist()
    sql_string = '''
    INSERT INTO {tbl} ({cols})
    VALUES ({vals})
    '''.format(tbl=tbl, cols=','.join(columns),
               vals=','.join(['?']*len(columns)))
    sql.execute(sql_string, conn, params=[tuple(row.values.tolist()) for index, row in df.iterrows()])


def clean_tbl(tbl, conn):
    """
    delete from ...
    :param tbl:
    :param conn:
    :return:
    """
    sql_string = '''
    DELETE FROM {tbl}
    '''.format(tbl=tbl)
    sql.execute(sql_string, conn)


def isnan(v):
    if v != v:
        return True
    else:
        return False
