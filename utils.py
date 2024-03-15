import math
import numpy as np


def is_leap_year(year: int):
    return year % 4 == 0 or year % 100 == 0 and year % 400 == 0


def number_of_day_per_month(year):
    return [
        31,
        29 if is_leap_year(year) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31
    ]


def lerp(x0, y0, x1, y1, x):
    return y0 + (x-x0)*(y1-y0)/(x1-x0)


def ambient_factor(a3, b3, km, s, sopt):
    return 10 ** (
        a3 + (b3 - a3) / (1 + np.exp(np.log(-b3 / a3) + km * (s - sopt)))
    )


def tetha_opt(wopt, pdmax):
    return ((wopt / 100) * pdmax)/1000


def c_swcc(m2, bf):
    return math.log10(m2**1.15) - (1 - (1 / bf))


def cf_swcc_thin(wpi):
    value = -0.2154 * math.log(wpi) + 0.7145
    return 0.03 if value < 0.01 else value


def bf_swcc_thin(wpi):
    return 1.421 * wpi**(-0.3185)


def af_swcc_thin(wpi):
    value = 32.835 * math.log(wpi) + 32.438
    return 5 if value < 5 else value


def cf_swcc(c, d10):
    return 0.26 * math.exp(0.758 * c) + 1.4 * d10


def bf_swcc(b):
    if 0.936 * b - 3.8 < 0.3:
        return 0.3
    elif 0.936 * b - 3.8 >= 4:
        return 4
    else:
        return 0.936 * b - 3.8


def af_swcc(a, p200):
    if (1.14 * a - 0.5) < 0:
        return 1
    elif (1.14 * a - 0.5) > 0 and (1.14 * a - 0.5) < 1:
        return 2.25 * p200**0.5 + 5
    else:
        return 1.14 * a - 0.5


def b_swcc(p200, d90, d10, d0, m1):
    return (5.39 - 0.29 * math.log(
        p200 * (d90 / d10)
    ) + 3 * d0**0.57 + 0.021 * p200**1.19) * m1**0.1


def a_swcc(d20, p200, d30, d100):
    return -2.79 - 14.1 * math.log10(d20) - 1.9 * 10**-6 *\
        p200**4.34 + 7 * math.log10(d30) + 0.055 * d100


def d_100(m1, d60):
    return 10 ** ((40/m1) + math.log10(d60))


def d_0(m2, d30):
    return 10 ** ((-30/m2) + math.log10(d30))


def m_1(d90, d60):
    return 30 / (math.log10(d90) - math.log10(d60))


def m_2(d30, d10):
    return 20 / (math.log10(d30) - math.log10(d10))


def volumetry_humedity_saturated(pdmax, gs):
    return 1 - pdmax / (1000*gs)


def volumetry_humedity(ch, osat, hm, af, bf, cf):
    return ch * (osat/(np.log(np.exp(1) + (hm/af) ** bf)**cf))


def monthly_heat_index(average_temperature_celsius):
    return (average_temperature_celsius/5) ** 1.514


def ept_without_correction(
    temp_celsius,
    anual_heat,
    anual_temp_3rd_poly
):
    return 16 * (10 * temp_celsius / anual_heat) ** anual_temp_3rd_poly


def ept_correction(ept_unadjust, sunshine_hours, monthly_days):
    return ept_unadjust * (sunshine_hours/12)*(monthly_days/30)


def thornthwaite_moisture_index(ept_adjusted, precipitation,):
    return 75 * (precipitation / ept_adjusted - 1) + 10


def matric_suction_plastic(a, b, y, s, tmi):
    return a * (np.exp(b / (tmi + y)) + s)


def matric_suction_no_plastic(a, b, y, tmi):
    return a + math.e ** (b+y*(tmi+101))


def third_degree_polynomial(anual_temp):
    a = (675 * 10**-9 * anual_temp ** 3)
    b = (771 * 10**-7 * anual_temp ** 2)
    c = (1792 * 10**-5 * anual_temp)
    d = 0.49239

    return a - b + c + d


def adjust_factor(hm, hr):
    return (1 - (np.log(1 + (hm / hr)) / (np.log(1 + (10 ** 6 / hr)))))
