from cooptools.geometry.curves.curves import CubicBezier, Arc, CircularArc, LineCurve, CatmullRom

def curve_from_json(json):
    curve_type = json['type']

    curve_gen_switch = {
        CubicBezier.__name__: CubicBezier.from_json,
        Arc.__name__: Arc.from_json,
        CircularArc.__name__: CircularArc.from_json,
        LineCurve.__name__: LineCurve.from_json,
        CatmullRom.__name__: CatmullRom.from_json,
    }
    gen_func = curve_gen_switch.get(curve_type, None)

    if gen_func is None:
        raise ValueError(f"Unsupported curve type: {curve_type}")

    return gen_func(json['data'])

def curves_from_json(json):
    curves_data = json['curves']

    curves = []
    for data in curves_data:
        curve = curve_from_json(data)
        curves.append(curve)

    return curves

