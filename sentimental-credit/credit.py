from cs50 import get_string
import re


def main():
    card = "INVALID"
    number = get_string("Number: ")

    if re.match(r"^(34|37)\d{13}$", number):
        card = "AMEX"
    elif re.match(r"^(51|52|53|54|55)\d{14}$", number):
        card = "MASTERCARD"
    elif re.match(r"^(4)\d{12,15}$", number):
        card = "VISA"

    sum = check_sum(number)

    if sum != 0:
        card = "INVALID"

    print(card)


def check_sum(number):
    sum = 0
    for i, n in enumerate(number[::-1]):
        n = int(n)
        if i % 2 == 1:
            digit = n * 2
            if digit > 9:
                sum += (digit % 10) + (digit // 10)
            else:
                sum += digit
        else:
            sum += n

    return sum % 10


main()
