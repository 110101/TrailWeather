import requests
import certifi
import M_apikey
import pandas
from datetime import timezone, datetime


def owm_hist_data(time, lat, lon):
    ts_owm_api_start = datetime.now()

    # assemble api url
    api_key= "54f724090313801f7966324601cccdfc"
    api_base = "https://api.openweathermap.org/data/2.5/onecall/"

    # api time limitations
    # 5 days back only
    days = 6
    loop = [5, 4, 3, 2, 1, 0.25]
    owm_dataset_processed = []

    for d in range(len(loop)):

        offset = round(loop[d] * (24 * 3600),0)
        datetime_apilimit = int(time - offset)

        print(datetime_apilimit, datetime.utcfromtimestamp(datetime_apilimit))

        api = api_base + "timemachine?lat=" + lat + "&lon=" + lon + "&dt=" + str(datetime_apilimit) + "&appid=" + api_key

        print(api)
        # access api
        owm_feedback_json = requests.get(api).json()
        owm_dataset_raw = owm_feedback_json["hourly"]

        # process owm data
        for x in range(len(owm_dataset_raw)):
            temp_celsius = round((int(owm_dataset_raw[x]["temp"]) - 273.15),2)
            dewpoint = round(int(owm_dataset_raw[x]["dew_point"]) - 273.15,2)
            wind = owm_dataset_raw[x]["wind_speed"]
            weather_id = owm_dataset_raw[x]["weather"]
            weather_id = weather_id[0]["id"]
            string = {"dt": int(owm_dataset_raw[x]["dt"]),"temp": temp_celsius, "humidity": owm_dataset_raw[x]["humidity"], "dew_point": dewpoint, "wind": wind, "weather_id": weather_id}
            owm_dataset_processed.append(string)


    # for  in owm_feedback_json["hourly"]
    owm_df_proccesed = pandas.DataFrame(owm_dataset_processed)
    ts_owm_api_end = datetime.now()
    return (owm_df_proccesed)


def owm_forecast_data(time, lat, lon):
    ts_owm_api_start = datetime.now()
    owm_dataset_processed = []

    offset = round((5 * 3600), 0)
    datetime_apilimit = int(time - offset)

    print(datetime_apilimit, datetime.utcfromtimestamp(datetime_apilimit))

    # assemble api url
    api_key = M_apikey.getkey()
    api_base = "https://api.openweathermap.org/data/2.5/"

    api = api_base + "onecall?lat=" + lat + "&lon=" + lon + "&appid=" + api_key

    # access api
    owm_feedback_json = requests.get(api).json()
    owm_dataset_raw = owm_feedback_json["hourly"]

    print(owm_dataset_raw)

    # process owm data
    for x in range(len(owm_dataset_raw)):
        temp_celsius = round((int(owm_dataset_raw[x]["temp"]) - 273.15),2)
        dewpoint = round(int(owm_dataset_raw[x]["dew_point"]) - 273.15,2)
        wind = owm_dataset_raw[x]["wind_speed"]
        weather_id = owm_dataset_raw[x]["weather"]
        weather_id = weather_id[0]["id"]
        string = {"dt": int(owm_dataset_raw[x]["dt"]),"temp": temp_celsius, "humidity": owm_dataset_raw[x]["humidity"], "dew_point": dewpoint, "wind": wind, "weather_id": weather_id}
        owm_dataset_processed.append(string)

    # for  in owm_feedback_json["hourly"]
    owm_df_proccesed = pandas.DataFrame(owm_dataset_processed)
    ts_owm_api_end = datetime.now()
    return (owm_df_proccesed)


def time_now_UNIX():
    now_UNIX_time = int(datetime.now(tz=None).timestamp())
    print(now_UNIX_time, datetime.utcfromtimestamp(now_UNIX_time))

    return (now_UNIX_time)

