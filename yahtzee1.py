from random import randint
import csv
from tabulate import tabulate

class Dice:
    @classmethod
    def roll(cls, dice=5):
        result = []
        for _ in range(dice):
            result.append(str(randint(1, 6)))
        return result

    #remove saved dice from the list "result" and then reroll the results
    @classmethod
    def save(cls, result, *dice):
        saved_dice = []
        for die in dice:
            if die == "1":
                saved_dice.append(result[0])
            elif die == "2":
                saved_dice.append(result[1])
            elif die == "3":
                saved_dice.append(result[2])
            elif die == "4":
                saved_dice.append(result[3])
            elif die == "5":
                saved_dice.append(result[4])
        new_dice = Dice.roll((5 - len(saved_dice)))
        return saved_dice + new_dice

class Scorecard:
    #show the current scorecard################################################################
    @classmethod
    def view(cls):
        scorecard = []
        with open("scorecard.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                scorecard.append(row)
        print(tabulate(scorecard, headers="keys", tablefmt="rounded_grid"))
        print()

    #adding the chosen score to the scorecard assuming a valid catagory, will return False if a filled catagory is picked#########
    @classmethod
    def write(cls, catagory, score):
        scorecard = []
        with open("scorecard.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                scorecard.append(row)

        for d in scorecard:
            #adding new values to the scorecard
            if catagory == d["Catagory"] and d["Score"] == "":
                d["Score"] = str(score)
            elif catagory == d["Catagory"] and d["Score"] != "":
                print(f"'{catagory}' already has a score assigned")
                return False

#########updating all the "Totals" scores
        bonus = 0
        for d in scorecard:
            #updating the "Pre-Bonus Total" for the upper section
            if d["Catagory"] == "Pre-Bonus Total":
                pre_total = [d["Score"] for d in scorecard if
                                                 (d["Catagory"] == "Ones" and d["Score"] != "") or
                                                 (d["Catagory"] == "Twos" and d["Score"] != "") or
                                                 (d["Catagory"] == "Threes" and d["Score"] != "") or
                                                 (d["Catagory"] == "Fours" and d["Score"] != "") or
                                                 (d["Catagory"] == "Fives" and d["Score"] != "") or
                                                 (d["Catagory"] == "Sixes" and d["Score"] != "")]
                if len(pre_total) > 0:
                    pre_total.append("0")
                    d["Score"] = str(eval("+".join(pre_total)))

                    if int(d["Score"]) >= 63:
                        bonus = 1


            #checking if the "Bonus" can be applied
            if d["Catagory"] == "Bonus" and bonus == 1:
                    d["Score"] = "35"

            #updating "Upper Total"
            if d["Catagory"] == "Upper Total":
                upper_total = [d["Score"] for d in scorecard if
                                                 (d["Catagory"] == "Pre-Bonus Total" and d["Score"] != "") or
                                                 (d["Catagory"] == "Bonus" and d["Score"] != "")]
                if len(upper_total) > 0:
                    upper_total.append("0")
                    d["Score"] = str(eval("+".join(upper_total)))

            #updating "Lower Total"
            if d["Catagory"] == "Lower Total":
                lower_total = [d["Score"] for d in scorecard if
                                                (d["Catagory"] == "3 of a kind" and d["Score"] != "") or
                                                (d["Catagory"] == "4 of a kind" and d["Score"] != "") or
                                                (d["Catagory"] == "Full House" and d["Score"] != "") or
                                                (d["Catagory"] == "Small Straight" and d["Score"] != "") or
                                                (d["Catagory"] == "Large Straight" and d["Score"] != "") or
                                                (d["Catagory"] == "YAHTZEE" and d["Score"] != "") or
                                                (d["Catagory"] == "Chance" and d["Score"] != "")]
                if len(lower_total) > 0:
                    lower_total.append("0")
                    d["Score"] = str(eval("+".join(lower_total)))


        with open("scorecard.csv", "w") as file:
            writer = csv.DictWriter(file, fieldnames=["Catagory", "Score"])
            writer.writeheader()
            for line in scorecard:
                writer.writerow(line)

    #cleaning scorecard for a new game#####################################################################################
    @classmethod
    def clean(cls):
        scorecard = []
        with open("scorecard.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                scorecard.append(row)

        for d in scorecard:
            if d["Score"].isdigit() == True:
                d["Score"] = ""

        with open("scorecard.csv", "w") as file:
            writer = csv.DictWriter(file, fieldnames=["Catagory", "Score"])
            writer.writeheader()
            for line in scorecard:
                writer.writerow(line)

    #taking result of dice roll and returning all valid scoring combos#####################################################
    @classmethod
    def choices(cls, results):
        scorecard = []
        choices = []
        times = []

        #dumping the scorecard.csv in the list "scorecard" to use for checking valid scoring combos
        with open("scorecard.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                scorecard.append(row)

        #count how many times each number appears and add that value to list "times"
        num = 1
        while num <= 6:
            times.append(results.count(str(num)))
            num = num + 1

        #checking for valid scoring combos with the given dice results
        for d in scorecard:
            if d["Catagory"] == "YAHTZEE":
                test_score = d["Score"]

#########checking for bonus "YAHTZEE"######################################################################
        if 5 in times and test_score != "" and test_score != "0":
            #updating the "YAHTZEE" and "Lower Total" scores
            for d in scorecard:
                if d["Catagory"] == "YAHTZEE" and d["Score"] != "" and d["Score"] != "0":
                    d["Score"] = str(int(d["Score"]) + 100)
                    for d in scorecard:
                        if d["Catagory"] == "Lower Total":
                            d["Score"] = str(eval(f"{d["Score"]} + 100"))

            with open("scorecard.csv", "w") as file:
                writer = csv.DictWriter(file, fieldnames=["Catagory", "Score"])
                writer.writeheader()
                for line in scorecard:
                    writer.writerow(line)

            #checking for valid upper section scoring and making a variable to track if a valid upper section choice is found or not
            test_x = 0
            #checking "Ones"
            if times[0] == 5:
                for d in scorecard:
                    if d["Catagory"] == "Ones" and d["Score"] == "":
                        choices.append({"catagory": "Ones", "score": (1 * times[0])})
                        test_x = 1

            #checking "Twos"
            elif times[1] == 5:
                for d in scorecard:
                    if d["Catagory"] == "Twos" and d["Score"] == "":
                        choices.append({"catagory": "Twos", "score": (2 * times[1])})
                        test_x = 1

            #checking "Threes"
            elif times[2] == 5:
                for d in scorecard:
                    if d["Catagory"] == "Threes" and d["Score"] == "":
                        choices.append({"catagory": "Threes", "score": (3 * times[2])})
                        test_x = 1

            #checking "Fours"
            elif times[3] == 5:
                for d in scorecard:
                    if d["Catagory"] == "Fours" and d["Score"] == "":
                        choices.append({"catagory": "Fours", "score": (4 * times[3])})
                        test_x = 1

            #checking "Fives"
            elif times[4] == 5:
                for d in scorecard:
                    if d["Catagory"] == "Fives" and d["Score"] == "":
                        choices.append({"catagory": "Fives", "score": (5 * times[4])})
                        test_x = 1

            #checking "Sixes"
            elif times[5] == 5:
                for d in scorecard:
                    if d["Catagory"] == "Sixes" and d["Score"] == "":
                        choices.append({"catagory": "Sixes", "score": (6 * times[5])})
                        test_x = 1

            #checking for valid lower section scoring if there is no valid upper section scoring
            if test_x == 0:
                for d in scorecard:

                    #checking "3 of a kind"
                    if d["Catagory"] == "3 of a kind" and d["Score"] == "":
                        choices.append({"catagory": "3 of a kind",
                        "score": ((1 * times[0]) + (2 * times[1]) + (3 * times[2]) + (4 * times[3]) + (5 * times[4]) + (6 * times[5]))})

                    #checking "4 of a kind"
                    if d["Catagory"] == "4 of a kind" and d["Score"] == "":
                        choices.append({"catagory": "4 of a kind",
                        "score": ((1 * times[0]) + (2 * times[1]) + (3 * times[2]) + (4 * times[3]) + (5 * times[4]) + (6 * times[5]))})

                    #checking "Full House"
                    if d["Catagory"] == "Full House" and d["Score"] == "":
                        choices.append({"catagory": "Full House", "score": 25})

                    #checking "Small Straight"
                    if d["Catagory"] == "Small Straight" and d["Score"] == "":
                        choices.append({"catagory": "Small Straight", "score": 30})

                    #checking "Large Straight"
                    if d["Catagory"] == "Large Straight" and d["Score"] == "":
                        choices.append({"catagory": "Large Straight", "score": 40})

                    #checking "Chance"
                    if d["Catagory"] == "Chance" and d["Score"] == "":
                        choices.append({"catagory": "Chance",
                        "score": ((1 * times[0]) + (2 * times[1]) + (3 * times[2]) + (4 * times[3]) + (5 * times[4]) + (6 * times[5]))})

                    #offering choice to add a zero to an empty upper catagory if all else fails
                    if len(choices) == 0:
                        choices.append({"catagory": "Any empty upper catagory", "score": 0})

#########checking for valid scoring if a bonus YAHTZEE is not rolled############################################################
        else:
            #checking "YAHTZEE"
            if 5 in times:
                for d in scorecard:
                    if d["Catagory"] == "YAHTZEE" and d["Score"] == "":
                        choices.append({"catagory": "YAHTZEE", "score": 50})

            #checking "Ones"
            if times[0] >= 1:
                for d in scorecard:
                    if d["Catagory"] == "Ones" and d["Score"] == "":
                        choices.append({"catagory": "Ones", "score": (1 * times[0])})

            #checking "Twos"
            if times[1] >= 1:
                for d in scorecard:
                    if d["Catagory"] == "Twos" and d["Score"] == "":
                        choices.append({"catagory": "Twos", "score": (2 * times[1])})

            #checking "Threes"
            if times[2] >= 1:
                for d in scorecard:
                    if d["Catagory"] == "Threes" and d["Score"] == "":
                        choices.append({"catagory": "Threes", "score": (3 * times[2])})

            #checking "Fours"
            if times[3] >= 1:
                for d in scorecard:
                    if d["Catagory"] == "Fours" and d["Score"] == "":
                        choices.append({"catagory": "Fours", "score": (4 * times[3])})

            #checking "Fives"
            if times[4] >= 1:
                for d in scorecard:
                    if d["Catagory"] == "Fives" and d["Score"] == "":
                        choices.append({"catagory": "Fives", "score": (5 * times[4])})

            #checking "Sixes"
            if times[5] >= 1:
                for d in scorecard:
                    if d["Catagory"] == "Sixes" and d["Score"] == "":
                        choices.append({"catagory": "Sixes", "score": (6 * times[5])})

            #checking "3 of a kind"
            if 3 in times or 4 in times or 5 in times:
                for d in scorecard:
                    if d["Catagory"] == "3 of a kind" and d["Score"] == "":
                        choices.append({"catagory": "3 of a kind",
                        "score": ((1 * times[0]) + (2 * times[1]) + (3 * times[2]) + (4 * times[3]) + (5 * times[4]) + (6 * times[5]))})

            #checking "4 of a kind"
            if 4 in times or 5 in times:
                for d in scorecard:
                    if d["Catagory"] == "4 of a kind" and d["Score"] == "":
                        choices.append({"catagory": "4 of a kind",
                        "score": ((1 * times[0]) + (2 * times[1]) + (3 * times[2]) + (4 * times[3]) + (5 * times[4]) + (6 * times[5]))})

            #checking "Full House"
            if 3 in times and 2 in times:
                for d in scorecard:
                    if d["Catagory"] == "Full House" and d["Score"] == "":
                        choices.append({"catagory": "Full House", "score": 25})

            #checking "Small Straight"
            if (times[0] == 0 and times[1] == 0 and 1 <= times[2] <= 2 and 1 <= times[3] <= 2 and 1 <= times[4] <= 2 and 1 <= times[5] <= 2) or (
                times[4] == 0 and times[5] == 0 and 1 <= times[0] <= 2 and 1 <= times[1] <= 2 and 1 <= times[2] <= 2 and 1 <= times[3] <= 2) or (
                times[0] == 0 and 1 <= times[1] <= 2 and 1 <= times[2] <= 2 and 1 <= times[3] <= 2 and 1 <= times[4] <= 2 and times[5] == 0) or (
                (times[0] == 0 or times[5] == 0) and times[1] == 1 and times[2] == 1 and times[3] == 1 and times[4] == 1):
                for d in scorecard:
                    if d["Catagory"] == "Small Straight" and d["Score"] == "":
                        choices.append({"catagory": "Small Straight", "score": 30})

            #checking "Large Straight"
            if (times[0] == 0 or times[5] == 0) and times[1] == 1 and times[2] == 1 and times[3] == 1 and times[4] == 1:
                for d in scorecard:
                    if d["Catagory"] == "Large Straight" and d["Score"] == "":
                        choices.append({"catagory": "Large Straight", "score": 40})

            #checking "Chance"
            for d in scorecard:
                if d["Catagory"] == "Chance" and d["Score"] == "":
                    choices.append({"catagory": "Chance",
                    "score": ((1 * times[0]) + (2 * times[1]) + (3 * times[2]) + (4 * times[3]) + (5 * times[4]) + (6 * times[5]))})

            #offering choice of adding zero score to any empty catagory
            choices.append({"catagory": "Any other empty catagory", "score": 0})
        return choices

#results = Dice.roll()
#print(results)
#choice = ["1", "3", "5"]
#print(Dice.save(results, *choice))
#print(Dice.roll())
#Scorecard.view()
#Scorecard.write("Fours", 50)
#Scorecard.clean()
#test = ["2", "2", "2", "2", "2"]
#print(Scorecard.choices(test))

