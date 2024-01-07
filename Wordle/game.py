import os
from nltk.corpus import words

def read_word(message):
    exists = False
    while not exists:
        word = input(message)
        if word.lower() == "i am a loser":
            break
        if word.lower() == "i am bored":
            break
        if word.lower() in words.words():
            exists = True
        else:
            print("Word doesn't exist in English corpus")

        if len(word) != 5:
            print("Word should contain 5 letters.")
            exists = False

    return word

def print_list_of_letters(message, letters):
    if len(letters) > 0:
        print(message + ' '.join(letters))


def user_trial(word):
    word = word.upper()
    found = False
    loser = False
    trial_count = 0
    letters_not_tried = list(map(chr, range(ord('A'), ord('Z')+1)))
    letters_not_exists = []
    current = ['_', '_', '_', '_', '_']
    while (not found and not loser):
        print_list_of_letters("letters don't exist: ", letters_not_exists)
        print_list_of_letters("letters not tried: ", letters_not_tried)
        print("Current setting: " + ''.join(current))
        result = ""
        if trial_count > 5:
            print("Type 'i am a loser' if you want to give up")
        trial = read_word(f"Trial {trial_count}: ")
        if trial.lower() == "i am a loser":
            loser = True
            continue
        trial = trial.upper()
        if trial != word:
            for i in range(len(trial)):
                if trial[i] in letters_not_tried:
                    letters_not_tried.remove(trial[i])
                if word[i] == trial[i]:
                    result += '*'
                    current[i] = word[i]
                elif trial[i] in word:
                    result += '#'
                else:
                    if trial[i] not in letters_not_exists:
                        letters_not_exists.append(trial[i].upper())
                    result += "-"
        
            print(f"Result : {result}")
        else:
            print("We have a winner, your trial is correct!")
            found = True
        trial_count += 1
    if loser:
        print(f"Sorry, you lost. Try harder next time ;) The word was: {word}")


def cls():
    os.system('cls' if os.name=='nt' else 'clear')
        
# ideas
# add players and scores dataset
if __name__ == "__main__":
    print("Welcome to Wordle")
    bored = False
    while(not bored):
        print("If you want to quit, type 'i am bored'")
        word = read_word("Please enter the word as the admin:")
        if word.lower() == "i am bored":
            bored = True
            continue
        cls()
        user_trial(word)

    print("Thanks for playing :) See you next time")