import utils
import math
import numpy as np
import bisect


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
    return a ** (math.e ** (b / (tmi+y)) + s)


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


SIEVES_SIZES_IN_MM = {
    "2": 50.8,
    "1-1/2": 38.1,
    "1": 25.4,
    "3/4": 19.1,
    "1/2": 12.5,
    "3/8": 9.52,
    "No4": 4.75,
    "No10": 2,
    "No40": 0.45,
    "No200": 0.075,
}

PARTICLE_SIZE_PASSING_PERCENT = {
    "D90": 22.383,
    "D60": 6.225,
    "D30": 0.628,
    "D20": 0.219,
    "D10": 0.086,
}

sieves_passing = {
    "2": 100,
    "1-1/2": 98.3,
    "1": 92.8,
    "3/4": 85.1,
    "1/2": 77.1,
    "3/8": 69.9,
    "No4": 53.7,
    "No10": 38.6,
    "No40": 27.1,
    "No200": 8.50
}


def sorround_num_keys(keys, value):
    sorted_keys = sorted(keys)
    index = bisect.bisect_right(sorted_keys, value)
    key_before = sorted_keys[index-1]
    key_after = sorted_keys[index]

    return (key_before, key_after)


TMI_PLASTIC = {
    0: {'a': 3.649, 'b': 3.338, 'y': -0.05046},
    2: {'a': 4.196, 'b': 2.741, 'y': -0.03824},
    4: {'a': 5.285, 'b': 3.473, 'y': -0.04004},
    6: {'a': 6.877, 'b': 4.402, 'y': -0.03726},
    8: {'a': 8.621, 'b': 5.379, 'y': -0.03836},
    10: {'a': 12.180, 'b': 6.646, 'y': -0.04688},
    12: {'a': 15.590, 'b': 7.599, 'y': -0.04904},
    14: {'a': 20.202, 'b': 8.154, 'y': -0.05164},
    16: {'a': 23.564, 'b': 8.283, 'y': -0.05218}
}

specific_gravity = 2.611
plasticity_index = 7.12
california_bearing_ratio = 100
maximum_dry_density = 2024
optimum_moisture_content = 8.500
percentage_passing_n200 = sieves_passing['No200']

precipitation_mm = np.array(
    [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
        42.78, 34.74, 29.80, 67.30, 74.58, 24.86]
)
temp_celsius = np.array(
    [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
     12.44, 12.54, 13.07, 13.48, 13.93, 13.55]
)


sunshine_hours = np.array([11.70, 11.80, 12.00, 12.10, 12.31,
                           12.30, 12.30, 12.20, 12.00, 11.90, 11.69, 11.70])

monthy_days = np.array(utils.number_of_day_per_month(2023))
monthly_heat = monthly_heat_index(temp_celsius)
anual_heat = np.sum(monthly_heat)
anual_3rd_polynomial = third_degree_polynomial(anual_heat)
ept_unadjust = ept_without_correction(
    temp_celsius, anual_heat, anual_3rd_polynomial)
ept_adjusted = ept_correction(ept_unadjust, sunshine_hours, monthy_days)
ept_adjusted = np.append(ept_adjusted, np.sum(ept_adjusted))
precipitation_mm = np.append(precipitation_mm, np.sum(precipitation_mm))
tmi = thornthwaite_moisture_index(ept_adjusted, precipitation_mm)

p_middle = sieves_passing['No200']

(p_before, p_after) = sorround_num_keys(
    TMI_PLASTIC.keys(), p_middle)

a_before = TMI_PLASTIC[p_before]['a']
a_after = TMI_PLASTIC[p_after]['a']

a = lerp(int(p_before), a_before, int(p_after), a_after, p_middle)

b_before = TMI_PLASTIC[p_before]['b']
b_after = TMI_PLASTIC[p_after]['b']

b = lerp(int(p_before), b_before, int(p_after), b_after, p_middle)

y_before = TMI_PLASTIC[p_before]['y']
y_after = TMI_PLASTIC[p_after]['y']

y = lerp(int(p_before), y_before, int(p_after), y_after, p_middle)

hm = matric_suction_no_plastic(a, b, y, tmi)

# SWCC parameter
hr = 100
d90 = PARTICLE_SIZE_PASSING_PERCENT['D90']
d60 = PARTICLE_SIZE_PASSING_PERCENT['D60']
d20 = PARTICLE_SIZE_PASSING_PERCENT['D20']
d30 = PARTICLE_SIZE_PASSING_PERCENT['D30']
d10 = PARTICLE_SIZE_PASSING_PERCENT['D10']
p200 = sieves_passing['No200']
m1 = m_1(d90, d60)
d100 = d_100(m1, d60)
a2 = a_swcc(d20, p200, d30, d100)
af = af_swcc(a2, p200)


m2 = m_2(d30, d10)
d0 = d_0(m2, d30)
b = b_swcc(p200, d90, d10, d0, m1)
bf = bf_swcc(b)

c = c_swcc(m2, bf)
cf = cf_swcc(c, d10)

ch = adjust_factor(hm, hr)

osat = volumetry_humedity_saturated(maximum_dry_density, specific_gravity)
ow = volumetry_humedity(ch, osat, hm, af, bf, cf)

s = ow / osat

a3 = -0.3123
b3 = 0.3
km = 6.8157

tetha_opt = tetha_opt(optimum_moisture_content, maximum_dry_density)
sopt = tetha_opt / osat

famb = ambient_factor(a3, b3, km, s, sopt)
cbr = famb * california_bearing_ratio

print(cbr)


# assert (
#    len(SIEVES_SIZES_IN_MM) == len(sieves_passing)
# ), "Missing sieves passing elements."
