# -*- coding: utf-8 -*-

import pandas as pd
import plotly.express as px


#### functions for data handling to be used in app.py


def get_data(download=False):
    '''
    Loading crime data from website or local file (default local).
    '''
    if download:
        excel = 'https://www.web.statistik.zh.ch/jahrbuch/tabellen/excel/JB_D5-101.xlsx'
    else:
        excel = 'JB_D5-101.xlsx'

    df = pd.read_excel(excel,skiprows=4,skipfooter=2)
    
    # rename first column
    df = df.rename(columns={'Unnamed: 0':'Art der Straftat'})
    return df

def add_levels(df):
    ''' 
    Adding levels to df for filtering.
    '''
    level_ranks = df.loc[(df['Art der Straftat'].str.startswith('Total'))|(df['Art der Straftat'].str.startswith('Übrige')),'Art der Straftat'].rank()
    df.loc[df.index.isin(level_ranks.index),'Ebene'] = level_ranks
    df['Unterebene'] = df['Ebene'].fillna(method='ffill')
    return df

def preprocessing_chart(df):
    '''
    Preprocessing of df for chart.
    '''
    df = df.set_index('Art der Straftat').stack().reset_index()
    df.columns = ['Art der Straftat','Jahr','Anzahl erfasste Straftaten (inkl. Versuche)']
    return df
def chart(df):
    '''
    Create figure object.
    '''
    fig = px.line(df,log_y=True,x='Jahr',y='Anzahl erfasste Straftaten (inkl. Versuche)',line_group='Art der Straftat',color='Art der Straftat')
    return fig

def select_sub(df,picked):
    '''
    Select data of sub levels bei given super level (picked).
    '''
    level = df.loc[df['Art der Straftat']==picked,'Unterebene'].iloc[0]
    return df[(df['Unterebene']==level) & (df['Ebene'].isna())]

def chart_total_crimes(df):
    '''
    Create chart with overall data.
    '''   
    overall = df.loc[df['Art der Straftat'].str.startswith('Gesamt')]
    fig = px.area(preprocessing_chart(overall),x='Jahr',y='Anzahl erfasste Straftaten (inkl. Versuche)')#,title=overall['Art der Straftat'].iloc[0])
    return fig
