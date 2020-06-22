import pandas

# abbriviations
# ts - timestamp

class rain_obj:
    def __init__(self):
        self.rain_start_ts = ""
        self.rain_end_ts = ""
        self.duration = ""
        self.intensity_min = ""
        self.intensity_max = ""
        self.intensity_avrg = ""
        self.time_2_prev_rain = ""
        self.temp_2_prev_rain = ""
        self.hum_2_prev_rain = ""
        self.wind_2_prev_rain = ""


def run(dataset):
    # data set consists out of six rows timestamp: 'dt'; temperature: 'temp'; humidity: 'humidity; dew point:
    # 'dew_point'; wind: 'wind'; weather id: 'weather_id'

    # last timestamp in data set
    newest = dataset.tail(1)

    # find all time stamps with rain
    rain = dataset.query('(weather_id >= 200) & (weather_id < 700)')

    # reverse rain data set to get it more logical, when working from top to bottom
    # rain.iloc[::-1] -- used reverse for loop

    # information on all "rains"
    # ---

    # last rain / last row
    lastrain_row = rain.tail(1)

    # short cut if last rain is really long ago
    # time since really last rain
    ts_lastrain = (int(newest['dt']) - int(lastrain_row['dt']))

    # xxx_may_dry_time in seconds / default 5 days
    max_dry_time = 432000

    # if last rain is below threshold do the math
    if ts_lastrain != 0:
        if ts_lastrain < max_dry_time:

            # all data on the rain
            # get timestamp change is bigger than 3600
            col = ['dt_start', 'dt_end', 'idx_start', 'idx_end','weather_id', 'duration', 'rain_intensity',
                   'time_since_prevrain', 'temp_since_prevrain', 'wind_since_prevrain', 'humidity_since_prevrain']
            rain_data = pandas.DataFrame(columns=col)

            # reference point "now" or timestamp of following rain
            ref_timestamp = int(newest['dt'])

            # end of last rain
            rain_end_ts = int(lastrain_row['dt'])
            rain_end_idx = rain.tail(1).index[0]

            rain_len = rain.shape[0] - 1
            for row in range(rain_len,1,-1):
                test = row
                if rain.iloc[row]['dt'] - rain.iloc[row-1]['dt'] > 3600:
                    # time since rain until ref timestamp
                    time_since_rain = ((ref_timestamp - rain_end_ts) / 3600) + 1

                    # temp since rain
                    temp_since_rain = dataset.query('dt <= @ref_timestamp and dt >= @rain_end_ts')['temp'].mean()

                    # wind since rain
                    wind_since_rain = dataset.query('dt <= @ref_timestamp and dt >= @rain_end_ts')['wind'].mean()

                    # humidity since rain
                    hum_since_rain = dataset.query('dt <= @ref_timestamp and dt >= @rain_end_ts')['humidity'].mean()

                    # initial trail condition
                    # ---
                    # start of rain
                    rain_start_ts = rain.iloc[row]['dt']
                    rain_start_idx = rain[rain['dt'] == rain.iloc[row]['dt']].index[0]

                    # rain duration
                    rain_duration = ((rain_end_ts - rain_start_ts) / 3600) + 1

                    # rain intensity
                    rain_intensity = rain.query('dt >= @rain_start_ts and dt <= @rain_end_ts')['rain_mm'].sum()

                    # equation goes here
                    # ...


                    # rain object
                    rain_data = rain_data.append(
                        {'dt_start': rain_end_ts, 'dt_end': rain.iloc[row]['dt'], 'weather_id': rain.iloc[row]['weather_id'], 'duration': rain_duration,
                         'intnsty_avrg': 0, 'intnsty_peak': 0}, ignore_index=True)
                    # update rain_end with next "rain block" from data set and reference timestamp
                    rain_end_ts = rain.iloc[row-1]['dt']
                    ref_timestamp = rain_start_ts
                    ref_idx = rain_start_idx

            # duration of last rain
            lastrain_duration = int(lastrain_row['dt']) - rain_end_ts

            # intensity of last rain


            # add last rain to rain_data dataset
            rain_data = rain_data.append(
               {'dt': int(lastrain_row['dt']), 'weather_id': int(lastrain_row['weather_id']), 'duration': lastrain_duration,
                 'intnsty_avrg': 0, 'intnsty_peak': 0}, ignore_index=True)

            # ----
            # Temperatur
            # Temp curve between rain
            # ----
            # average temp since last rain
            # index_lastrain = lastrain.index.values[0]
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

            # ----
            # Humidity
            # Humidity curve between rain
            # ----

            # ----
            # Wind
            # Wind intensity between rain
            # ----

            # second shortcut

            prob_road = 0.5
            prob_gravel = 0.5
            prob_trail = 0.5

        elif ts_lastrain > max_dry_time:

            prob_road = 0
            prob_gravel = 0
            prob_trail = 0

    elif ts_lastrain == 0:

        prob_road = 2
        prob_gravel = 2
        prob_trail = 2

    return prob_road, prob_gravel, prob_trail
