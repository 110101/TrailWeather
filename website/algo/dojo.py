import csv
from datetime import datetime

def writelogfile(lat, lon, surface, condition):

    # get current date and time
    timestamp = datetime.now()
    # create file name

    # write csv
    f = open('algo/dojo_data/testfile' + str(timestamp) + '.csv', 'w')
    writer = csv.writer(f)
    row = str(lat) + ";" + str(lon) + ";"
    writer.writerow(row)

    return
