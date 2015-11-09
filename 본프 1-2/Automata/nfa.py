__author__ = 'CJeon'
global debug
debug = 0

class nfa(object):
    global debug
    def __init__(self, filepath = 0):
        self.e_closure_cache=[]
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
        self.accepting_state = []
        for state in data_lines[idx+2].split(" "):
            self.accepting_state.append(state)

        if (debug):
            print (self.states)
            print (self.symbols)
            print (self.tfs)
            print (self.starting_state)
            print (self.accepting_state)


    '''
    states
    symbols
    tfs
    starting_state
    accepting_state
    '''
    def to_dfa(self):
        dfa_states = []
        done = []
        dfa_symbols = self.symbols
        dfa_tfs = []
        dfa_starting_state = None
        dfa_accepting_state = None
        dfa_states.append(self.e_closure(self.starting_state))
        while len(dfa_states) != len(done):
            idx = 0
            while dfa_states[idx] in done:
                idx += 1
            state = dfa_states[idx]
            for symbol in self.symbols:
                moved = self.move(state, symbol)
                e_ed = self.e_closure(moved)
                if not e_ed in dfa_states:
                    dfa_states.append(e_ed)
                if not state in done:
                    done.append(state)
                if e_ed == [] or e_ed == [[]]:
                    # Dead state
                    dfa_states.pop()
                    if not "dead state" in dfa_states:
                        dfa_states.append("dead state")
                    dfa_tfs.append([state, symbol, "dead state"])
                else:
                    dfa_tfs.append([state, symbol, e_ed])

        from Automata.dfa import dfa
        dfa = dfa()
        dfa.states = dfa_states
        dfa.symbols = self.symbols
        dfa.tfs = dfa_tfs
        for state in dfa.states:
            for acceptingstate in self.accepting_state:
                if acceptingstate == state or (type(state) == type([]) and acceptingstate in state):
                    dfa.accepting_state.append(state)
            if self.starting_state in state:
                dfa.starting_state = state

        if debug:
            print(dfa_states)
            for line in dfa_tfs:
                print(line)

        return dfa


    def e_closure(self, state, prev = None):
        e_closure = []
        for cache in self.e_closure_cache:
            if cache[0] == state or (type(state) == type([]) and len(state)==1 and cache[0]==state[0]):
                if cache[1] == prev:
                    return cache[1]
                else:
                 return cache[1]

        if type(state) == type([]):
            for item in state:
                if type(item) == type([]):
                    for elem in item:
                        e_closure.append(elem)
                else:
                    e_closure.append(item)

            for elem in state:
                result = self.e_closure(elem, state)
                if type(result) == type([]):
                    for item in result:
                        if not item in e_closure:
                            e_closure.append(item)
                elif not result in e_closure:
                    # if item is not duplicate
                    e_closure.append(item)

        else:
            e_closure.append(state)
            for tf in self.tfs:
                if tf[0] == state and tf[1] == 'eps':
                    e_closure.append(tf[2])

        self.e_closure_cache.append([state, e_closure])
        for i in range (len(self.e_closure_cache)):
            if self.e_closure_cache[i][1] == state:
                self.e_closure_cache[i][1] = e_closure
        if e_closure == prev:
            # if no more epsilon closure was found
            return e_closure
        else:
            return self.e_closure(e_closure, state)

    def move(self, state, symbol):
        return_val = []
        if type(state) == type([]):
            for elem in state:
                return_val.append(self.move(elem, symbol))
                if return_val[-1] == []:
                    return_val.pop()
            return return_val

        for tf in self.tfs:
            if tf[0] == state and tf[1] == symbol:
                return_val.append(tf[2])
        if len(return_val) == 1:
            return return_val[0]
        return return_val

