import requests
import serial
import time
import datetime

from helpers import stopped_at_station_to_section, L_to_AC, in_transit_station_to_section

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

def fillDictionary():
  VehiclePosition = requests.get('http://api.openmetrolinx.com/OpenDataAPI/api/V1/Gtfs/Feed/VehiclePosition?key=30023457')
  TripUpdates = requests.get('http://api.openmetrolinx.com/OpenDataAPI/api/V1/Gtfs/Feed/TripUpdates?key=30023457')
  VehiclePosition = VehiclePosition.json()["entity"]
  TripUpdates = TripUpdates.json()["entity"]

  Combined_API_Response = []

  for trip in VehiclePosition:
      id = trip["id"].split("-")
      # east = 0
      # west = 1
      if id[1] == "LW" or id[1] == "LE":
          direction_code = trip["vehicle"]["trip"]["direction_id"]
          if direction_code == 0:
            direction_code = id[1] + "EB"
          else:
            direction_code = id[1] + "WB"

          Combined_API_Response.append({
              "trip_num": id[2],
              "status": trip["vehicle"]["current_status"],
              "direction": direction_code,
              "label": trip["vehicle"]["vehicle"]["label"],
          })

  for trip in TripUpdates:
      trip_num = trip["id"].split("-")[2]
      for i in Combined_API_Response:
          if i["trip_num"] == trip_num:
              i["next_stop"] = trip["trip_update"]["stop_time_update"][0]

  return Combined_API_Response

def getPositions(Combined_API_Response):
  send_to_serial = ""
  num_of_trains = 0
  for trip in Combined_API_Response:
    if trip.get("next_stop") and trip["next_stop"]["stop_id"] in ["SCTH", "NI"]: # edge case: trains on the niagara portion of LW
       continue    
    elif trip["status"] == "STOPPED_AT": #trains that are stopped at a station
      light_section = stopped_at_station_to_section(trip["next_stop"], trip["direction"])
      send_to_serial +=  L_to_AC(light_section)
      num_of_trains += 1
    elif not trip.get("next_stop"): #deadheading trains
       continue
    elif trip["next_stop"]["stop_id"] == "WR" and trip["direction"] == "LWEB": #trains coming towards west harbor on the niagara portion
      continue
    else: #all other trains
      light_section = in_transit_station_to_section(trip["next_stop"], trip["direction"], trip["trip_num"])
      send_to_serial +=  L_to_AC(light_section)
      num_of_trains += 1
  return send_to_serial, num_of_trains

def setupCOM():
  port = serial.Serial(port="COM3", baudrate=9600, timeout=1)
  return port

def send_to_arduino(string_to_send, port):
  time.sleep(2)
  # Send the string
  port.write(string_to_send.encode())  # Convert the string to bytes before sending
  time.sleep(2)
  response = port.readline().decode().strip()
  if response:
    print("String sent successfully.", response)
  else:
    print("String not sent or not acknowledged.")
def main(to_arduino=True):
  try:
    if to_arduino:
      port = setupCOM()
    while True:
      print("Fetching from server...")
      start_time = datetime.datetime.now()
      API_Dictionary = fillDictionary()
      positions, num_trains = getPositions(API_Dictionary)
      print(f"{num_trains} trains total, {positions}")
      if to_arduino:
        send_to_arduino(positions, port)
      time_diff = datetime.datetime.now() - start_time
      print(f"Fetched in {time_diff.total_seconds()} seconds. ", end="")
      print("Time Now: " + datetime.datetime.now().strftime('%H:%M:%S'), end="\n\n")
      time.sleep(10)
  except KeyboardInterrupt:
    print("byebye")
    if to_arduino:
      port.close()
  except Exception as e:
     print(f"Error occured! {e}")

main(to_arduino=False) # set this to false when testing
