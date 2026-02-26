def calculate_price(base_price: float, occupancy: float):

    factor = 1.0

    if occupancy < 0.4:
        factor -= 0.05
    elif occupancy < 0.7:
        factor += 0.05
    else:
        factor += 0.15

    return round(base_price * factor, 2)