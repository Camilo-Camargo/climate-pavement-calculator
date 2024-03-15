import numpy as np
from climate_in_pavement import climate_in_pavements

common_data = {
    "precipitation_mm": np.array(
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86]
    ),
    "temp_celsius": np.array(
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55]
    )
}

# specific_gravity =  gs
# plasticity_index =  ip
# california_bearing_ratio =  cbr
# maximum_dry_density =  pdmax
# optimum_moisture_content = wopt

thin_data = {
    'specific_gravity': 2.736,
    'plasticity_index': 19,
    'california_bearing_ratio': 30,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'p200': 58,
}

thick_data = {
    'specific_gravity': 2.611,
    'plasticity_index': 7.12,
    'california_bearing_ratio': 100,
    'maximum_dry_density': 2024,
    'optimum_moisture_content': 8.500,
    'p200': 8.50
}


print(climate_in_pavements(mode='thin', common_data=common_data, data=thin_data))
