import utils
import numpy as np
from constant import (PARTICLE_SIZE_PASSING_PERCENT,
                      TMI_PLASTIC, TMI_NO_PLASTIC)

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

mode = 'thin'

if mode == 'thin':
    specific_gravity = 2.736  # gs
    plasticity_index = 19  # ip
    california_bearing_ratio = 30  # cbr
    maximum_dry_density = 1240  # pdmax
    optimum_moisture_content = 38  # wopt
    thin_n200 = 58
else:
    specific_gravity = 2.611  # gs
    plasticity_index = 7.12  # ip
    california_bearing_ratio = 100  # cbr
    maximum_dry_density = 2024  # pdmax
    optimum_moisture_content = 8.500  # wopt
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

if mode == 'thin':
    p200 = thin_n200
    wpi = (p200 / 100) * plasticity_index
else:
    p200 = sieves_passing['No200']


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
        (p_before, p_after) = utils.sorround_num_keys(
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

        hm = utils.matric_suction_plastic(a, b, y, s, tmi)
        hr = 500
else:
    p_middle = p200
    (p_before, p_after) = utils.sorround_num_keys(
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

    hm = utils.matric_suction_no_plastic(a, b, y, tmi)
    hr = 100

# SWCC parameter
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

print(cbr)
