# check if the enter value is positive
def check_negative_value(string_to_print):
    while True:
        value = int(input(string_to_print))

        if value <= 0:
            print("Please try to digit a positive value!\n")
        else:
            break

    return value
