import csv
import sys
import os


def main():
    # TODO: Check for command-line usage
    if (
        (len(sys.argv) != 3)
        or (not os.path.exists(sys.argv[1]))
        or (not os.path.exists(sys.argv[2]))
    ):
        print("Usage: python dna.py csvfilename dnatextfile")

    # TODO: Read database file into a variable
    persons = []
    with open(sys.argv[1], "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            persons.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file:
        dna_string = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    dna_split = {}
    for key in persons[0].keys():
        if key == "name":
            continue
        dna_split[key] = longest_match(dna_string, key)

    # TODO: Check database for matching profiles
    for person in persons:
        if all(
            int(person[key]) == value
            for key, value in dna_split.items()
            if key != "name"
        ):
            print(person["name"])
            return
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
