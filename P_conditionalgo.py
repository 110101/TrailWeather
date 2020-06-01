import pandas

# abbriviations
# ts - timestamp

def run(dataset):
    # dataset consists out of six rows timestamp: 'dt'; temperature: 'temp'; humidity: 'humidity; dew point:
    # 'dew_point'; wind: 'wind'; weather id: 'weather_id'

    # newest timestamp in dataset
    newest = dataset.tail(1)

    # all information on last rain
    # timestamp of last rain
    rain = dataset.query('(weather_id >= 200) & (weather_id < 700)')
    lastrain = rain.tail(1)

    # time since last rain
    ts_lastrain = (int(newest['dt']) - int(lastrain['dt']))

    # all other rain
    # get timestamp change is bigger than 3600
    col = ['dt', 'weather_id', 'duration', 'intnsty_avrg', 'intnsty_peak']
    rain_data = pandas.DataFrame(columns=col)
    rain_len = rain.shape[0] -1
    rain_start_ts = int(rain.head(1)['dt'].values)
    for row in range(rain_len):
        if rain.iloc[row+1]['dt'] - rain.iloc[row]['dt'] > 3600:
            rain_end_ts = rain.iloc[row]['dt']
            rain_duration = rain_end_ts - rain_start_ts
            rain_data = rain_data.append({'dt': rain.iloc[row]['dt'], 'weather_id': rain.iloc[row]['weather_id'], 'duration': rain_duration,'intnsty_avrg': 0, 'intnsty_peak': 0}, ignore_index=True)
            rain_start_ts = rain.iloc[row+1]['dt']

    # duration of last rain
    lastrain_duration = int(lastrain['dt']) - rain_start_ts

    # intensity of last rain

    # add last rain to rain_data dataset
    # rain_data = rain_data.append(
    #   {'dt': rain.iloc[row]['dt'], 'weather_id': rain.iloc[row]['weather_id'], 'duration': rain_duration,
    #     'intnsty_avrg': 0, 'intnsty_peak': 0}, ignore_index=True)

    # ----
    # Temperatur
    # ----
    # average temp since last rain
    index_lastrain = lastrain.index.values[0]
    index_newest = newest.index.values[0]
    # if index_newest != index_newest:
    temp_curve_lastrain = dataset[130:index_newest]['temp']
    # else:
        # print("currently raining")

    # duration_last_rain_r = duration_last_rain.time_now_UNIX()

    #test output dataset
    # first_rain = t_last_rain.iloc[0]

    #reverse dataset
    # reversed_rain = ts_lastrain.iloc[::-1]

    # test output
    # print(reversed_rain)

    # duration of last rain

    # intensity of last rain

    # temp, wind, sky since last rain
    temp = dataset[['dt', 'temp']]

    # time till rain before last rain

    # intensity of rain before last rain

    print(ts_lastrain)

    prob_road = 0.5
    prob_gravel = 0.8
    prob_trail = 1

    return prob_road, prob_gravel, prob_trail
