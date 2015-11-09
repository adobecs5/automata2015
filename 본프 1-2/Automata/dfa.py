__author__ = 'CJeon'
global debug
debug = 0

class dfa(object):
    global debug

    def read_from_file(self, filepath = 0):
        if filepath:
            with open(filepath, 'r') as data:
                data_lines = data.readlines()
            for i in range(len(data_lines)):
                data_lines[i] = data_lines[i].replace("\n", "")
        else:
            data_lines = []
            import os.path
            from os import getcwd
            with open("input_manual_text") as texts:
                texts = texts.readlines()
            data_lines.append(input(texts[0]))  # state
            data_lines.append(input(texts[1]))  # symbol
            data_lines.append(input("1"+texts[2]))  # transition function
            while data_lines[-1] not in ['end', '\n']:
                data_lines.append(input(str(len(data_lines)-1)+texts[2]))
            data_lines.append(input(texts[3])) #starting state
            data_lines.append(input(texts[4]+"\n")) #accepting state

        self.states = []
        for state in data_lines[0].split(" "):
            self.states.append(state)

        self.symbols = []
        for symbol in data_lines[1].split(" "):
            self.symbols.append(symbol)

        self.tfs = []
        idx = 2
        while not data_lines[idx] in ["end", "\n"]:
            self.tfs.append(data_lines[idx].split(" "))
            idx += 1

        self.starting_state = data_lines[idx+1]
        self.accepting_state = data_lines[idx+2]

        if (debug):
            print (self.states)
            print (self.symbols)
            print (self.tfs)
            print (self.starting_state)
            print (self.accepting_state)

    def __init__(self):
        self.states = []
        self.symbols = []
        self.tfs = []
        self.starting_state = None
        self.accepting_state = []
        self.move_cache = []


    '''
    states
    symbols
    tfs
    starting_state
    accepting_state
    '''

    def move(self, state, symbol):
        if type(symbol) == type([]):
            if len(symbol) > 1:
                move_first_letter = self.move(state, symbol[0])
                return self.move(move_first_letter, symbol[1:])
            else:
                return self.move(state,symbol[0])

        if symbol == '':
            return state

        for tf in self.tfs:
            if tf[0] == state and tf[1] == symbol:
                return tf[2]
        return None # if no tf exists return none.

    def accepted(self, state):
        if state in self.accepting_state:
            return True
        else:
            return False

    def minimize(self):
        # build string list
        no_of_states = len(self.states)
        string_list = []
        for symbol in self.symbols:
            string_list.append([symbol])
        idx = 0

        for i in range (no_of_states-1):
            temp_list = []
            while idx < len(string_list):
                elem = string_list[idx]
                idx += 1
                for symbol in self.symbols:
                    temp_list.append(elem+[symbol])
            string_list += temp_list
        string_list = [['']] + string_list

        if debug and 0:
            for item in string_list:
                print(item)
            print(len(string_list))

        # run table filling algorithm
        undistinguished_states = []
        for state_1 in self.states:
            for state_2 in self.states:
                duplicate_flag = 0
                if state_1 != state_2:
                    for item in undistinguished_states:
                        if item == [state_1, state_2] or item == [state_2, state_1]:
                            duplicate_flag = 1
                            break
                    if not duplicate_flag:
                        undistinguished_states.append([state_1, state_2])

        result = []
        for item in undistinguished_states:
            result.append(item)

        for pair in undistinguished_states:
            state_1 = pair[0]
            state_2 = pair[1]
            for string in string_list:
                result1 = self.move(state_1, string)
                result2 = self.move(state_2, string)
                if self.accepted(result1) != self.accepted(result2):
                    result.remove(pair)
                    break

        if debug:
            print("undistinguished items")
            for item in result:
                print(item)

        # write new state
        for new_state in result:
            self.states.append(new_state)
            for state in new_state:
                if state in self.states:
                    self.states.remove(state)
                for tf in self.tfs:
                    if tf[0] == state:
                        tf[0] = new_state
                    if tf[2] == state:
                        tf[2] = new_state

        # remove duplicate transitions
        new_tf = []
        for tf in self.tfs:
            if tf in new_tf:
                pass
            else:
                new_tf.append(tf)
        self.tfs = new_tf

        # renew accepting states
        new_accpeting_states = []
        for state in self.states:
            if self.accepted(self.move(state, '')):
                new_accpeting_states.append(state)
        self.accepting_state = new_accpeting_states

        # check
        if debug:
            print("DFA minimization check")
            print("states")
            for state in self.states:
                print(state)
            print("tfs")
            for tf in self.tfs:
                print(tf)

        return self

    def print_dfa(self):
        print("States:",)
        print(self.states)
        print("Vocabulary:",)
        print(self.symbols)
        print("State Transition Functions:")
        for tf in self.tfs:
            print("(%s, %s) => %s" % (tf[0], tf[1], tf[2]))
        print("Initial State:",)
        print(self.starting_state)
        print("Final State:",)
        print(self.accepting_state)
