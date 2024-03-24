from cs50 import get_string
import re


def main():
    s = get_string("Text: ")

    letters = len([c for c in s if c.isalpha()])
    words = len(s.split(" "))
    sentences = len(re.split(r"[.!?]", s)) - 1

    L = letters / words * 100
    S = sentences / words * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    grade = round(index)

    if grade > 15:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {grade}")


main()
