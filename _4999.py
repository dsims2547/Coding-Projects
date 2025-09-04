from random import randint

# Non-recursive implementation to allow for longer games
def Game(numPlayers):
    # Game will call Turn() and Turn() will implement a while loop to prevent recursion
    scores = [0] * numPlayers
    # currentPlayer is 0-indexed
    currentPlayer = 0

    while True:
        someoneWon, scores = Turn(numPlayers, scores, currentPlayer)
        if someoneWon:
            break
        currentPlayer = (currentPlayer + 1) % numPlayers

# Returns (True/False, updated scores). Returns True if someone won, False otherwise
def Turn(numPlayers, scores, currentPlayer):
    widthOfScreen = 90
    currentScore = 0
    used = [False] * 6
    DisplayTurnAndScores(numPlayers, scores, currentPlayer)

    print()
    print("Press enter to roll")
    input()

    # Gets randomly generated dice
    dice = Roll()
    while True:
        # Present the dice
        print()
        MakeDice(dice[0], dice[1], dice[2], dice[3], dice[4], dice[5], used)
        print()
        # Check for bad roll
        availableDice = []
        for i in range(6):
            if not used[i]:
                availableDice.append(dice[i])
        if IsBadRoll(availableDice):
            print("Bad roll!")
            break

        print("The dice are numbered 1 to 6 from left to right")
        numbers = ParseNumbers(input("Enter the numbers of the dice you would like to use: "))

        # For undos
        previousUsed = []
        tempScore = 0

        # Do while loop which terminates when a valid input is given
        while True:
            while numbers is None:
                numbers = ParseNumbers(input("Try again: "))
            for num in numbers:
                if used[num] == True:
                    print("Die number", num, "has already been used")
                    numbers = None
                    break
            if numbers is not None:
                chosenDice = []
                for num in numbers:
                    chosenDice.append(dice[num])
                tempScore = ScoreRoll(chosenDice)
                if IsBadRoll(chosenDice):
                    #print(numbers)
                    print("The dice you've chosen have resulted in a bad roll")
                    numbers = None
                elif tempScore == 0:
                    print("At least one die you've chosen was not able to be scored")
                    numbers = None
                # Upon exiting the while loop we add tempScore to our current score and update the used array
                else:
                    currentScore += tempScore
                    # For undos
                    for value in used:
                        previousUsed.append(value)
                    # We used the dice so we change their used value here
                    for num in numbers:
                        used[num] = True
                    break

        # Present dice again after using some
        print()
        MakeDice(dice[0], dice[1], dice[2], dice[3], dice[4], dice[5], used)
        print()
        # Show score
        scoreText = "Current score: " + str(currentScore)
        print(scoreText.center(widthOfScreen))
        print()

        # If we used all 6 dice we must roll again
        if used == [True] * 6:
            print()
            print("Press enter to roll")
            input()
            used = [False] * 6
            dice = Roll()
            continue

        # Gets the choice from the user
        print("1. Roll")
        print("2. Stop")
        print("3. Undo\n")
        choice = input("Enter your choice: ")

        while not (choice == '1' or choice == '2' or choice == '3'):
            choice = input("Enter a valid choice: ")

        # Rolls the dice before the loop starts over
        if choice == '1':
            # First we roll the dice that haven't been used
            numDice = 0
            for isUsed in used:
                if not isUsed:
                    numDice += 1
            tempDice = Roll(numDice)

            # Then we change those dice here
            tempCounter = 0
            for dieNum in range(6):
                if not used[dieNum]:
                    dice[dieNum] = tempDice[tempCounter]
                    tempCounter += 1
                 
        # If we choose to stop then our current score is added to our total score
        elif choice == '2':
            scores[currentPlayer] += currentScore
            break

        # Undo
        elif choice == '3':
            currentScore -= tempScore
            for i in range(6):
                used[i] = previousUsed[i]
            # May want to skip checking for bad roll
            continue
    
    # We check the win condition
    winner = FindWinner(numPlayers, scores, currentPlayer)
    if winner != -1:
        # Check for ties
        if IsTie(scores, winner):
            winners = []
            for player in range(numPlayers):
                if scores[player] == scores[winner]:
                    winners.append[player + 1]
            PrintWinners(winners)
        # If no tie then print the win message
        else:
            print("Player", winner + 1, "has won!")
        return True, scores
    else:
        return False, scores

