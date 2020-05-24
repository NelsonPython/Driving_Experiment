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
    print("great circle")
