import utils
import numpy as np


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


def tmi(ept_adjusted, precipitation,):
    return 75 * (precipitation / ept_adjusted - 1) + 10


def third_degree_polynomial(anual_temp):
    a = (675 * 10**-9 * anual_temp ** 3)
    b = (771 * 10**-7 * anual_temp ** 2)
    c = (1792 * 10**-5 * anual_temp)
    d = 0.49239

    return a - b + c + d


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
print(tmi(ept_adjusted, precipitation_mm))

assert (
    len(SIEVES_SIZES_IN_MM) == len(sieves_passing)
), "Missing sieves passing elements."