# Displays dice based on numbers generated
def MakeDice(num1, num2, num3, num4, num5, num6, used):
    numbers = (num1, num2, num3, num4, num5, num6)
    width = 10
    height = 5
    spacing = 4
    numDice = 6
    # Top
    TopOrBottom(width, spacing, used)
    # Inner rows
    for row in range(height):
        for num in range(numDice):
            if num > 0:
                print(" " * spacing, end = "")
            MakeDieRow(numbers[num], row, width, used[num])
        print()
    # Bottom
    TopOrBottom(width, spacing, used)
    # White text
    print("\033[37m", end = "")

# Makes the inner row for one die based on its generated number and the row number
# We assume width is an even number and width - 4 is divisible by 3
def MakeDieRow(num, row, width, used = False):
    if used:
        # Red text
        print("\033[31m", end = "")
    else:
        # Green text
        print("\033[32m", end = "")
    oneCircleSpacing = width // 2 - 1
    twoCircleSpacing = width // 3 - 1
    print("|", end = "")
    if row == 0 or row == 4:
        if num == 2 or num == 3:
            print(" " * oneCircleSpacing + "()" + " " * oneCircleSpacing, end = "")
        elif num == 4 or num == 5 or num == 6:
            print((" " * twoCircleSpacing + "()") * 2 + " " * twoCircleSpacing, end = "")
        else:
            print(" " * width, end = "")
    elif row == 2:
        if num == 1 or num == 3 or num == 5:
            print(" " * oneCircleSpacing + "()" + " " * oneCircleSpacing, end = "")
        elif num == 6:
            print((" " * twoCircleSpacing + "()") * 2 + " " * twoCircleSpacing, end = "")
        else:
            print(" " * width, end = "")
    else:
        print(" " * width, end = "")
    print("|", end = "")

# Makes the top or bottom row
def TopOrBottom(width, spacing, used):
    for i in range(6):
        if used[i]:
            # Red text
            print("\033[31m", end = "")
        else:
            # Green text
            print("\033[32m", end = "")
        if i > 0:
            print(" " * spacing, end = "")
        print(" " + "-" * width + " ", end = "")
    print()

