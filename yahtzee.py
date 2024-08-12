from yahtzee1 import Scorecard, Dice
from tabulate import tabulate
from pyfiglet import Figlet
import csv
import sys
import time
figlet = Figlet()

def input_checker(word):

    #checking "rules"
    if word == "rules":
        print("Here is a link to the rules for yahtzee: https://www.hasbro.com/common/instruct/yahtzee.pdf")
        return True

    #checking "score"
    elif word == "scorecard":
        Scorecard.view()
        return True

    #checking "exit"
    elif word == "exit":
        while True:
            con = input("\nAre you sure you want to exit the game?(Y/N) ").lower().strip()
            if con == "y":
                print("\nGoodbye")
                sys.exit(0)
            elif con == "n":
                return True
            else:
                print("Could not understand input. Please enter Y or N")

    else:
        return word

def main():
    print("\033[2J\033[H", end="", flush=True)
    #welcome text
    figlet.setFont(font="big")
    print(figlet.renderText("Welcome to YAHTZEE !"))

    #displaying the current highscore
    with open("highscore.txt") as file:
        highscore = file.read()
    highscore = f"Highscore :   {highscore}"
    print(figlet.renderText(highscore))

    #running menu options
    while True:
        menu_select = input("New Game(1)\nContinue(2)\nExit(3)\n\nInput: ").strip()
        #checking new game
        if menu_select == "1":
            Scorecard.clean()
            print("\033[2J\033[H", end="", flush=True)
            break

        #checking continue
        elif menu_select == "2":
            print("\033[2J\033[H", end="", flush=True)
            break

        #checking exit
        elif menu_select == "3":
            while True:
                confirm = input("Are you sure you want to exit?(Y/N) ").lower().strip()
                if confirm == "y":
                    print("\033[2J\033[H", end="", flush=True)
                    print("Goodbye")
                    sys.exit(0)
                elif confirm == "n":
                    print()
                    break
                else:
                    print("Could not understand input. Please enter 'Y' or 'N'")

        else:
            print("Could not understand input. Please enter 1, 2, or 3\n")

    #game commands
    print("While playing you can type these commands at any time:")
    print(
    "'rules' to see the rules for yahtzee\n'scorecard' to see the current scorecard\n'exit' to exit the game\n")
    while True:
        con = input("Continue? Entering 'N' will exit the game(Y/N) ").lower().strip()
        if con == "y":
            break
        if con == "n":
            print("Goodbye")
            sys.exit(0)
        else:
            print("Could not understand input. Please enter 'Y' or 'N'")


    #checking scorecard to see how many rounds the game needs
    print("\033[2J\033[H", end="", flush=True)
    round_check = []
    with open("scorecard.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            round_check.append(row)

    rounds = eval("+".join(["1" for row in round_check if
    row["Catagory"] != "Pre-Bonus Total" and row["Catagory"] != "Bonus" and
    row["Catagory"] != "Upper Total" and row["Catagory"] != "Lower Total" and
    row["Catagory"] != "Grand Total" and row["Score"] == ""]))

    #rounds = 13
    #game start
    while rounds > 0:
        print("\nYour first roll for this round is:")
        result = Dice.roll()
        rerolls = 3
        while rerolls > 0:
            print(tabulate([result], tablefmt="simple_outline"))
            print("\nReroll your dice(reroll)\nSave some dice and reroll the remaining dice(save)\nScore your dice(score)")
            strat = input(
            f"{rerolls - 1} reroll(s) remaining\nIf there are 0 rerolls remaining, any valid input will send you to scoring.\nInput: "
            ).lower().strip()
            strat = input_checker(strat)
            if strat == True:
                pass

            elif strat == "reroll":
                if rerolls - 1 > 0:
                    print("\nYour new roll is:")
                result = Dice.roll()
                rerolls = rerolls - 1

            elif strat == "save":
                while True:
                    print("\nCounting from the left, enter the dice you would like to save. For example, '1 3' will save the first and third die.")
                    print("Entering 'back' will bring you back to the previous choices. If nothing is entered all dice will be rerolled.")
                    dice = input("Any other input that is not a digit between 1-5 inclusive will be ignored.\nInput: ").lower().strip()
                    dice = input_checker(dice)
                    if dice == True:
                            pass

                    elif dice == "back":
                        print()
                        break

                    else:
                        die = dice.split(" ")
                        result = Dice.save(result, *die)
                        if rerolls - 1 > 0:
                            print("\nYour new roll is:")
                        rerolls = rerolls - 1
                        break

            elif strat == "score":
                if rerolls - 1 > 0:
                    while True:
                        con = input(
                        "\nAre you sure you want to score your current roll? This decision cannot be reversed(Y/N)\nInput ").lower().strip()
                        con = input_checker(con)
                        if con == True:
                            pass

                        elif con == "n":
                            print()
                            break

                        elif con == "y":
                            rerolls = 0
                            break

                        else:
                            print("Could not understand input. Please enter 'Y' or 'N'")
                else:
                    rerolls = 0

            else:
                print("Please enter a valid command\n")

        #scoring a roll###############################################################################################################
        choices = Scorecard.choices(result)
        loop_break = 0
        while True:
            print("\nHere are your scoring choices:")
            print(tabulate(choices, headers="keys", tablefmt="rounded_grid"))
            print("\nEnter the catagory you want to score.")
            print("Entering 'zero' will give options to score a 0 in any other empty catagory.")
            print("Entering any catagory not on the list will be ignored.")
            catagory = input("Input: ").strip().lower()
            catagory = input_checker(catagory)
            if catagory == True:
                pass

            elif catagory == "zero":
                scorecard = []
                with open("scorecard.csv") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        scorecard.append(row)

                possible_cata = [d["Catagory"] for d in scorecard if
                (d["Score"] == "") and (d["Catagory"] != "Pre-Bonus Total") and (d["Catagory"] != "Bonus") and (
                 d["Catagory"] != "Upper Total") and (d["Catagory"] != "Lower Total") and (d["Catagory"] != "Grand Total")]

                invalid_catagories = [dic["catagory"] for dic in choices]

                possible_catagories = [cata for cata in possible_cata if cata not in invalid_catagories]

                if len(possible_catagories) != 0:
                    while True:
                        print("\nHere are the catagories you can assign a zero to:")
                        print(tabulate([possible_catagories], tablefmt="rounded_outline"))
                        print("\nEnter the catagory you want to assign a zero to. You can enter 'back' to return to the previous choices.")
                        zero = input("Input of a catagory not on the list, or an invalid command, will be ignored.\nInput: ").strip().lower()
                        zero = input_checker(zero)
                        if zero == True:
                            zero = 1000

                        elif zero == "yahtzee":
                            zero = zero.upper()

                        elif zero == "small straight" or zero == "large straight" or zero == "full house":
                            zero = zero.title()

                        elif (zero == "ones") or (zero == "twos") or (zero == "threes") or (zero == "fours") or (zero == "fives") or (
                            zero == "sixes") or (zero == "3 of a kind") or (zero == "4 of a kind") or (zero == "chance"):
                            zero = zero.capitalize()

                        elif zero == "back":
                            break

                        else:
                            print("Please enter a valid catagory")
                            zero = 1000

                        if zero != 1000 and zero in possible_catagories:
                            Scorecard.write(zero, 0)
                            loop_break = loop_break + 1
                            break

                        elif zero != 1000 and zero not in possible_catagories:
                            print("Please enter a valid catagory")

                else:
                    print("There are no empty catagories you can assign a 0 to.")

            elif catagory == "yahtzee":
                catagory = catagory.upper()

            elif catagory == "small straight" or catagory == "large straight" or catagory == "full house":
                catagory = catagory.title()

            elif (catagory == "ones") or (catagory == "twos") or (catagory == "threes") or (catagory == "fours") or (catagory == "fives") or (
                catagory == "sixes") or (catagory == "3 of a kind") or (catagory == "4 of a kind") or (catagory == "chance"):
                catagory = catagory.capitalize()

            else:
                print("Please enter a valid catagory")

            if loop_break > 0:
                break

            for d in choices:
                if catagory == d["catagory"]:
                    score = d["score"]
                    Scorecard.write(catagory, score)
                    loop_break = loop_break + 1

            if loop_break > 0:
                break

        print()
        Scorecard.view()
        rounds = rounds - 1
        if rounds > 0:
            while True:
                _confirm = input("Type 'roll' to start the next round.\nInput: ").strip().lower()
                _confirm = input_checker(_confirm)
                if _confirm == True:
                    pass
                elif _confirm == "roll":
                    break
                else:
                    print("Please enter a valid command.\n")

    #updating the grand total
    grandtotal = []
    with open("scorecard.csv") as file:
        read = csv.DictReader(file)
        for row in read:
            grandtotal.append(row)

    for dic in grandtotal:
        if dic["Catagory"] == "Grand Total":
            dic["Score"] = str(eval("+".join([
            cat["Score"] for cat in grandtotal if cat["Catagory"] == "Upper Total" or cat["Catagory"] == "Lower Total"])))

    with open("scorecard.csv", "w") as file:
         writer = csv.DictWriter(file, fieldnames=["Catagory", "Score"])
         writer.writeheader()
         for line in grandtotal:
            writer.writerow(line)

    print("\nHere is your final card:")
    Scorecard.view()

    #checking if there is a new highscore
    with open("highscore.txt") as file:
        _highscore = file.read()

    for grand in grandtotal:
        if grand["Catagory"] == "Grand Total":
            possible_highscore = grand["Score"]

    if int(possible_highscore) > int(_highscore):
        print(figlet.renderText("\nYou made a new highscore !\n"))
        with open("highscore.txt", "w") as file:
            file.write(possible_highscore)

    else:
        print(figlet.renderText("\nGame Over !"))

    time.sleep(6)
    Scorecard.clean()

if __name__ == "__main__":
    main()
