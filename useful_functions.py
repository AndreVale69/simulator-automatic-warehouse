# Check if the enter value is positive
def check_negative_value(string_to_print):
    while True:
        value = int(input(string_to_print))

        if value <= 0:
            print("Please try to digit a positive value!\n")
        else:
            break

    return value


# Check if the answer is Y or N, otherwise error
def check_answer(answer: str):
    escape = False

    while True:
        if answer == "N":
            escape = True
            break
        else:
            if answer != "Y":
                answer = str(input("Enter only Y or N if you wanna continue or no! Continue? [Y/N] "))
            else:
                break

    return escape
