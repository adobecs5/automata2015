__author__ = 'CJeon'

# using unicode.
import sys

def inputManager():
    import os
    os.system("stty raw -echo")
    c = sys.stdin.read(1)
    os.system("stty -raw echo")
    # print(ord(c))
    return EngKor_table[c]

def inputManagerPycharm():
    c = input(">>")
    return EngKor_table[c]

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
                "\x7f" : "delete", "\r" : "enter", ' ' : "space",
                "?" : "?", "!": "!", "~": "~", ".": ".", ",": ","}

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

        if self.mid_sound == -1:
            return (list(self.first_sound_table.keys())[list(self.first_sound_table.values()).index(self.first_sound)])

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


def lastFirstHangulAssembler(state, new_letter):
    # treat special cases
    if new_letter in ["delete", "enter", "space", "?", "!", "~", ".", ","]:
        if new_letter == "space":
            state.append(" ")
            return state

        elif new_letter == "delete":
            return state[:-1]

        else:
            state.append(new_letter)
            return state

    # initialize
    split_flag = 1
    if state != [] and state[-1] != " ":
        char = state[-1]
    else:
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

        elif char.final_sound == 0:
            char.add_final_sound(new_letter)

        elif char.final_sound_k in ["ㄱ", "ㄴ", "ㄹ", "ㅂ"]:
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

                if split_flag == 1:
                    state[-1] = char
                    return state

        state.append(new_char)
        return state


def main():
    current_string = []
    while 1:
        new_letter = inputManager()
        #new_letter = inputManagerPycharm()

        current_string = lastFirstHangulAssembler(current_string, new_letter)
        a = 1
        for i in current_string:
            print(i, end="")
        print()

main()


