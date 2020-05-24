import argparse
from math import radians, degrees, cos, sin, asin, sqrt, atan2

def GPSplusDistance(lat1,lng1,d,bearing):
    # -35 degrees is about the trajectory of I5 from San Diego going north
    # 160 degrees is about the trajectory of I5 from Washingto going south
    brng = radians(bearing)
    R = 3956
    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = asin(sin(lat1)*cos(d/R) + cos(lat1)*sin(d/R)*cos(brng))
    lng2 = lng1 + atan2(sin(brng)*sin(d/R)*cos(lat1),cos(d/R)-sin(lat1)*sin(lat2))
    lat2 = degrees(lat2)
    lng2 = degrees(lng2)
    return(lat2,lng2)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-t","--lat",required=True, help="latitude")
    ap.add_argument("-l","--lng",required=True, help="longitude")
    ap.add_argument("-v","--vehicleRange",required=True, help="vehicle range")
    ap.add_argument("-b","--bearing",required=True, help="bearing adjustment")
    args = vars(ap.parse_args())

    lat2, lng2 = GPSplusDistance(float(args["lat"]),float(args["lng"]),int(args["vehicleRange"]),int(args["bearing"]))
    print(round(lat2,6),round(lng2,6))
