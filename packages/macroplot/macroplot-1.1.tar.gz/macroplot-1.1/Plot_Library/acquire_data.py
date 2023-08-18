import pandas as pd
from pandas_datareader import wb
import country_converter as coco
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import imageio
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt


def acquire_data(variable, name, countries, start_date='1960-01-01', end_date='2022-12-31'):

    df = wb.download(indicator=variable, country=countries, start=start_date, end=end_date)
    df = df.reset_index().sort_values('country').set_index('country')
    df = df.pivot(columns='year')
    columns = [f'{year}_{col}'.format(col, year) for year in df.columns for col in variable]
    df = df.reset_index()
    df.rename(columns={variable: name}, inplace=True)
    df.columns = ['{} {}'.format(col[0], col[1]) for col in df.columns]
    df.rename(columns={'countryYear': 'Country'})
    df['Country Code'] = coco.convert(names=df['country '], to='ISO3')
    df=df.where(df['Country Code'] != "not found")
    df = df.dropna(axis=1, how='all')
    
    df.iloc[:, :1] = df.iloc[:, :1].apply(lambda row: row.ffill().bfill(), axis=1)
    df.dropna(how = 'all', inplace = True)
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]
    df= df.rename(columns = {'country ': 'Country'})
    return df
