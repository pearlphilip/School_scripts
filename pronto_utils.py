import os

import wget
import zipfile 

from urllib.request import urlopen, URLError
import matplotlib.pyplot as plt
import pandas as pd


def download_if_needed(url, filename):

    """ Downloads the data from a given URL, if not already present in the directory, or displays any of the following:
        1. The file already exists.
        2. URL does not exist.
        3. Server is not responding.
    """

    if os.path.exists(filename):
        explanation = filename+ ' already exists'
        return explanation
    else:
        try:
            r = urlopen(url)
        except URLError as e:
            r = e
        if r.code < 400:
            wget.download(url)
            explanation = 'downloading'
            return explanation
        elif r.code>=400 and r.code<500:
            explanation = 'Url does not exist'
            return explanation
        else:
            explanation = 'Server is not responding'
            return explanation

        
def get_pronto_data():

    """ Downloads the Pronto bike data if not present in directory."""

    download_if_needed('https://s3.amazonaws.com/pronto-data/open_data_year_one.zip', 'open_data_year_one.zip')

    
def get_trip_data():

    """ Unzips the Pronto bike data zip folder and returns the trip data csv file from it."""
    
    get_pronto_data()
    zf=zipfile.ZipFile('open_data_year_one.zip')
    file_handle=zf.open('2015_trip_data.csv')
    return pd.read_csv(file_handle)
    
    
def get_weather_data():

    """ Unzips the Pronto bike data zip folder and returns the weather data csv file from it."""
    
    get_pronto_data()
    zf=zipfile.ZipFile('open_data_year_one.zip')
    file_handle=zf.open('2015_weather_data.csv')
    return pd.read_csv(file_handle)


def get_trips_and_weather():

    """ Merges the weather and trip data csv files, after setting the indices of 
        both to the Date of the weather measurement or bike ride."""

    trips= get_trip_data()
    weather = get_weather_data()
    trip_date=pd.DatetimeIndex(trips['starttime'])
    trip_date.date
    trips_by_date = trips.pivot_table('trip_id', aggfunc='count', index=trip_date.date, columns='usertype')
    weather = weather.set_index('Date')
    weather.index=pd.DatetimeIndex(weather.index)
    weather=weather.iloc[:-1]
    return weather.join(trips_by_date)


def plot_daily_totals():

    """ Plots the daily total bike rides of both Annual and Short-Term Pass Holders"""

    data = get_trips_and_weather()
    fig, ax = plt.subplots(2, figsize=(14,6), sharex=True)
    data['Annual Member'].plot(ax = ax[0], title = 'Annual Member')
    data['Short-Term Pass Holder'].plot(ax=ax[1], title = 'Short-Term Pass Holder')
    return fig.savefig('plot_daily_totals.jpg')


def remove_data(filename):

    """ Removes the file specified from the directory, if present, else raises exception."""

    if os.path.isfile(filename):
        os.remove(filename)
        explanation = 'Data file removed'
        return explanation
    else:
        explanation = 'No such data file exists that can be removed'
        return explanation


# Run the following code if the file is run at the command line
if __name__ == "__main__":
  plot_daily_totals()