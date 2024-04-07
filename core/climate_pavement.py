import utils
from latitude import lerp_latitudes
from constant import (
    TMI_PLASTIC, TMI_NO_PLASTIC,
    SIEVES_SIZES_IN_MM
)


def climate_pavement_validation(data):
    if data['mode'] != 'thin' and data['mode'] != 'thick':
        raise Exception("Invalid mode. Mode must be 'thin' or 'thick'.")

    if data['mode'] == 'thick':
        if 'sieves_passing' not in data:
            raise Exception("You must provide sieves passing for thick mode")

    if "precipitation_mm" not in data:
        raise Exception("You must provide precipitation in mm")

    if "temp_celsius" not in data:
        raise Exception("You must provide temperature in celsius")

    if "specific_gravity" not in data:
        raise Exception("You must provide specific gravity")

    if "plasticity_index" not in data:
        raise Exception("You must provide plasticity index")

    if "california_bearing_ratio" not in data:
        raise Exception("You must provide California Bearing Ratio")

    if "maximum_dry_density" not in data:
        raise Exception("You must provide maximum dry density")

    if "optimum_moisture_content" not in data:
        raise Exception("You must provide optimum moisture content")

    if "p200" not in data:
        raise Exception("You must provide p200")

    if "latitude" not in data:
        raise Exception("You must provide latitude")

    if "direction" not in data:
        raise Exception("You must provide direction")


def climate_pavements(data):
    climate_pavement_validation(data)

    mode = data['mode']

    precipitation_mm = data["precipitation_mm"]
    temp_celsius = data["temp_celsius"]

    specific_gravity = data['specific_gravity']
    plasticity_index = data['plasticity_index']
    california_bearing_ratio = data['california_bearing_ratio']
    maximum_dry_density = data['maximum_dry_density']
    optimum_moisture_content = data['optimum_moisture_content']
    p200 = data['p200']
    latitude = data['latitude']
    direction = data['direction']

    if mode == 'thin':
        wpi = (p200 / 100) * plasticity_index
    else:
        sieves_passing = data['sieves_passing']

    # TODO: Add latitude and longitude interpolation
    sunshine_hours = lerp_latitudes(latitude, direction)
    monthy_days = utils.number_of_day_per_month(2023)
    monthly_heat = utils.monthly_heat_index(temp_celsius)

    anual_heat = sum(monthly_heat)
    anual_3rd_polynomial = utils.third_degree_polynomial(anual_heat)
    ept_unadjust = utils.ept_without_correction(
        temp_celsius, anual_heat, anual_3rd_polynomial)
    ept_adjusted = utils.ept_correction(
        ept_unadjust, sunshine_hours, monthy_days)

    ept_adjusted.append(sum(ept_adjusted))
    precipitation_mm.append(sum(precipitation_mm))
    tmi = utils.thornthwaite_moisture_index(ept_adjusted, precipitation_mm)

    if mode == 'thin':
        a = 0.3
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

        a = utils.lerp(int(p_before), a_before,
                       int(p_after), a_after, p_middle)

        b_before = TMI_PLASTIC[p_before]['b']
        b_after = TMI_PLASTIC[p_after]['b']

        b = utils.lerp(int(p_before), b_before,
                       int(p_after), b_after, p_middle)

        y_before = TMI_PLASTIC[p_before]['y']
        y_after = TMI_PLASTIC[p_after]['y']

        y = utils.lerp(int(p_before), y_before,
                       int(p_after), y_after, p_middle)

        hm = utils.matric_suction_no_plastic(a, b, y, tmi)
        hr = 100

    # SWCC parameter
    ch = utils.adjust_factor(hm, hr)

    if mode == 'thin':
        af = utils.af_swcc_thin(wpi)
        bf = utils.bf_swcc_thin(wpi)
        cf = utils.cf_swcc_thin(wpi)
    else:
        d90 = utils.d_generator(
            SIEVES_SIZES_IN_MM[2],
            SIEVES_SIZES_IN_MM[4],
            sieves_passing[2],
            sieves_passing[4],
            90
        )
        d60 = utils.d_generator(
            SIEVES_SIZES_IN_MM[5],
            SIEVES_SIZES_IN_MM[6],
            sieves_passing[5],
            sieves_passing[6],
            60
        )
        d20 = utils.d_generator(
            SIEVES_SIZES_IN_MM[8],
            SIEVES_SIZES_IN_MM[9],
            sieves_passing[8],
            p200,
            20
        )
        d30 = utils.d_generator(
            SIEVES_SIZES_IN_MM[7],
            SIEVES_SIZES_IN_MM[8],
            sieves_passing[7],
            sieves_passing[8],
            30
        )
        d10 = utils.d_generator(
            SIEVES_SIZES_IN_MM[8],
            SIEVES_SIZES_IN_MM[9],
            sieves_passing[8],
            p200,
            10
        )
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

    s = [x/osat for x in ow]

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
    cbr = [x * california_bearing_ratio for x in famb]

    return {
        "ept_unadjust": ept_unadjust,
        "ept_adjusted": ept_adjusted,
        "tmi": tmi,
        "hm": hm,
        "ch": ch,
        "ow": ow,
        "s": s,
        "famb": famb,
        "cbr": cbr
    }
