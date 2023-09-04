import datetime
import requests
def getAllTripsOnOneLine(today_date, line, direction):
  alltrips = requests.get(f'http://api.openmetrolinx.com/OpenDataAPI/api/V1/Schedule/Line/{today_date}/{line}/{direction}?key=30023457')
  return alltrips.json()["Lines"]["Line"][0]["Trip"]

def getAllTripsOnLWLE(today_date):
   return {
      "LWWB": getAllTripsOnOneLine(today_date, "LW", "W"),
      "LWEB": getAllTripsOnOneLine(today_date, "LW", "E"),
      "LEWB": getAllTripsOnOneLine(today_date, "LE", "W"),
      "LEEB": getAllTripsOnOneLine(today_date, "LE", "E")
   }

print(getAllTripsOnLWLE("20230904"))
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