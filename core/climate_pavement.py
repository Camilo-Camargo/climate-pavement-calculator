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
        sieves_passing.append(p200)
        sieves_passing = sorted(sieves_passing)

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
            b = TMI_NO_PLASTIC[:1]['b']
            y = TMI_NO_PLASTIC[:1]['y']
            s = TMI_NO_PLASTIC[:1]['s']

        elif wpi >= 50:
            b = TMI_NO_PLASTIC[:-1]['b']
            y = TMI_NO_PLASTIC[:-1]['y']
            s = TMI_NO_PLASTIC[:-1]['s']

        else:
            p_middle = wpi
            tmi_no_plastic_keys = list(TMI_NO_PLASTIC.keys())
            (p_before, p_after) = utils.sorround_num_keys(
                tmi_no_plastic_keys, p_middle)

            p_before = tmi_no_plastic_keys[p_before]
            p_after = tmi_no_plastic_keys[p_after]

            s_before = TMI_NO_PLASTIC[p_before]['s']
            s_after = TMI_NO_PLASTIC[p_after]['s']

            s = utils.lerp(int(p_before), s_before,
                           int(p_after), s_after, p_middle)

            b_before = TMI_NO_PLASTIC[p_before]['b']
            b_after = TMI_NO_PLASTIC[p_after]['b']

            b = utils.lerp(int(p_before), b_before,
                           int(p_after), b_after, p_middle)

            y_before = TMI_NO_PLASTIC[p_before]['y']
            y_after = TMI_NO_PLASTIC[p_after]['y']

            y = utils.lerp(int(p_before), y_before,
                           int(p_after), y_after, p_middle)

        hm = utils.matric_suction_plastic(a, b, y, s, tmi)
        hr = 500
    else:
        if p200 < 0:
            a = TMI_NO_PLASTIC[:1]['a']
            b = TMI_NO_PLASTIC[:1]['b']
            y = TMI_NO_PLASTIC[:1]['y']

        elif p200 > 16:
            a = TMI_NO_PLASTIC[:-1]['a']
            b = TMI_NO_PLASTIC[:-1]['b']
            y = TMI_NO_PLASTIC[:-1]['y']
        else:
            tmi_plastic_keys = list(TMI_PLASTIC.keys())
            p_middle = p200
            (p_before, p_after) = utils.sorround_num_keys(
                tmi_plastic_keys, p_middle)

            p_before = tmi_plastic_keys[p_before]
            p_after = tmi_plastic_keys[p_after]

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
        s_middle = 90
        (s_before, s_after) = utils.sorround_num_keys(
            sieves_passing, s_middle)

        s_before_i = s_before
        s_after_i = s_after

        s_before = sieves_passing[s_before]
        s_after = sieves_passing[s_after]

        d90 = utils.d_generator(
            SIEVES_SIZES_IN_MM[s_before_i],
            SIEVES_SIZES_IN_MM[s_after_i],
            s_before,
            s_after,
            s_middle
        )

        s_middle = 60
        (s_before, s_after) = utils.sorround_num_keys(
            sieves_passing, s_middle)

        s_before_i = s_before
        s_after_i = s_after

        s_before = sieves_passing[s_before]
        s_after = sieves_passing[s_after]

        d60 = utils.d_generator(
            SIEVES_SIZES_IN_MM[s_before_i],
            SIEVES_SIZES_IN_MM[s_after_i],
            s_before,
            s_after,
            s_middle
        )

        s_middle = 20
        (s_before, s_after) = utils.sorround_num_keys(
            sieves_passing, s_middle)

        s_before_i = s_before
        s_after_i = s_after

        s_before = sieves_passing[s_before]
        s_after = sieves_passing[s_after]

        d20 = utils.d_generator(
            SIEVES_SIZES_IN_MM[s_before_i],
            SIEVES_SIZES_IN_MM[s_after_i],
            s_before,
            s_after,
            s_middle
        )

        s_middle = 30
        (s_before, s_after) = utils.sorround_num_keys(
            sieves_passing, s_middle)

        s_before_i = s_before
        s_after_i = s_after

        s_before = sieves_passing[s_before]
        s_after = sieves_passing[s_after]

        d30 = utils.d_generator(
            SIEVES_SIZES_IN_MM[s_before_i],
            SIEVES_SIZES_IN_MM[s_after_i],
            s_before,
            s_after,
            s_middle
        )

        s_middle = 10
        (s_before, s_after) = utils.sorround_num_keys(
            sieves_passing, s_middle)

        s_before_i = s_before
        s_after_i = s_after

        s_before = sieves_passing[s_before]
        s_after = sieves_passing[s_after]

        d10 = utils.d_generator(
            SIEVES_SIZES_IN_MM[s_before_i],
            SIEVES_SIZES_IN_MM[s_after_i],
            s_before,
            s_after,
            s_middle
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
