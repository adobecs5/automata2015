__author__ = 'CJeon'

# using unicode.
import sys
import gc
global delete_flag
"""
The below defined delete_flag works like below:
    0: if new char is just added, it is always set to be 0
    1: if a sound is just deleted, it is set to be zero.You can still modify the letter you were typing.
    2: if a whole char was deleted, it is set to be zero. Now delete function will remove whole character.
"""
delete_flag = 0


def inputManager():
    import os
    os.system("stty raw -echo")
    c = sys.stdin.read(1)
    os.system("stty -raw echo")
    if ord(c) == 3 or ord(c) == 27:
        print (" keyboard interrupt. quitting. Bye~~")
        exit()
    print(ord(c))
    try:
        return EngKor_table[c]
    except:
        return c

def inputManagerPycharm():
    c = input(">>")
    try:
        return EngKor_table[c]
    except:
        return c

EngKor_table = {"q" : "ㅂ", "w" : "ㅈ", "e" : "ㄷ", "r" : "ㄱ",
                "t" : "ㅅ", "y" : "ㅛ", "u" : "ㅕ", "i" : "ㅑ",
                "o" : "ㅐ", "p" : "ㅔ", "a" : "ㅁ", "s" : "ㄴ",
                "d" : "ㅇ", "f" : "ㄹ", "g" : "ㅎ", "h" : "ㅗ",
                "j" : "ㅓ", "k" : "ㅏ", "l" : "ㅣ", "z" : "ㅋ",
                "x" : "ㅌ", "c" : "ㅊ", "v" : "ㅍ", "b" : "ㅠ",
                "n" : "ㅜ", "m" : "ㅡ", "Q" : "ㅃ", "W" : "ㅉ",
                "E" : "ㄸ", "R" : "ㄲ", "T" : "ㅆ", "Y" : "ㅛ",
                "U" : "ㅕ", "I" : "ㅑ", "O" : "ㅒ", "P" : "ㅖ",
                "A" : "ㅁ", "S" : "ㄴ", "D" : "ㅇ", "F" : "ㄹ",
                "G" : "ㅎ", "H" : "ㅗ", "J" : "ㅓ", "K" : "ㅏ",
                "L" : "ㅣ", "Z" : "ㅋ", "X" : "ㅌ", "C" : "ㅊ",
                "V" : "ㅍ", "B" : "ㅠ", "N" : "ㅜ", "M" : "ㅡ",
                "\x7f" : "delete", "\r" : "\n", "enter": "\n",
                "del" : "delete"}

class hangul(object):
    first_sound_table = {"ㄱ": 0, "ㄲ": 1, "ㄴ": 2, "ㄷ": 3, "ㄸ": 4,
                         "ㄹ": 5, "ㅁ": 6, "ㅂ": 7, "ㅃ": 8, "ㅅ": 9,
                         "ㅆ":10, "ㅇ":11, "ㅈ":12, "ㅉ":13, "ㅊ":14,
                         "ㅋ":15, "ㅌ":16, "ㅍ":17, "ㅎ":18}

    mid_sound_table= {"ㅏ" : 0, "ㅐ": 1, "ㅑ": 2, "ㅒ": 3, "ㅓ": 4,
                      "ㅔ" : 5, "ㅕ": 6, "ㅖ": 7, "ㅗ": 8, "ㅘ": 9,
                      "ㅙ" :10, "ㅚ":11, "ㅛ":12, "ㅜ":13, "ㅝ":14,
                      "ㅞ" :15, "ㅟ":16, "ㅠ":17, "ㅡ":18, "ㅢ":19,
                      "ㅣ" :20}

    final_sound_table= { "없 ": 0,"ㄱ" : 1,"ㄲ" : 2,"ㄳ" : 3,"ㄴ" : 4,
                         "ㄵ" : 5,"ㄶ" : 6,"ㄷ" : 7,"ㄹ" : 8,"ㄺ" : 9,
                         "ㄻ" :10,"ㄼ" :11,"ㄽ" :12,"ㄾ" :13,"ㄿ" :14,
                         "ㅀ" :15,"ㅁ" :16,"ㅂ" :17,"ㅄ" :18,"ㅅ" :19,
                         "ㅆ" :20,"ㅇ" :21,"ㅈ" :22,"ㅊ" :23,"ㅋ" :24,
                         "ㅌ" :25,"ㅍ" :26,"ㅎ" :27}

    def __init__(self):
        self.first_sound = -1
        self.mid_sound = -1
        self.final_sound = 0
        self.first_sound_k = None
        self.mid_sound_k = None
        self.final_sound_k = None

    def __repr__(self):
        if self.first_sound == -1 and self.mid_sound != -1:
            return (list(self.mid_sound_table.keys())[list(self.mid_sound_table.values()).index(self.mid_sound)])

        if self.mid_sound == -1 and self.first_sound!= -1:
            return (list(self.first_sound_table.keys())[list(self.first_sound_table.values()).index(self.first_sound)])

        if self.mid_sound == -1 and self.first_sound == -1:
            return ""

        return (chr(self.first_sound*588 + self.mid_sound*28 + self.final_sound + 44032))

    def add_first_sound(self, letter):
        self.first_sound = self.first_sound_table[letter]
        self.first_sound_k = letter

    def add_mid_sound(self, letter):
        self.mid_sound = self.mid_sound_table[letter]
        self.mid_sound_k = letter

    def add_final_sound(self, letter):
        self.final_sound = self.final_sound_table[letter]
        self.final_sound_k = letter

