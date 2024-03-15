import utils
import numpy as np
import bisect

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

TMI_NO_PLASTIC = {
    0: {"a": 0.3, "b": 419.07, "y": 133.5, "s": 15},
    1: {"a": 0.3, "b": 521.5, "y": 137.3, "s": 16},
    2: {"a": 0.3, "b": 521.5, "y": 137.3, "s": 16},
    3: {"a": 0.3, "b": 663.5, "y": 142.5, "s": 17.5},
    4: {"a": 0.3, "b": 801, "y": 147.6, "s": 25},
    5: {"a": 0.3, "b": 975, "y": 152.5, "s": 32},
    6: {"a": 0.3, "b": 1171.2, "y": 157.5, "s": 27.8}
}


mode = 'thin'  # or thick

# Thick
specific_gravity = 2.611  # gs
plasticity_index = 7.12  # ip
california_bearing_ratio = 100  # cbr
maximum_dry_density = 2024  # pdmax
optimum_moisture_content = 8.500  # wopt

# Thin
specific_gravity = 2.736  # gs
plasticity_index = 19  # ip
california_bearing_ratio = 30  # cbr
maximum_dry_density = 1240  # pdmax
optimum_moisture_content = 38  # wopt
thin_n200 = 58

if mode == 'thin':
    p200 = thin_n200
    wpi = (p200 / 100) * plasticity_index
else:
    p200 = sieves_passing['No200']


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
monthly_heat = utils.monthly_heat_index(temp_celsius)


anual_heat = np.sum(monthly_heat)
anual_3rd_polynomial = utils.third_degree_polynomial(anual_heat)
ept_unadjust = utils.ept_without_correction(
    temp_celsius, anual_heat, anual_3rd_polynomial)
ept_adjusted = utils.ept_correction(ept_unadjust, sunshine_hours, monthy_days)
ept_adjusted = np.append(ept_adjusted, np.sum(ept_adjusted))
precipitation_mm = np.append(precipitation_mm, np.sum(precipitation_mm))
tmi = utils.thornthwaite_moisture_index(ept_adjusted, precipitation_mm)


if mode == 'thin':
    a = 0.3
    if p200 == 10 and wpi == 0:
        b = TMI_NO_PLASTIC[0]['b']
        y = TMI_NO_PLASTIC[0]['y']
        s = TMI_NO_PLASTIC[0]['s']

    if p200 == 50 and wpi == 0:
        b = TMI_NO_PLASTIC[1]['b']
        y = TMI_NO_PLASTIC[1]['y']
        s = TMI_NO_PLASTIC[1]['s']

    if wpi <= 0.5:
        b = TMI_NO_PLASTIC[2]['b']
        y = TMI_NO_PLASTIC[2]['y']
        s = TMI_NO_PLASTIC[2]['s']

    if wpi >= 50:
        b = TMI_NO_PLASTIC[6]['b']
        y = TMI_NO_PLASTIC[6]['y']
        s = TMI_NO_PLASTIC[6]['s']

    if wpi > 0.5 and wpi < 50:
        tmi_table = [5, 10, 20]

        p_middle = wpi
        (p_before, p_after) = sorround_num_keys(
            tmi_table, p_middle)

        p_before_i = tmi_table.index(p_before) + 3
        p_after_i = tmi_table.index(p_after) + 3

        s_before = TMI_NO_PLASTIC[p_before_i]['s']
        s_after = TMI_NO_PLASTIC[p_after_i]['s']

        s = utils.lerp(int(p_before), s_before,
                       int(p_after), s_after, p_middle)

        b_before = TMI_NO_PLASTIC[p_before_i]['b']
        b_after = TMI_NO_PLASTIC[p_after_i]['b']

        b = utils.lerp(int(p_before), b_before,
                       int(p_after), b_after, p_middle)

        y_before = TMI_NO_PLASTIC[p_before_i]['y']
        y_after = TMI_NO_PLASTIC[p_after_i]['y']

        y = utils.lerp(int(p_before), y_before,
                       int(p_after), y_after, p_middle)
else:
    p_middle = p200
    (p_before, p_after) = sorround_num_keys(
        TMI_PLASTIC.keys(), p_middle)

    a_before = TMI_PLASTIC[p_before]['a']
    a_after = TMI_PLASTIC[p_after]['a']

    a = utils.lerp(int(p_before), a_before, int(p_after), a_after, p_middle)

    b_before = TMI_PLASTIC[p_before]['b']
    b_after = TMI_PLASTIC[p_after]['b']

    b = utils.lerp(int(p_before), b_before, int(p_after), b_after, p_middle)

    y_before = TMI_PLASTIC[p_before]['y']
    y_after = TMI_PLASTIC[p_after]['y']

    y = utils.lerp(int(p_before), y_before, int(p_after), y_after, p_middle)

print(a, b, y, s, tmi)

if mode == 'thin':
    hm = utils.matric_suction_plastic(a, b, y, s, tmi)
else:
    hm = utils.matric_suction_no_plastic(a, b, y, tmi)

# SWCC parameter

if mode == 'thin':
    hr = 500
else:
    hr = 100

ch = utils.adjust_factor(hm, hr)

if mode == 'thin':
    af = utils.af_swcc_thin(wpi)
    bf = utils.bf_swcc_thin(wpi)
    cf = utils.cf_swcc_thin(wpi)
else:
    d90 = PARTICLE_SIZE_PASSING_PERCENT['D90']
    d60 = PARTICLE_SIZE_PASSING_PERCENT['D60']
    d20 = PARTICLE_SIZE_PASSING_PERCENT['D20']
    d30 = PARTICLE_SIZE_PASSING_PERCENT['D30']
    d10 = PARTICLE_SIZE_PASSING_PERCENT['D10']
    p200 = sieves_passing['No200']
    m1 = utils.m_1(d90, d60)
    d100 = utils.d_100(m1, d60)
    a2 = utils.a_swcc(d20, p200, d30, d100)
    af = utils.af_swcc(a2, p200)

    m2 = utils.m_2(d30, d10)
    d0 = utils.d_0(m2, d30)
    b = utils.b_swcc(p200, d90, d10, d0, m1)
    bf = utils.bf_swcc(b)

    c = utils.c_swcc(m2, bf)
    cf = utils.cf_swcc(c, d10)


osat = utils.volumetry_humedity_saturated(
    maximum_dry_density, specific_gravity)

ow = utils.volumetry_humedity(ch, osat, hm, af, bf, cf)

s = ow / osat

if mode == 'thin':
    a3 = -0.5934
    b3 = 0.4
    km = 6.1324
else:
    a3 = -0.3123
    b3 = 0.3
    km = 6.8157

tetha_opt = utils.tetha_opt(optimum_moisture_content, maximum_dry_density)
sopt = tetha_opt / osat

famb = utils.ambient_factor(a3, b3, km, s, sopt)
cbr = famb * california_bearing_ratio
