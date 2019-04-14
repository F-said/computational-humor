from infoWeb import infoWeb


def main():
    ans = ''
    # Get prompt from user
    prompt = input("Input prompt:")

    # Pass expectation to function that creates graph of expectations
    chumor = infoWeb(prompt)
    chumor.getSubject()

    # Get help from human to make sure subject matter is correct
    print("Please confirm if subject is correct\n")
    subject_matters = chumor.initialSearch()
    for s in subject_matters:
        potential_answer = s
        print("Is ", potential_answer, " the subject of this sentence?\n")
        ans = input("Input y for yes or n for no.")
        if ans is "y":
            chumor.confirmSubject(s)
            print("Thank you for your assistance.")
            break
    # If list of subject matters were exhausted without finding a solution, exit program.
    if ans is "n":
        print("Subject failed to be found. Exiting.")
        return 1

    # Check if outcome subverts expectation
    punch = input("Input outcome:")
    # If outcome does not subvert expectations, exit program
    if not (chumor.detectSubversion(punch)):
        print("Humor ✘")
        return

    if chumor.detectHumor():
        print("Humor ✔")


if __name__ == "__main__":
    main()