def delete(state):
    global delete_flag
    if delete_flag == 2:
        # if delete_flag is 1, just delete the last char.
        # set delete flag to be zero so that no editing is possible
        delete_flag = 2
        return state[:-1]

    # increment delete flag
    delete_flag +=1
    if state != [] and type(state[-1]) is hangul:
        char = state[-1]
        if char.final_sound != 0: # if it has a final sound
            char.final_sound = 0 # delete it
        elif char.mid_sound != -1: # if it has a mid sound
            char.mid_sound = -1 # delete it
            if char.first_sound == -1: # if it only had a mid sound
                return state[:-1] # delete whole character
        elif char.first_sound != -1: # if it has only first sound
            state = state[:-1] # remove whole character
            delete_flag = 2
            return state # return state without last char

        state[-1] = char # return fixed char
        return state

    return state[:-1] # if it were not Hangul remove last char



def lastFirstHangulAssembler(state, new_letter):
    global delete_flag

    # treat special cases
    if new_letter not in hangul().first_sound_table and new_letter not in hangul().mid_sound_table:
        if new_letter == "delete":
            return delete(state)

        else:
            # it was not delete, so set delete flag to be zero
            delete_flag = 0
            state.append(new_letter)
            return state

    # initialize
    split_flag = 1
    if state != [] and type(state[-1]) is hangul and delete_flag != 2:
        char = state[-1]

    else:
        delete_flag = 0
        new_char = hangul()
        try:
            new_char.add_first_sound(new_letter)
        except:
            new_char.add_mid_sound(new_letter)
        state.append(new_char)
        return state

    if new_letter in char.first_sound_table:
        # handle 자음

        if char.mid_sound == -1: # if char has no mid sound
            new_char = hangul()
            new_char.add_first_sound(new_letter)
            state.append(new_char)
            return state

        elif char.final_sound == 0: # if char has no final sound
            try: # if is final-soundable
                char.add_final_sound(new_letter)

            except:
                new_char = hangul()
                new_char.add_first_sound(new_letter)
                state.append(new_char)
                return state

        elif char.final_sound_k in ["ㄱ", "ㄴ", "ㄹ", "ㅂ"]:
            char, split_flag = handle_double_final_sound(char, new_letter, split_flag)

        else:
            new_char = hangul()
            new_char.add_first_sound(new_letter)
            state.append(new_char)
            return state

        if split_flag == 0:
            new_char = hangul()
            new_char.add_first_sound(new_letter)
            state.append(new_char)
            return state

        state[-1] = char
        return state

    else:
        # handle 모음
        new_char = hangul()
        new_char.add_mid_sound(new_letter)

        if char.mid_sound == -1: # if letter does not have a vowel
            char.add_mid_sound(new_letter)
            state[-1] = char
            return state

        elif char.final_sound != 0: # if there is a final sound
                final_sound_k = char.final_sound_k
                char.final_sound = 0 # remove last sound
                if final_sound_k in ["ㄳ", "ㄵ","ㄶ","ㄺ", "ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅄ"]:
                    if final_sound_k == "ㄳ":
                        char.add_final_sound("ㄱ")
                        new_char.add_first_sound("ㅅ")

                    elif final_sound_k == "ㄵ":
                        char.add_final_sound("ㄴ")
                        new_char.add_first_sound("ㅈ")

                    elif final_sound_k == "ㄶ":
                        char.add_final_sound("ㄴ")
                        new_char.add_first_sound("ㅎ")

                    elif final_sound_k == "ㄺ":
                        char.add_final_sound("ㄹ")
                        new_char.add_first_sound("ㄱ")

                    elif final_sound_k == "ㄻ":
                        char.add_final_sound("ㄹ")
                        new_char.add_first_sound("ㅁ")

                    elif final_sound_k == "ㄼ":
                        char.add_final_sound("ㄹ")
                        new_char.add_first_sound("ㅂ")

                    elif final_sound_k == "ㄽ":
                        char.add_final_sound("ㄹ")
                        new_char.add_first_sound("ㅅ")

                    elif final_sound_k == "ㄾ":
                        char.add_final_sound("ㄹ")
                        new_char.add_first_sound("ㅌ")

                    elif final_sound_k == "ㄿ":
                        char.add_final_sound("ㄹ")
                        new_char.add_first_sound("ㅍ")

                    elif final_sound_k == "ㅀ":
                        char.add_final_sound("ㄹ")
                        new_char.add_first_sound("ㅎ")

                    elif final_sound_k == "ㅄ":
                        char.add_final_sound("ㅂ")
                        new_char.add_first_sound("ㅅ")

                else:
                    new_char.add_first_sound(final_sound_k)

                state[-1] = char

        else: # if it has a vowel
            vowel = char.mid_sound_k
            if vowel in ["ㅗ", "ㅜ", "ㅡ"]:
                char, split_flag = handle_double_mid_sound(char, new_letter, split_flag)

                if split_flag == 1:
                    state[-1] = char
                    return state


        state.append(new_char)
        return state

