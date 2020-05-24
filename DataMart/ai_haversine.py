import argparse
from math import radians, degrees, cos, sin, asin, sqrt, atan2

def Haversine(lat1, lng1, lat2, lng2):
        """ Haversine formula for computing the great circle distance between two points
            3956 is radius of earth in miles.  use 6371 for kilometers
        """
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        dLat = lat2 - lat1
        dLng = lng2 - lng1
        a = sin(dLat/2)**2 + cos(lat1) * cos(lat2) * sin(dLng/2)**2
        c = 2 * asin(sqrt(a))
        r = 3956
        varDistance = c*r
        return varDistance

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-ot","--originLat",required=True, help="latitude")
    ap.add_argument("-ol","--originLng",required=True, help="longitude")
    ap.add_argument("-dt","--destLat",required=True, help="latitude")
    ap.add_argument("-dl","--destLng",required=True, help="longitude")
    args = vars(ap.parse_args())

    tripDistance = int(Haversine(float(args["originLat"]),float(args["originLng"]),float(args["destLat"]),float(args["destLng"])))
    print(tripDistance)
    # bearing adjustment
    if float(args["originLat"]) - float(args["destLat"]) > 0:
        print(160)
    else:
        print(-35)
