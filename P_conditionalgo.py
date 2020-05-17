import pandas

def run(dataset):

    # time since last rain
    t_last_rain = dataset.loc[(dataset['weather_id'] >= 200) & (dataset['weather_id'] < 700)]

    # duration of last rain

    # intensity of last rain

    # temp, wind, sky since last rain
    temp = dataset[['dt', 'temp']]

    # time till rain before last rain

    # intensity of rain before last rain

    print(temp)

    return (prob_road, prob_gravel, prob_trail)
