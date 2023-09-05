import datetime
import requests
r = requests.get('http://api.openmetrolinx.com/OpenDataAPI/api/V1/Gtfs/Feed/VehiclePosition?key=30023457')
# r = requests.get('http://api.openmetrolinx.com/OpenDataAPI/api/V1/Schedule/Line/20230904/LW/E?key=30023457')
alltrips = r.json()["entity"]#["Lines"]["Line"][0]["Trip"]


def main():
  for trips in alltrips:
    if trips['Number'] == '1970':
      print(trips)
      first_time = trips['Stops'][0]['Time']
      second_time = trips['Stops'][1]['Time']
      first_time_object = datetime.datetime.strptime(first_time,'%Y-%m-%d %H:%M:%S')
      second_time_object = datetime.datetime.strptime(second_time,'%Y-%m-%d %H:%M:%S')
      print((second_time_object - first_time_object).total_seconds() / 60)
      break

def main2():
  print("number of trips today:", len(alltrips))
  for trips in alltrips:
    print(trips, end="\n\n")

for trip in alltrips:
  print(trip)
# v = r.json()["entity"]
# c = []
# for i in v:
#     if i["vehicle"]["vehicle"]["label"][0:2] == "LW":
#       c.append(i)
#       print(i, end="\n\n")

# for d in c:
#    time = d["vehicle"]["timestamp"]
#    time = datetime.datetime.fromtimestamp(time)
#    d["vehicle"]["timestamp"] = str(time)
#    print(d, end="\n\n")