import M_owm_api as owm_api
import pandas

# demo lat long
lat = str(48.07)
lon = str(11.54)

# get UNIX timestamp
timestamp = owm_api.time_now_UNIX()

# will be called from main loop later on
# get hist data
owm_hist_dataset_return = owm_api.owm_hist_data(timestamp, lat, lon)

# get forecast
owm_forecast_dataset_return = owm_api.owm_forecast_data(timestamp, lat, lon)

# merge owm returns for algo
owm_dataset_return = pandas.DataFrame([])
owm_dataset_return = owm_hist_dataset_return.append(owm_forecast_dataset_return, ignore_index=True)

# algo
condition_prob = condition_algo.run(owm_dataset_return)

print("fin")
