import utils
from latitude_table import LATITUDE


def lerp_latitudes(latitude, direction):
    latitude_keys = list(LATITUDE.keys())
    (before, after) = utils.sorround_num_keys(latitude_keys, latitude)
    before = latitude_keys[before]
    after = latitude_keys[after]
    before_values = LATITUDE[before][direction]
    after_values = LATITUDE[after][direction]

    latitudes = []
    for (x, y) in zip(before_values, after_values):
        latitudes.append(utils.lerp(before, x, after, y, latitude))
    return latitudes
