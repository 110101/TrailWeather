import pandas
from datetime import datetime

# abbriviations
# ts - timestamp

def run(dataset):
    # data set consists out of six rows timestamp: 'dt'; temperature: 'temp'; humidity: 'humidity; dew point:
    # 'dew_point'; wind: 'wind'; weather id: 'weather_id'

    # last timestamp in data set
    newest = dataset.tail(1)

    # find all time stamps with rain
    rain = dataset.query('(weather_id >= 200) & (weather_id < 700)')

    # information on all "rains"
    # ---
    if rain.empty == False:
        # last rain / last row
        lastrain_row = rain.tail(1)

        # short cut if last rain is really long ago
        # time since really last rain
        # reference point "now" or timestamp of following rain
        ref_timestamp = int(datetime.now(tz=None).timestamp())

        ts_lastrain = (int(newest['dt']) - int(lastrain_row['dt']))

        # xxx_may_dry_time in seconds / default 5 days
        max_dry_time = 432000

        # if last rain is below threshold do the math
        if ts_lastrain != 0 and ts_lastrain < max_dry_time:
                # status bit: there was rain in the past 5 days
                rain_status = 1

                # all data on the rain
                # get timestamp change is bigger than 3600
                col = ['dt_start', 'dt_end','weather_id', 'rain_duration', 'rain_intensity',
                       'time_since_prevrain', 'temp_since_rain', 'wind_since_rain', 'hum_since_rain']
                rain_data = pandas.DataFrame(columns=col)



                # overall last rain and additional info
                # end of last rain (overall)
                rain_end_ts = int(lastrain_row['dt'])
                rain_end_idx = rain.tail(1).index[0]

                # time since rain until ref timestamp in hours
                # -1 because of 1 hour blocks in the data set
                time_since_rain = ((ref_timestamp - rain_end_ts) / 3600) - 1

                # temp since rain
                temp_since_rain = dataset.query('dt <= @ref_timestamp and dt >= @rain_end_ts')['temp'].mean()

                # wind since rain
                wind_since_rain = dataset.query('dt <= @ref_timestamp and dt >= @rain_end_ts')['wind'].mean()

                # humidity since rain
                hum_since_rain = dataset.query('dt <= @ref_timestamp and dt >= @rain_end_ts')['humidity'].mean()

                # determine rain duration and further "rain" in the time frame
                rain_len = rain.shape[0] - 1
                for row in range(rain_len,0,-1):
                    if row != 0:
                        if rain.iloc[row]['dt'] - rain.iloc[row-1]['dt'] > 3600:
                            # start of rain
                            rain_start_ts = rain.iloc[row]['dt']
                            # rain_start_idx = rain[rain['dt'] == rain.iloc[row]['dt']].index[0]

                            # rain duration
                            rain_duration = ((rain_end_ts - rain_start_ts) / 3600) + 1

                            # rain intensity
                            rain_intensity = rain.query('dt >= @rain_start_ts and dt <= @rain_end_ts')['rain_mm'].sum()

                            # rain object
                            rain_data = rain_data.append(
                                {'dt_start': rain_end_ts, 'dt_end': rain.iloc[row]['dt'], 'weather_id': rain.iloc[row]['weather_id'], 'rain_duration': rain_duration,
                                 'rain_intnsty': rain_intensity }, ignore_index=True)

                            # update rain_end with next "rain block" from data set and reference timestamp
                            rain_end_ts = rain.iloc[row-1]['dt']
                            ref_timestamp = rain_start_ts

                        # condition if rain is only 1 hour
                        elif (rain.iloc[row]['dt'] - rain.iloc[row-1]['dt'] == 3600) and (row == 1):
                            rain_start_ts = rain.iloc[row-1]['dt']

                            # rain duration
                            rain_duration = ((rain_end_ts - rain_start_ts) / 3600) + 1

                            # rain intensity
                            rain_intensity = rain.query('dt >= @rain_start_ts and dt <= @rain_end_ts')['rain_mm'].sum()

                            # rain object
                            rain_data = rain_data.append(
                                {'dt_start': rain_end_ts, 'dt_end': rain.iloc[row]['dt'], 'weather_id': rain.iloc[row]['weather_id'], 'rain_duration': rain_duration,
                                 'rain_intnsty': rain_intensity }, ignore_index=True)

                            # update rain_end with next "rain block" from data set and reference timestamp
                            rain_end_ts = rain.iloc[row-1]['dt']
                            ref_timestamp = rain_start_ts
                if rain_len == 0:
                    rain_duration = 1
                    rain_intensity = rain.query('dt == @rain_end_ts')['rain_mm'].sum()
                    # rain object
                    rain_data = rain_data.append(
                        {'dt_start': rain_end_ts, 'dt_end': rain_end_ts,
                         'weather_id': rain.query('dt == @rain_end_ts')['weather_id'], 'rain_duration': rain_duration,
                         'rain_intnsty': rain_intensity}, ignore_index=True)

                # duration of last rain - MVP - only consider last rain and its duration
                if rain_data.empty == False:
                    lastrain_duration = float(rain_data.head(1)['rain_duration'])
                    lastrain_intensity = float(rain_data.head(1)['rain_intnsty'])

        elif ts_lastrain > max_dry_time:
            # last rain to long ago
            rain_status = 0  # no rain > 0
            time_since_rain = 99  # not relevant > 99
            lastrain_duration = 99  # not relevant > 99
            lastrain_intensity = 99  # not relevant > 99

        elif ts_lastrain == 0:
            # it's raining, let's get dirty or shred on an other day!
            rain_status = 50            # it's raining > 50
            time_since_rain = 50         # it's raining > 50
            lastrain_duration = 99      # not relevant > 99
            lastrain_intensity = 99     # not relevant > 99

    else:
        # no rain
        rain_status = 0  # no rain > 0
        time_since_rain = 99  # not relevant > 99
        lastrain_duration = 99  # not relevant > 99
        lastrain_intensity = 99  # not relevant > 99

    return {'rain_status': rain_status, 'time_since_rain_h': str(time_since_rain), 'lastrain_duration_h': str(lastrain_duration), 'lastrain_intensity_mm': str(lastrain_intensity)}

