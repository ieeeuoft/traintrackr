import requests
import datetime
from helpers import time_to_L
r = requests.get('http://api.openmetrolinx.com/OpenDataAPI/api/V1/Gtfs/Feed/TripUpdates?key=30023457')
v = r.json()["entity"]
c = []
# print(v[0]["trip_update"]["vehicle"])
# for i in v:
#     if i["trip_update"]["vehicle"]["label"][0:2] == "LW": 
#       stops = i["trip_update"]["stop_time_update"]
#       c.append(stops)
#       print(i, end="\n\n")
for i in v:
    if i["trip_update"]["vehicle"]["label"][0:2] == "LW": 
      first_stop = i["trip_update"]["stop_time_update"][0]
      print(i)
      time_to_L("LWWB", first_stop)
      break

# for d in c:
#   for stop in d:
#     arrival_time = stop["departure"]["time"]
#     arrival_time = datetime.datetime.fromtimestamp(arrival_time)
#     stop["departure"]["time"] = arrival_time
#     print(stop["stop_id"], arrival_time)
#   print("\n\n")

### matplotlib gui?
### use time stamp to compare
### output
### AXXCXAXXCXAXXCX ;