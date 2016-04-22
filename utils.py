import time
import math

def floatToInt(fnum):
    return int(math.floor(fnum))

# Returns the current time in milliseconds
# Source: http://stackoverflow.com/a/5998359
def getCurrentTime():
    return int(round(time.time() * 1000))
