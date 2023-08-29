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
    for i in range(10):
        if stationNum + i in boardNumberings.values():
            return stationNum + i
        
    return None