# Presents a menu for the user to make their choice
# The current player is 0-indexed
def Menu(numPlayers, scores, currentPlayer = 0,  firstRoll = True, dice = [], currentScore = 0, used = [False] * 6):
    widthOfScreen = 90
    if firstRoll:
        DisplayTurnAndScores(numPlayers, scores, currentPlayer)
        print()
        print("Press enter to roll")
        input()
        # Gets randomly generated dice
        dice = Roll()
        # Presents the dice
        #MakeDice(dice[0], dice[1], dice[2], dice[3], dice[4], dice[5])
        Menu(numPlayers, scores, currentPlayer, False, dice, currentScore, [False] * 6)
    else:
        print()
        MakeDice(dice[0], dice[1], dice[2], dice[3], dice[4], dice[5], used)
        print()
        # Check for bad roll
        availableDice = []
        for i in range(6):
            if not used[i]:
                availableDice.append(dice[i])
        if IsBadRoll(availableDice):
            print("Bad roll!")
            Menu(numPlayers, scores, (currentPlayer + 1) % numPlayers)
            return

        print("The dice are numbered 1 to 6 from left to right")
        numbers = ParseNumbers(input("Enter the numbers of the dice you would like to use: "))

        # Do while loop which terminates when a valid input is given
        while True:
            while numbers is None:
                numbers = ParseNumbers(input("Try again: "))
            for num in numbers:
                if used[num] == True:
                    print("Die number", num + 1, "has already been used")
                    numbers = None
                    break
            if numbers is not None:
                chosenDice = []
                for num in numbers:
                    chosenDice.append(dice[num])
                tempScore = ScoreRoll(chosenDice)
                if IsBadRoll(chosenDice):
                    #print(numbers)
                    print("The dice you've chosen have resulted in a bad roll")
                    numbers = None
                elif tempScore == 0:
                    print("At least one die you've chosen was not able to be scored")
                    numbers = None
                # Upon exiting the while loop we add tempScore to our current score and update the used array
                else:
                    currentScore += tempScore
                    for num in numbers:
                        used[num] = True
                    break

        print()
        MakeDice(dice[0], dice[1], dice[2], dice[3], dice[4], dice[5], used)
        print()
        scoreText = "Current score: " + str(currentScore)
        print(scoreText.center(widthOfScreen))
        print()

        # If we used all 6 dice we must roll again
        if used == [True] * 6:
            Menu(numPlayers, scores, currentPlayer, True, currentScore = currentScore)
            return

        # Gets the choice from the user
        print("1. Roll")
        print("2. Stop\n")
        choice = input("Enter your choice: ")

        while(choice != '1' and choice != '2'):
            choice = input("Enter a valid choice: ")

        # Rolls the dice then calls Menu() again
        if choice == '1':
            # First we roll the dice that haven't been used
            numDice = 0
            for isUsed in used:
                if not isUsed:
                    numDice += 1
            tempDice = Roll(numDice)

            # Then we change those dice here
            tempCounter = 0
            for dieNum in range(6):
                if not used[dieNum]:
                    dice[dieNum] = tempDice[tempCounter]
                    tempCounter += 1

            # Then we send it all to the next Menu()
            Menu(numPlayers, scores, currentPlayer, False, dice, currentScore, used)
                 
        # If we choose to stop then our current score is added to our total score
        elif choice == '2':
            scores[currentPlayer] += currentScore
            # We check the win condition
            winner = FindWinner(numPlayers, scores, currentPlayer)
            if winner != -1:
                # Check for ties
                if IsTie(scores, winner):
                    winners = []
                    for player in range(numPlayers):
                        if scores[player] == scores[winner]:
                            winners.append[player + 1]
                    PrintWinners(winners)
                # If no tie then print the win message
                else:
                    print("Player", winner + 1, "has won!")
            else:
                Menu(numPlayers, scores, (currentPlayer + 1) % numPlayers)

# Displays the scores as well as whose turn it is
def DisplayTurnAndScores(numPlayers, scores, currentPlayer):
    widthOfScreen = 90
    sizeOfText = 14

    # First we print whose turn it is
    whoseTurn = "Player " + str(currentPlayer + 1) + "'s turn"
    print(whoseTurn.center(widthOfScreen))
    print()

    # There will be spacing on either side of the scores as well as in between
    spacing = (widthOfScreen - sizeOfText * numPlayers) // (numPlayers + 1)
    for i in range(numPlayers):
        print(" " * spacing, end = "")
        # Format the scores to length 4
        print("Player ", i + 1, ": ", str(scores[i]).ljust(4), sep = "", end = "")
    print()

# Returns the index of the winning player or -1 if no player has won
def FindWinner(numPlayers, scores, currentPlayer):
    maxIndex = 0
    for i in range(1, numPlayers):
        if scores[i] > scores[maxIndex]:
            maxIndex = i
    # The game ends if the last player takes their turn and at least one player has more than 4999 points
    if currentPlayer + 1 == numPlayers and scores[maxIndex] > 4999:
        return maxIndex
    else:
        return -1

def IsTie(scores, winner):
    topScore = scores[winner]
    for i in range(len(scores)):
        if i != winner and scores[i] == topScore:
            return True
    return False

