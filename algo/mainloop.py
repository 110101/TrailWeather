from algo import M_owm_api as owm_api, P_conditionalgo as algo
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
# owm_hist_dataset_return = owm_api.owm_hist_data(timestamp, lat, lon)

# test data to csv
# owm_hist_dataset_return.to_csv("ref_test_data_city_but_200622.csv")

# read in test data
owm_hist_dataset_return = pandas.read_csv("ref_data/synth_test_one_rain.csv",
                                          usecols=['dt', 'temp', 'humidity', 'dew_point', 'wind', 'weather_id',
                                                   'rain_mm'])

# get forecast
# owm_forecast_dataset_return = owm_api.owm_forecast_data(timestamp, lat, lon)

# algo
condition_prob = algo.run(owm_hist_dataset_return)
iteration = 0
for prob in condition_prob:
    # setting ids for output / selecting image
    # 0: dry
    # 20: nearly dry, only some puddle of mud
    # 40: some puddle of muds in not sun covered areas
    # 60: puddle of muds
    # 80: wet
    # 100: it's raining
    print (prob)

    if prob < 0.20:
        prob_clustered = 0
    elif 0.20 < prob < 0.40:
        prob_clustered = 20
    elif 0.40 < prob < 0.60:
        prob_clustered = 40
    elif 0.60 < prob < 0.80:
        prob_clustered = 60
    elif 0.80 < prob < 1:
        prob_clustered = 80
    elif prob == 1 or prob == 100:
        prob_clustered = 100

    if iteration == 0:
        prob_road_clustered = prob_clustered
    elif iteration == 1:
        prob_gravel_clustered = prob_clustered
    elif iteration == 2:
        prob_trail_clustered = prob_clustered

    iteration = iteration + 1

road = condition_prob[0]
gravel = condition_prob[1]
trail = condition_prob[2]

print('road: ' + str(road) + ' / gravel: ' + str(gravel) + ' / trail: ' + str(trail))
print('road: ' + str(prob_road_clustered) + ' / gravel: ' + str(prob_gravel_clustered) + ' / trail: ' + str(prob_trail_clustered))
