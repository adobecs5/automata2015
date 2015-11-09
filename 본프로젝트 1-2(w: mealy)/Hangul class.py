# using unicode.
global delete_flag
"""
The below defined delete_flag works like below:
    0: if new char is just added, it is always set to be 0
    1: if a sound is just deleted, it is set to be zero.You can still modify the letter you were typing.
    2: if a whole char was deleted, it is set to be zero. Now delete function will remove whole character.
"""
delete_flag = 0


class hangul(object):
    first_sound_table = {"ㄱ": 0, "ㄲ": 1, "ㄴ": 2, "ㄷ": 3, "ㄸ": 4,
                         "ㄹ": 5, "ㅁ": 6, "ㅂ": 7, "ㅃ": 8, "ㅅ": 9,
                         "ㅆ":10, "ㅇ":11, "ㅈ":12, "ㅉ":13, "ㅊ":14,
                         "ㅋ":15, "ㅌ":16, "ㅍ":17, "ㅎ":18}

    mid_sound_table = {"ㅏ": 0, "ㅐ": 1, "ㅑ": 2, "ㅒ": 3, "ㅓ": 4,
                       "ㅔ": 5, "ㅕ": 6, "ㅖ": 7, "ㅗ": 8, "ㅘ": 9,
                       "ㅙ":10, "ㅚ":11, "ㅛ":12, "ㅜ":13, "ㅝ":14,
                       "ㅞ":15, "ㅟ":16, "ㅠ":17, "ㅡ":18, "ㅢ":19,
                       "ㅣ":20}

    final_sound_table = {"없": 0,"ㄱ": 1,"ㄲ": 2,"ㄳ": 3,"ㄴ": 4,
                         "ㄵ": 5,"ㄶ": 6,"ㄷ": 7,"ㄹ": 8,"ㄺ": 9,
                         "ㄻ":10,"ㄼ":11,"ㄽ":12,"ㄾ":13,"ㄿ":14,
                         "ㅀ":15,"ㅁ":16,"ㅂ":17,"ㅄ":18,"ㅅ":19,
                         "ㅆ":20,"ㅇ":21,"ㅈ":22,"ㅊ":23,"ㅋ":24,
                         "ㅌ":25,"ㅍ":26,"ㅎ":27}

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

        return chr(self.first_sound*588 + self.mid_sound*28 + self.final_sound + 44032)

    def add_first_sound(self, letter):
        self.first_sound = self.first_sound_table[letter]
        self.first_sound_k = letter

    def add_mid_sound(self, letter):
        self.mid_sound = self.mid_sound_table[letter]
        self.mid_sound_k = letter

    def add_final_sound(self, letter):
        self.final_sound = self.final_sound_table[letter]
        self.final_sound_k = letter

    def double_final_sound(self, final_sound_k):
        if final_sound_k[0] == "ㄱ":
            if final_sound_k[1] == "ㅅ":
                return "ㄳ"
            else:
                raise Exception("Undefined double final sound error", final_sound_k)

        elif final_sound_k[0] == "ㄴ":
            if final_sound_k[1] == "ㅈ":
                return "ㄵ"
            elif final_sound_k[1] == "ㅎ":
                return "ㄶ"
            else:
                raise Exception("Undefined double final sound error", final_sound_k)

        elif final_sound_k[0] == "ㄹ":
            if final_sound_k[1] == "ㄱ":
                return "ㄺ"
            elif final_sound_k[1] == "ㅁ":
                return "ㄻ"
            elif final_sound_k[1] == "ㅂ":
                return "ㄼ"
            elif final_sound_k[1] == "ㅅ":
                return "ㄽ"
            elif final_sound_k[1] == "ㅌ":
                return "ㄾ"
            elif final_sound_k[1] == "ㅍ":
                return "ㄿ"
            elif final_sound_k[1] == "ㅎ":
                return "ㅀ"
            else:
                raise Exception("Undefined double final sound error", final_sound_k)

        elif final_sound_k[0] == "ㅂ":
            if final_sound_k[1] == "ㅅ":
                return "ㅄ"
            else:
                raise Exception("Undefined double final sound error", final_sound_k)

        else:
            raise Exception("undefined double final sound.", final_sound_k)