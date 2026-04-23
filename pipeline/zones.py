ENTRY_LINE_Y = 130
BILLING_LINE_Y = 250


def get_zone(x, y):
    if y < ENTRY_LINE_Y:
        return "ENTRY"
    if y > BILLING_LINE_Y:
        return "BILLING"
    return "FLOOR"