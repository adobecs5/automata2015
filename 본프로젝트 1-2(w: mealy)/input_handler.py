__author__ = 'CJeon'


def load_dfa_data_from_txt(path):
    """
    :param path: path of the datafile. default is DFA_data
    :return: returns DFA data. states, alphabet, transition function, start_state, accept state.
    :data: [0:states, 1:initial state, 2:input alphabet,
            3:output alphabet, 4:transition_function, 5:output_function)]
    """
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = data.split("\n")
    data = [data[1].split(", "), data[3].split(", "), data[5].split(", "),
            data[7].split(", "), data[9].split(", "), data[11].split(", ")]
    return data[0], data[1], data[2], data[3], data[4], data[5]


def inputManager():
    import os
    import sys
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