def create_new_hangul(state, new_letter):
    new_char = hangul()
    try:
        new_char.add_first_sound(new_letter)
    except:
        new_char.add_mid_sound(new_letter)
    state.append(new_char)
    return state

def handle_double_final_sound(char, new_letter, split_flag):
    if char.final_sound_k == "ㄱ":
        if new_letter == "ㅅ":
            char.add_final_sound("ㄳ")
        else:
            split_flag = 0

    elif char.final_sound_k == "ㄴ":
        if new_letter == "ㅈ":
            char.add_final_sound("ㄵ")
        elif new_letter == "ㅎ":
            char.add_final_sound("ㄶ")
        else:
            split_flag = 0

    elif char.final_sound_k == "ㄹ":
        if new_letter == "ㄱ":
            char.add_final_sound("ㄺ")

        elif new_letter == "ㅁ":
            char.add_final_sound("ㄻ")

        elif new_letter == "ㅂ":
            char.add_final_sound("ㄼ")

        elif new_letter == "ㅅ":
            char.add_final_sound("ㄽ")

        elif new_letter == "ㅌ":
            char.add_final_sound("ㄾ")

        elif new_letter == "ㅍ":
            char.add_final_sound("ㄿ")

        elif new_letter == "ㅎ":
            char.add_final_sound("ㅀ")
        else:
            split_flag = 0


    elif char.final_sound_k == "ㅂ":
        if new_letter == "ㅅ":
            char.add_final_sound("ㅄ")
        else:
            split_flag = 0

    return char, split_flag

def handle_double_mid_sound(char, new_letter, split_flag):
    vowel = char.mid_sound_k
    if vowel == "ㅗ":
        if new_letter == "ㅏ":
            char.add_mid_sound("ㅘ")
        elif new_letter == "ㅐ":
            char.add_mid_sound("ㅙ")
        elif new_letter == "ㅣ":
            char.add_mid_sound("ㅚ")
        else:
            split_flag = 0

    elif vowel == "ㅜ":
        if new_letter == "ㅓ":
            char.add_mid_sound("ㅝ")
        elif new_letter == "ㅔ":
            char.add_mid_sound("ㅞ")
        elif new_letter == "ㅣ":
            char.add_mid_sound("ㅟ")
        else:
            split_flag = 0

    elif vowel == "ㅡ":
        if new_letter == "ㅣ":
            char.add_mid_sound("ㅢ")
        else:
            split_flag = 0

    return char, split_flag


