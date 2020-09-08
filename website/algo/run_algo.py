# from algo
from algo import M_owm_api as owm_api, process_algo as process
import pandas

def test(lat, lng):
    rain_status = 1
    time_since_rain_days = 4
    time_since_rain_hours = 22
    lastrain_duration = 1
    lastrain_intensity =  0.5
    rain_commulated_l5days = 5.0
    cors_road = "dry"
    cors_gravel = "mostly dry"
    cors_trail = "wet"

    return {'rain_status': rain_status, 'time_since_rain_days': str(time_since_rain_days),'time_since_rain_hours': str(time_since_rain_hours), 'lastrain_duration_h': str(lastrain_duration), 'lastrain_intensity_mm': str(lastrain_intensity), 'rain_commulated_l5days_mm': str(rain_commulated_l5days), 'cors_road': str(cors_road), 'cors_gravel': str(cors_gravel), 'cors_trail': str(cors_trail), 'lat': str(lat), 'lng': str(lng)}

def calc_prob (condition_prob):
    # cluster slgo return
    iteration = 0
    for prob in condition_prob:
        # setting ids for output / selecting image
        # 0: dry
        # 1: nearly dry, only some last puddle of mud in uneven areas
        # 2: some puddle of muds in not sun covered areas
        # 3: muddy
        # 4: wet
        # 5: it's raining
        print(prob)

        if prob < 0.20:
            prob_clustered = 0
        elif 0.20 < prob < 0.40:
            prob_clustered = 1
        elif 0.40 < prob < 0.60:
            prob_clustered = 2
        elif 0.60 < prob < 0.80:
            prob_clustered = 3
        elif 0.80 < prob < 1:
            prob_clustered = 4
        elif prob == 1 or prob == 100:
            prob_clustered = 5

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

    return road, gravel, trail

def get_weather_data(lat, lon):
    # dem lat long city
    # lat = str(48.12152)
    # lon = str(11.54549)

    # demo lat long isar trails
    # lat = str(48.07)
    # lon = str(11.54)

    # get UNIX timestamp
    timestamp = owm_api.time_now_UNIX()

    # get hist data
    owm_hist_dataset_return = owm_api.owm_hist_data(timestamp, lat, lon)

    # read in test data
    # owm_hist_dataset_return = pandas.read_csv("ref_data/synth_test_one_rain.csv",
    #                                          usecols=['dt', 'temp', 'humidity', 'dew_point', 'wind', 'weather_id',
    #                                                   'rain_mm'])

    # algo
    condition_feedback = process.run(owm_hist_dataset_return, lat, lon)

    return condition_feedback

    # print('road: ' + str(road) + ' / gravel: ' + str(gravel) + ' / trail: ' + str(trail))
    # print('road: ' + str(prob_road_clustered) + ' / gravel: ' + str(prob_gravel_clustered) + ' / trail: ' + str(prob_trail_clustered))

# just for testing
lat = str(48.07)
lon = str(11.54)

feedb = get_weather_data(lat, lon)
# print(feedb)
