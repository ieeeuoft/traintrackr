import requests
import datetime
import serial
import time

from helpers import stopped_at_station_to_section, L_to_AC, in_transit_station_to_section

def getPositions():
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
              #"vehicle": trip["vehicle"]["vehicle"],
          })

  for trip in TripUpdates:
      trip_num = trip["id"].split("-")[2]
      for i in Combined_API_Response:
          if i["trip_num"] == trip_num:
              i["next_stop"] = trip["trip_update"]["stop_time_update"][0]

  send_to_serial = ""
  for trip in Combined_API_Response:
    if trip["next_stop"]["stop_id"] == "SCTH" or trip["next_stop"]["stop_id"] == "NI":
      continue
    elif trip["next_stop"]["stop_id"] == "WR" and trip["direction"] == "LWEB":
      continue
    elif trip["status"] == "STOPPED_AT":
      light_section = stopped_at_station_to_section(trip["next_stop"], trip["direction"])
      send_to_serial +=  L_to_AC(light_section)
    else:
      light_section = in_transit_station_to_section(trip["next_stop"], trip["direction"])
      send_to_serial +=  L_to_AC(light_section)
  return send_to_serial

print(getPositions())

# sending shit
def send_to_arduino(string_to_send):
  try:
    port = serial.Serial(port="COM4", baudrate=9600, timeout=1)
  except serial.SerialException:
    print('Cannot initialize serial communication.')
    print('Is the device plugged in? \r\nIs the correct COM port chosen?')

  time.sleep(2)
  # Send the string
  port.write(string_to_send.encode())  # Convert the string to bytes before sending

  time.sleep(2)

  response = port.readline().decode().strip()
  if response:
    print("String sent successfully.", response)
  else:
    print("String not sent or not acknowledged.")

  port.close()

try:
   while True:
    print("hi")
    positions = getPositions()
    send_to_arduino(positions)
    time.sleep(30)
except KeyboardInterrupt:
   print("byebye")
      
### matplotlib gui?
### use time stamp to compare
### output
### AXXCXAXXCXAXXCX ; 