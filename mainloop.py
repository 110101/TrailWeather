import M_owm_api as owm_api
import P_conditionalgo as algo
import pandas

# dem lat long city
# lat = str(48.12152)
# lon = str(11.54549)

# demo lat long isar trails
lat = str(48.07)
lon = str(11.54)

# get UNIX timestamp
timestamp = owm_api.time_now_UNIX()
print(timestamp)

# get hist data
owm_hist_dataset_return = owm_api.owm_hist_data(timestamp, lat, lon)

# test data to csv
# owm_hist_dataset_return.to_csv("ref_test_data_city_but_200622.csv")

# read in test data
# owm_hist_dataset_return = pandas.read_csv("ref_data/synth_test_one_rain.csv", usecols=['dt','temp','humidity','dew_point','wind','weather_id','rain_mm'])

# get forecast
# owm_forecast_dataset_return = owm_api.owm_forecast_data(timestamp, lat, lon)

# algo
condition_prob = algo.run(owm_hist_dataset_return)

if condition_prob[0] and condition_prob[1] and condition_prob[2] == 2:
 print("it's raining")
else:
 road = condition_prob[0]
 gravel = condition_prob[1]
 trail = condition_prob[2]

 print('road: ' + str(road) + ' / gravel: ' + str(gravel) + ' / trail: ' + str(trail))
