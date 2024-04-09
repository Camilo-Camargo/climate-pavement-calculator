from climate_pavement import climate_pavements

# specific_gravity =  gs
# plasticity_index =  ip
# california_bearing_ratio =  cbr
# maximum_dry_density =  pdmax
# optimum_moisture_content = wopt

# latitude 5.54
# direction norte

thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 19,
    'california_bearing_ratio': 30,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 5.54,
    'direction': 'N',
    'p200': 58,
}

thick_data = {
    "mode": "thick",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.611,
    'plasticity_index': 7.12,
    'california_bearing_ratio': 100,
    'maximum_dry_density': 2024,
    'optimum_moisture_content': 8.500,
    'sieves_passing': [100, 100, 100, 100, 100, 100, 53.7, 27.1, 27.1],
    'latitude': 5.54,
    'direction': 'N',
    'p200': 8.50
}

thick_data = {
    "mode": "thick",
    "precipitation_mm":
    [15.20, 17.57, 69.99, 173.80, 262.35, 314.20,
        265.81, 172.57, 177.05, 138.11, 117.32, 24.17],
    "temp_celsius":
    [24.26, 24.35, 24.20, 23.81, 23.79, 23.98,
        24.17, 24.34, 24.03, 23.79, 23.71, 23.88],
    'specific_gravity': 2.736,
    'plasticity_index': 19,
    'california_bearing_ratio': 65,
    'maximum_dry_density': 2024,
    'optimum_moisture_content': 8.500,
    'sieves_passing':
    [100.0, 100.0, 85.0, 75.0, 55.0, 45.0, 35.0, 25.0, 15.0],
    'latitude': 5.54,
    'direction': 'N',
    'p200': 5
}
thick_data = {
    "mode": "thick",
    "precipitation_mm":
    [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
        42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
    [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
        12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.611,
    'plasticity_index': 8,
    'california_bearing_ratio': 65,
    'maximum_dry_density': 2024,
    'optimum_moisture_content': 8.500,
    'sieves_passing':
    [100.0, 98.3, 92.8, 85.1, 77.1, 69.9, 53.7, 38.6, 27.1],
    'latitude': 7.0667,
    'direction': 'S',
    'p200': 8
}

thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 6,
    'california_bearing_ratio': 10,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 7.0667,
    'direction': 'N',
    'p200': 7,
}

thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 13,
    'california_bearing_ratio': 10,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 7.0667,
    'direction': 'N',
    'p200': 33,
}

thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 13,
    'california_bearing_ratio': 10,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 7.0667,
    'direction': 'N',
    'p200': 33,
}
thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 13,
    'california_bearing_ratio': 10,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 7.0667,
    'direction': 'N',
    'p200': 33,
}
thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 13,
    'california_bearing_ratio': 10,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 7.0667,
    'direction': 'N',
    'p200': 33,
}


thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 22,
    'california_bearing_ratio': 10,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 7.0667,
    'direction': 'N',
    'p200': 35,
}

thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 35,
    'california_bearing_ratio': 10,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 7.0667,
    'direction': 'N',
    'p200': 35,
}

thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 35,
    'california_bearing_ratio': 10,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 7.0667,
    'direction': 'N',
    'p200': 77,
}

thin_data = {
    "mode": "thin",
    "precipitation_mm":
        [19.03, 21.51, 70.85, 81.81, 87.84, 44.50,
            42.78, 34.74, 29.80, 67.30, 74.58, 24.86],
    "temp_celsius":
        [13.53, 14.06, 14.37, 13.99, 13.75, 13.04,
         12.44, 12.54, 13.07, 13.48, 13.93, 13.55],
    'specific_gravity': 2.736,
    'plasticity_index': 66,
    'california_bearing_ratio': 10,
    'maximum_dry_density': 1240,
    'optimum_moisture_content': 38,
    'latitude': 7.0667,
    'direction': 'N',
    'p200': 88,
}

data = thin_data
result = climate_pavements(data=data)
# print(result["s"])
# print(result["famb"])
# print(result["cbr"])
for r in result:
    print(r, result[r])
