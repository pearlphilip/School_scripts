import wget, os, pandas as pd, zipfile, matplotlib.pyplot as plt


def download_if_needed(url, filename):
    if os.path.exists(filename):
        print(filename, 'already exists')
    else:
        print('downloading')
        wget.download(url)
		
def get_pronto_data():
    download_if_needed('https://s3.amazonaws.com/pronto-data/open_data_year_one.zip', 'open_data_year_one.zip')

def get_trip_data():
    get_pronto_data()
    zf=zipfile.ZipFile('open_data_year_one.zip')
    file_handle=zf.open('2015_trip_data.csv')
    return pd.read_csv(file_handle)
	
def get_weather_data():
    get_pronto_data()
    zf=zipfile.ZipFile('open_data_year_one.zip')
    file_handle=zf.open('2015_weather_data.csv')
    return pd.read_csv(file_handle)
	
def get_trips_and_weather():
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
    data = get_trips_and_weather()
    fig, ax = plt.subplots(2, figsize=(14,6), sharex=True)
    data['Annual Member'].plot(ax = ax[0], title = 'Annual Member')
    data['Short-Term Pass Holder'].plot(ax=ax[1], title = 'Short-Term Pass Holder')
    fig.savefig('plot_daily_totals.jpg')

