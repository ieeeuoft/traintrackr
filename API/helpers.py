from timings import exportBoardNumberings, exportTrainTimings
import datetime

def L_to_AC(L):
    C = (L - 1) // 16 
    A = (L - 1) % 16
    if A < 10:
        A = "0" + str(A)
    
    return "A" + str(A) + "C" + str(C)

def time_to_L(direction, station, timing=0):
    trainTimings = exportTrainTimings[direction]
    boardNumberings = exportBoardNumberings[direction]
    
def time_to_next_stop(station):
    now = datetime.datetime.timestamp(datetime.datetime.now())
    # The entire object obtained from the first item of "'trip_update' of 'stop_time_update'" 
    # From the trip updates API return

    next_stop = station["departure"]["time"]
    diff = (next_stop - now) / 60
    return diff
    # next_stop = datetime.datetime.fromtimestamp(station["departure"]["time"] + station["departure"]["delay"])

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

def station_to_section(station, direction):
    # first determine the percentage of the way from the previous station to the next station
    station_id = station["stop_id"]
    est_time_to_station = time_to_next_stop(station)
    print("est_time_to_station", est_time_to_station)
    full_time_to_station = exportTrainTimings[direction][station_id]
    print("full_time_to_station", full_time_to_station)
    value = min(max(0 , est_time_to_station/full_time_to_station), 1)

    # now determine the board number
    prev_station_boardNum = find_prev_station_boardNum(station_id, direction)
    current_station_boardNum = exportBoardNumberings[direction][station_id]
    print(current_station_boardNum, prev_station_boardNum)
    num_lights = prev_station_boardNum - current_station_boardNum - 1
    print("num_lights", num_lights)
    relative_section = value_to_section(value, num_lights)
    print("relative_section", relative_section)

    return current_station_boardNum + relative_section

sample_station = {'stop_id': 'CL', 'arrival': None, 'departure': {'delay': 106, 'time': 1693349686, 'uncertainty': 0}, 'schedule_relationship': 'SCHEDULED'}
print(station_to_section(sample_station, "LWWB"))