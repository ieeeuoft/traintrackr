from timings import exportBoardNumberings, exportTrainTimings
import json
import datetime
from all_trips import getAllTrips

def L_to_AC(L):
    if not L:
        return ""
    C = (L - 1) // 16 
    A = (L - 1) % 16
    if A < 10:
        A = "0" + str(A)
    
    return "A" + str(A) + "C" + str(C)
    
def time_to_next_stop(station):
    now = datetime.datetime.timestamp(datetime.datetime.now())
    # The entire object obtained from the first item of "'trip_update' of 'stop_time_update'" 
    # From the trip updates API return

    next_stop = station["departure"]["time"]
    
    diff = (next_stop - now) / 60
    return diff

def value_to_section(value, num_sections):
    adjusted_value = value * num_sections
    for i in range(num_sections):
        if adjusted_value < i:
            return i
    return num_sections

def find_prev_station_boardNum(station, direction):
    # enter station in the form of "HC" or "WR"
    boardNumberings = exportBoardNumberings[direction]
    stationNum = boardNumberings[station]
    for i in range(1,10):
        if stationNum + i in boardNumberings.values():
            return stationNum + i
    return None

def stopped_at_station_to_section(station, direction): 
    station_id = station["stop_id"]
    if station_id == "SCTH":
        return ""
    return exportBoardNumberings[direction][station_id]

def get_all_scheduled_trips_today():
    all_trips = None
    while not all_trips:
        try:
            with open(f"{datetime.date.today().strftime('%Y%m%d')} - Scheduled Trains",'r') as openfile:
                all_trips = json.load(openfile)
                return all_trips
        except:
            getAllTrips()

def scheduled_full_time_between_stations(next_station_id, trip_id, direction):
    all_trips = get_all_scheduled_trips_today()
    all_trips_in_direction = all_trips[direction]
    relevant_trip = None
    for trip in all_trips_in_direction:
        if (trip_id == trip['Number']):
            relevant_trip = trip
            break
    if not relevant_trip:
        print("Unscheduled Trip")
        return None
    for i in range(len(relevant_trip['Stops'])):
        next_stop = relevant_trip['Stops'][i]
        if (next_stop['Code']) == next_station_id:
            previous_stop = relevant_trip['Stops'][i-1]
            break
    next_stop_time = next_stop['Time']
    prev_stop_time = previous_stop['Time']
    next_stop_time = datetime.datetime.strptime(next_stop_time,'%Y-%m-%d %H:%M:%S')
    prev_stop_time = datetime.datetime.strptime(prev_stop_time,'%Y-%m-%d %H:%M:%S')
    minutes_diff = (next_stop_time - prev_stop_time).total_seconds() / 60
    prev_station_id = previous_stop['Code']

    return {
        "prev_station_id": prev_station_id,
        "full_time": minutes_diff
    }
    

def in_transit_station_to_section(station, direction, trip_id):
    # first determine the percentage of the way from the previous station to the next station
    station_id = station["stop_id"]
    est_time_to_station = time_to_next_stop(station)
    # print("est_time_to_station", est_time_to_station)
    real_previous_station = scheduled_full_time_between_stations(station['stop_id'], trip_id, direction)
    
    if real_previous_station:
        full_time_to_station = real_previous_station['full_time']
        previous_station_id = real_previous_station['prev_station_id']
        if previous_station_id == "SCTH":
            return None
        prev_station_boardNum = exportBoardNumberings[direction][previous_station_id]
    else: # edge case: the trip isn't on the schedule
        full_time_to_station = exportTrainTimings[direction][station_id]
        prev_station_boardNum = find_prev_station_boardNum(station_id, direction)
    # print("full_time_to_station", full_time_to_station)
    value = min(max(0 , est_time_to_station/full_time_to_station), 1)

    # now determine the board number
    current_station_boardNum = exportBoardNumberings[direction][station_id]
    # print(current_station_boardNum, prev_station_boardNum)
    
    num_lights = prev_station_boardNum - current_station_boardNum - 1
    # print("num_lights", num_lights)
    
    relative_section = value_to_section(value, num_lights)
    # print("relative_section", relative_section)
    if station_id == "AL" and previous_station_id == "HA": # Edge case: LW train going eastbound to Aldershot
        return 124 + value_to_section(value, 3)
    if station_id == "HA": # Edge case: LW train going westbound to Hamilton Center
        return 1 + value_to_section(value, 3)
    return current_station_boardNum + relative_section

# sample_station = {'stop_id': 'CL', 'arrival': None, 'departure': {'delay': 106, 'time': 1693349686, 'uncertainty': 0}, 'schedule_relationship': 'SCHEDULED'}
# print(in_transit_station_to_section(sample_station, "LWWB"))