def firstFirstHangulAssembler(state, new_letter):
    # 초성 우선 어셈블러
    global delete_flag

    # treat special cases
    if new_letter not in hangul().first_sound_table and new_letter not in hangul().mid_sound_table:
        if new_letter == "delete":
            return delete(state)

        elif new_letter == " ":
            try:
                char = state[-1]
                older_char = state[-2]
                if older_char.final_sound == 0 and char.mid_sound == -1:
                    # if letter before was just first sound and
                    # letter before that does not have a final sound,
                    # make the first sound last of letter before that
                    older_char.add_final_sound(char.first_sound_k)
                    state[-2] = older_char
                    # replace last char with space
                    state[-1] = " "
                    return state

                if older_char.final_sound_k in ["ㄱ", "ㄴ", "ㄹ", "ㅂ"]:
                    split_flag = 1
                    older_char, split_flag = handle_double_final_sound(older_char, char.first_sound_k, split_flag)
                    if split_flag == 1:
                        state[-2] = older_char
                        state[-1] = " "
                        return state
                    else:
                        raise Exception("break")

                raise Exception("break")
            except:
                delete_flag = 0
                state.append(new_letter)
                return state

        else:
            # it was not delete, so set delete flag to be zero
            delete_flag = 0
            state.append(new_letter)
            return state

    if state != [] and type(state[-1]) is hangul :
        char = state[-1]
    else:
        return create_new_hangul(state, new_letter)

    if len(state) > 1 and type(state[-2]) is hangul:
        older_char = state[-2]
    else:
        older_char = hangul()
        older_char.add_final_sound("ㄱ")

    if new_letter in hangul().first_sound_table:
        # handle 자음
        if char.mid_sound != -1:
            #if letter before has a middle sound
            return create_new_hangul(state, new_letter)

        if char.first_sound != -1:
        # if letter before has a first sound
            if older_char.final_sound == 0:
            # if letter before before does not have a final sound
            # make the first sound of letter before last sound of letter before before
                if older_char.mid_sound != -1:
                    # if older char has a vowel
                    older_char.add_final_sound(char.first_sound_k)
                    char.add_first_sound(new_letter)
                    state[-1] = char
                    state[-2] = older_char
                    return state

                else:
                    return create_new_hangul(state, new_letter)

            elif older_char.final_sound_k in ["ㄱ", "ㄴ", "ㄹ", "ㅂ"]:
                split_flag = 1
                older_char, split_flag = handle_double_final_sound(older_char, char.first_sound_k, split_flag)
                if split_flag == 1:
                    state[-2] = older_char
                    return create_new_hangul(state[:-1], new_letter)
                else:
                    return create_new_hangul(state, new_letter)

            else:
                #add new hangul with only first sound.
                return create_new_hangul(state, new_letter)

    elif new_letter in hangul().mid_sound_table:
        # handle 모음
        if char.first_sound != -1:
            # if letter before have a first sound
            if char.mid_sound == -1:
                #if letter before does not have a vowel
                char.add_mid_sound(new_letter)
                state[-1] = char
            elif char.mid_sound != -1:
                #if letter before have a vowel
                vowel = char.mid_sound_k
                if vowel in ["ㅗ", "ㅜ", "ㅡ"]:
                    split_flag = 0
                    char, split_flag = handle_double_mid_sound(char, new_letter, split_flag)
                    state[-1] = char

                else:
                    return create_new_hangul(state, new_letter)


        else:
            return create_new_hangul(state, new_letter)

        return state

    raise Exception("Something Wrong")


def main():
    gc.enable()
    for i in range(100):
        print ("#", end="")
    logo = open("logo.txt", "r")
    logotxt = logo.readlines()
    logo.close()
    for i in logotxt:
        if i != "\n":
            print(i, end="")
    print("")
    for i in range(100):
        print ("#", end="")
    print("")

    intro = open("intro.txt", "r")
    introtxt = intro.readlines()
    intro.close()
    for i in introtxt:
        if i != "\n":
            print(i, end="")
    print("")

    print("Please choose input method")
    print("1. Raw mode. Program will catch your input without you pressing enter. (recommended)")
    print("2. Normal mode. You should press enter every input. If 1 does not work, use this instead.")
    input_mode = input(">>")
    if input_mode == "1":
        print ("You chose raw mode.")
    elif input_mode == "2":
        print ("You chose normal mode. type \"enter\" and \"del\" to linebreak and delete")
    else:
        raise Exception("Invalid choice")

    print("\nPlease choose testing function")
    print("1. 받침우선")
    print("2. 초성우선")
    test_mode = input(">>")
    if test_mode == "1":
        print ("You chose 받침우선.")
    elif test_mode == "2":
        print ("You chose 초성우선")
    else:
        raise Exception("Invalid choice")

    current_string = []
    while 1:
        if input_mode == "1":
            new_letter = inputManager()
        else:
            new_letter = inputManagerPycharm()

        if test_mode == "1":
            current_string = lastFirstHangulAssembler(current_string, new_letter)
        else:
            current_string = firstFirstHangulAssembler(current_string, new_letter)
        for i in current_string:
            print(i, end="")
        print()

main()