def PrintWinners(winners):
    print("Players ", end = "")
    for i in range(len(winners) - 1):
        if i > 0:
            print(", ", end = "")
        print(winners[i])
    print(" and", winners[len(winners) - 1], "have tied!")

# Dice rolling mechanics
def Roll(numDice = 6):
    dice = []
    for i in range(numDice):
        dice.append(randint(1, 6))
    return dice

def IsBadRoll(dice):
    sortedDice = sorted(dice)
    #print(dice)
    #print(sortedDice)
    return not (ContainsOneOrFive(dice) or FindTrio(sortedDice) != -1 or Straight(sortedDice) or ThreePairs(sortedDice))

def ContainsOneOrFive(dice):
    for die in dice:
        if die == 1 or die == 5:
            return True
    return False

# Scores the roll and determines if it is a bad roll
# For better user experience we may have to call this function twice
def ScoreRoll(dice):
    sortedDice = sorted(dice)
    # Rolls which require all six dice can be scored immediately
    if len(dice) == 6:
        if SixOfAKind(dice):
            return 5000
        elif Straight(sortedDice):
            return 2000
        elif ThreePairs(sortedDice) or TwoTrios(sortedDice):
            return 1500

    score = 0
    # First we find any trios
    trioNum = FindTrio(sortedDice)
    if len(dice) >= 3:
        if trioNum != -1:
            if trioNum == 1:
                score += 1000
            else:
                score += trioNum * 100

    # Then we score any ones or fives that are not part of a trio
    # There also should not be any unscored dice
    trioCount = 0
    for die in dice:
        if die != 1 and die != 5:
            if die != trioNum:
                return 0
            elif trioCount == 3:
                return 0
        if die != trioNum or trioCount >= 3:
            if die == 1:
                score += 100
            elif die == 5:
                score += 50
        if die == trioNum:
            trioCount += 1

    return score

# Hand definitions
def SixOfAKind(dice):
    return dice[0] == dice[1] == dice[2] == dice[3] == dice[4] == dice[5]

# Assumes sorted dice
def Straight(dice):
    return dice == [1, 2, 3, 4, 5, 6]

# Assumes sorted dice
def ThreePairs(dice):
    return len(dice) == 6 and dice[0] == dice[1] and dice[2] == dice[3] and dice[4] == dice[5]

# Assumes sorted dice
def TwoTrios(dice):
    return dice[0] == dice[1] == dice[2] and dice[3] == dice[4] == dice[5]

# Assumes sorted dice
def FindTrio(dice):
    for i in range(len(dice) - 2):
        if dice[i] == dice[i + 1] == dice[i + 2]:
            return dice[i]
    return -1

# Parses the numbers the user enters
def ParseNumbers(numbers):
    nums = []
    for num in numbers:
        if IsInvalid(num):
            print("Invalid input")
            return None
        if num.isdigit():
            nums.append(int(num) - 1)
    if len(nums) == 0:
        print("No dice selected")
        return None
    elif len(nums) > 6:
        print("More than 6 dice selected")
        return None
    return nums

def IsInvalid(c):
    return not (c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6' or c == ' ' or c == ',')

# Some undo button functionality. You can't undo rolls but you can undo which dice you selected
def Undo():
    pass

#(ScoreRoll([1, 1, 1, 1, 1, 1]))
#print(ScoreRoll([6, 4, 2, 3, 5, 1]))
#print(ScoreRoll([6, 3, 2, 3, 6, 2]))
#print(ScoreRoll([2, 5, 5, 2, 5, 2]))
#print(ScoreRoll([1, 3, 4, 1, 6, 1]))
#print(ScoreRoll([1, 3, 3, 6, 3]))

'''print("\033[31m")
\033[32m
print("test")
print("\033[37m")'''

# Gets the number of players
numPlayers = input("Enter the number of players up to 4: ")
while not (numPlayers == '1' or numPlayers == '2' or numPlayers == '3' or numPlayers == '4'):
    numPlayers = input("Enter a valid input: ")
playerNum = int(numPlayers)

print()
Game(playerNum)
