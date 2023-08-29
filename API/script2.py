import datetime
import requests
r = requests.get('http://api.openmetrolinx.com/OpenDataAPI/api/V1/Gtfs/Feed/VehiclePosition?key=30023457')
v = r.json()["entity"]
c = []
for i in v:
    if i["vehicle"]["vehicle"]["label"][0:2] == "LW":
      c.append(i)
      print(i, end="\n\n")

# for d in c:
#    time = d["vehicle"]["timestamp"]
#    time = datetime.datetime.fromtimestamp(time)
#    d["vehicle"]["timestamp"] = str(time)
#    print(d, end="\n\n")