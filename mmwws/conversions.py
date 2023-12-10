#
# Copyright Mark McIntyre, 2023-
#

import math

KMHTOMPH = 0.6214
HPATOINHG = 0.02953
MMTOIN = 1/25.4

PRESSCORR = 10.0


def dewPoint(t, rh): 
    # t in C, rh as a number eg 90, 50
    E0 = 0.611 # kPa
    lrv = 5423 # K (L/Rv over flat surface of water)
    T0 = 273.15 # K
    Es = E0 * math.exp(lrv * (1/T0 - 1/(t + T0)))
    dewPoint = 1.0 / (-math.log(rh/100 * Es/E0)/lrv + 1/T0)-T0
    return round(dewPoint, 4)


def CtoF(tempc):
    return tempc * 1.8 +32


def windChill(t, v):
    # after https://www.calculator.net/wind-chill-calculator.html
    # note not defined for T > 10C or v < 4.8 km/h
    if t > 10.1 or v < 4.8:
        return t
    wc = 13.12 + 0.6215 * t -11.37 * pow(v, 0.16) + 0.3965 * t * pow(v, 0.16)
    return round(wc, 4)


def heatIndex(t, rh):
    # after https://www.weather.gov/media/epz/wxcalc/heatIndex.pdf
    # and https://en.wikipedia.org/wiki/Heat_index for the formula in centigrade

    # Note the formula is only useful for T > 27C and H > 40%
    if t < 27.1 or rh < 40.1:
        return t
    c_1 = -8.78469475556
    c_2 = 1.61139411
    c_3 = 2.33854883889
    c_4 = -0.14611605
    c_5 = -0.012308094
    c_6 = -0.016425
    c_7 = 2.211732e-3
    c_8 = 7.2546e-4
    c_9 = -3.582e-6
    HI =c_1 + c_2 * t + c_3 * rh + c_4 * t*rh +c_5 * t*t + \
        c_6 * rh*rh + c_7 * t*t*rh + c_8 *t *rh*rh +c_9*t*t * rh*rh
    return round(HI, 4)
