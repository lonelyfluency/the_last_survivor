'''
将经纬度坐标转化成距离，结果的单位是米

'''
from math import sin, atan, cos, radians, tan, acos


def calcDistance(Lat_A, Lng_A, Lat_B, Lng_B):
    ra = 6378.140
    rb = 6356.755
    flatten = (ra - rb) / ra
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return distance*1000


def cor2dis(loc1, loc2):
    lat1 = float(loc1[1])
    lnt1 = float(loc1[0])
    lat2 = float(loc2[1])
    lnt2 = float(loc2[0])
    return calcDistance(lat1, lnt1, lat2, lnt2)

