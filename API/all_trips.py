import requests
import datetime
import json
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


def getAllTrips():
   print("No schedule file found, making new one...")
   today = datetime.date.today()

   all_trips = getAllTripsOnLWLE(today.strftime('%Y%m%d'))

   with open(f"{today.strftime('%Y%m%d')} - Scheduled Trains", "w") as outfile:
      outfile.write(json.dumps(all_trips, indent=4))