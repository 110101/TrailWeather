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

    # information on all "rains"
    # ---
    if rain.empty == False:
        # last rain / last row
        lastrain_row = rain.tail(1)

        # short cut if last rain is really long ago
        # time since really last rain
        ts_lastrain = (int(newest['dt']) - int(lastrain_row['dt']))

        # xxx_may_dry_time in seconds / default 5 days
        max_dry_time = 432000

        # if last rain is below threshold do the math
        if ts_lastrain != 0 and ts_lastrain < max_dry_time:
                # all data on the rain
                # get timestamp change is bigger than 3600
                col = ['dt_start', 'dt_end','weather_id', 'duration', 'rain_intensity',
                       'time_since_prevrain', 'temp_since_prevrain', 'wind_since_prevrain', 'humidity_since_prevrain']
                rain_data = pandas.DataFrame(columns=col)

                # reference point "now" or timestamp of following rain
                ref_timestamp = int(newest['dt'])

                # end of last rain
                rain_end_ts = int(lastrain_row['dt'])
                rain_end_idx = rain.tail(1).index[0]

                # time since rain until ref timestamp in hours
                time_since_rain = ((ref_timestamp - rain_end_ts) / 3600) + 1

                # temp since rain
                temp_since_rain = dataset.query('dt <= @ref_timestamp and dt >= @rain_end_ts')['temp'].mean()

                # wind since rain
                wind_since_rain = dataset.query('dt <= @ref_timestamp and dt >= @rain_end_ts')['wind'].mean()

                # humidity since rain
                hum_since_rain = dataset.query('dt <= @ref_timestamp and dt >= @rain_end_ts')['humidity'].mean()

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
                                {'dt_start': rain_end_ts, 'dt_end': rain.iloc[row]['dt'], 'weather_id': rain.iloc[row]['weather_id'], 'duration': rain_duration,
                                 'intnsty': rain_intensity }, ignore_index=True)

                            # update rain_end with next "rain block" from data set and reference timestamp
                            rain_end_ts = rain.iloc[row-1]['dt']
                            ref_timestamp = rain_start_ts

                        elif (rain.iloc[row]['dt'] - rain.iloc[row-1]['dt'] == 3600) and (row == 1):
                            rain_start_ts = rain.iloc[row-1]['dt']

                            # rain duration
                            rain_duration = ((rain_end_ts - rain_start_ts) / 3600) + 1

                            # rain intensity
                            rain_intensity = rain.query('dt >= @rain_start_ts and dt <= @rain_end_ts')['rain_mm'].sum()

                            # rain object
                            rain_data = rain_data.append(
                                {'dt_start': rain_end_ts, 'dt_end': rain.iloc[row]['dt'], 'weather_id': rain.iloc[row]['weather_id'], 'duration': rain_duration,
                                 'intnsty': rain_intensity }, ignore_index=True)

                            # update rain_end with next "rain block" from data set and reference timestamp
                            rain_end_ts = rain.iloc[row-1]['dt']
                            ref_timestamp = rain_start_ts
                if rain_len == 0:
                    rain_duration = 1
                    rain_intensity = rain.query('dt == @rain_end_ts')['rain_mm'].sum()
                    # rain object
                    rain_data = rain_data.append(
                        {'dt_start': rain_end_ts, 'dt_end': rain_end_ts,
                         'weather_id': rain.query('dt == @rain_end_ts')['weather_id'], 'duration': rain_duration,
                         'intnsty': rain_intensity}, ignore_index=True)

                # duration of last rain - MVP - only consider last rain and its duration
                if rain_data.empty == False:
                    lastrain_duration = float(rain_data.tail(1)['duration'])
                    lastrain_intensity = float(rain_data.tail(1)['intnsty'])

                    if lastrain_intensity > 0.1:
                        # test output
                        print('time since rain: ' + str(time_since_rain) + 'h; rain intensity: ' + str(lastrain_intensity) + ' mm; avrg temp since last rain: ' + str(temp_since_rain))

                        # # # # #
                        # equation / algo
                        # # # # #

                        # algo paramter for surface type
                        road_faktor = 1
                        gravel_faktor = 1.5
                        trail_faktor = 1.75
                        std_drytime = 48
                        temp_factor = 1

                        # the real deal:
                        # -
                        base_equation = std_drytime*(rain_intensity+0.5)
                        prob_road = -(1/(road_faktor*base_equation))*time_since_rain+1
                        # prob_road = -(1/(road_faktor*std_drytime)*(temp_factor/50))*time_since_rain+1
                        prob_gravel = -(1/(gravel_faktor*base_equation))*time_since_rain+1
                        prob_trail = -(1/(trail_faktor*base_equation))*time_since_rain+1

                    else:
                        prob_road = 0
                        prob_gravel = 0
                        prob_trail = 0

        elif ts_lastrain > max_dry_time:

            prob_road = 0
            prob_gravel = 0
            prob_trail = 0

        elif ts_lastrain == 0:

            # it's raining, let's get dirty or shred on an other day!
            prob_road = 2
            prob_gravel = 2
            prob_trail = 2


    else:
        prob_road = 0
        prob_gravel = 0
        prob_trail = 0

    return prob_road, prob_gravel, prob_trail
