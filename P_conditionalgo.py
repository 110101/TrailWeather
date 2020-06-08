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
    # dataset consists out of six rows timestamp: 'dt'; temperature: 'temp'; humidity: 'humidity; dew point:
    # 'dew_point'; wind: 'wind'; weather id: 'weather_id'

    # newest timestamp in dataset
    newest = dataset.tail(1)

    # all information on last rain
    # find all time stamps with rain
    rain = dataset.query('(weather_id >= 200) & (weather_id < 700)')

    # ---
    # information on all "rains"
    # ---

    # last rain / last row
    lastrain_row = rain.tail(1)

    # time since really last rain
    ts_lastrain = (int(newest['dt']) - int(lastrain_row['dt']))

    # shortcut if time since last rain is bigger than max threshold for each road type
    # xxx_may_dry_time in seconds / default 5 days
    road_max_dry_time = 432000
    gravel_max_dry_time = 432000
    trail_max_dry_time = 432000

    if (ts_lastrain > road_max_dry_time) or (ts_lastrain > gravel_max_dry_time) or (ts_lastrain > trail_max_dry_time):

        # all data on the rain
        # get timestamp change is bigger than 3600
        col = ['dt_start', 'dt_end', 'idx_start', 'idx_end','weather_id', 'duration', 'rain_intensity', 'time_since_prevrain', 'temp_since_prevrain', 'wind_since_prevrain', 'humidity_since_prevrain']
        rain_data = pandas.DataFrame(columns=col)

        rain_len = rain.shape[0] - 1
        rain_start_ts = int(rain.head(1)['dt'].values)
        for row in range(rain_len):
            if rain.iloc[row+1]['dt'] - rain.iloc[row]['dt'] > 3600:
                rain_end_ts = rain.iloc[row]['dt']
                rain_duration = rain_end_ts - rain_start_ts

                # rain object
                rain_data = rain_data.append(
                    {'dt_start': rain_start_ts, 'dt_end': rain.iloc[row]['dt'], 'weather_id': rain.iloc[row]['weather_id'], 'duration': rain_duration,
                     'intnsty_avrg': 0, 'intnsty_peak': 0}, ignore_index=True)
                rain_start_ts = rain.iloc[row+1]['dt']

        # duration of last rain
        lastrain_duration = int(lastrain_row['dt']) - rain_start_ts

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

    else:

        prob_road = 0.5
    prob_gravel = 0.8
    prob_trail = 1

    return prob_road, prob_gravel, prob_trail
