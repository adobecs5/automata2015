import sys

__author__ = 'CJeon'
"""
Automata 예비프로젝트 1-1 DFA 시뮬레이터
madeby 전철호
"""


class TransitionTable(object):
    """
    Class for transition table.
    :type states: a list of allowed states in the language.
    :type alphabet: a list of allowed alphabets in the language.
    :type transitions: a list of transitions in the language. len(transitions) = states * alphabet
    """
    states = []
    alphabet = []
    transitions = []

    def __init__(self, data):
        """
        :param data: data read from the txt, processed by load_dfa_data_from_txt
        :return: Nothing.
        """
        states = data[0]
        alphabets = data[1]
        transitions = data[2]

        for state in states:
            self.add_states(state)

        for alphabet in alphabets:
            self.add_alphabet(alphabet)

        for transition in transitions:
            """
            transitions are saved as a list of transitions.
            A transition is composed of (from, alphabet, to).
            Example: if S1+1 => S2, then ("S1", "1", "S2")
            all three components are strings.
            """
            transition = transition.split(" ")
            from_state = transition[0].replace("(", "")
            alphabet = transition[1]
            to_state = transition[2].replace(")", "")
            self.add_transition(from_state, alphabet, to_state)


    def add_states(self, new_state):
        """
        :param new_state: a new state, in type string.
        :return: Exception is raised if new_state is not a string, or new_state is a duplicate.
        """
        assert type(new_state) is str
        assert new_state not in self.states
        self.states.append(new_state)


    def add_alphabet(self, new_alphabet):
        """
        :param new_alphabet: a new alphabet, in type string.
        :return: Exception is raised if new_alphabet is not a string, or new_alphabet is a duplicate.
        """
        assert type(new_alphabet) is str
        assert new_alphabet not in self.alphabet
        self.alphabet.append(new_alphabet)

    def add_transition(self, from_state, alphabet, to_state):
        """
        :param from_state: from state, where the transition begins
        :param alphabet: an input alphabet
        :param to_state: a result
        :return: Exception is raised if certain state or alphabet is undefined.
        """
        # check if all input are type string
        assert type(from_state) is str
        assert type(alphabet) is str
        assert type(to_state) is str
        # check if all input are defined.
        assert from_state in self.states
        assert alphabet in self.alphabet
        assert to_state in self.states

        # define a new transition
        new_transition = [from_state, alphabet, to_state]

        # check if new transition is duplicate
        assert new_transition not in self.transitions

        self.transitions.append(new_transition)

    def check_transition(self, from_state, alphabet):
        """
        :type self: self.
        from_state: starting state
        alphabet: input to starting state
        :returns "to_state"of the transition, or exception
        """
        if from_state not in self.states:
            raise(Exception("Undefined transition %s, %s", from_state, self.transitions))

        if alphabet not in self.alphabet:
            raise(Exception("Undefined transition %s, %s", self.alphabet, self.alphabet))

        for transition in self.transitions:
            if transition[0] == from_state and transition[1] == alphabet:
                return transition[2]

        raise(Exception("Such transition is not defined. %s, %s", from_state, alphabet))


class DFA(object):
    """
    Definition of DFA.
    """
    states = []
    alphabet = []
    transition_function = None
    start_state = ""
    accept_state = []

    def __init__(self, states, alphabet, transition_function, start_state, accept_state):
        # Assign data to the object
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_state = accept_state

    def is_string_a_language(self, string):
        """
        :type string: a string.
        :string: a sequence of alphabets.
        If string is composed of allowed alphabets, return true, else, false.
        :returns: True or False
        """

        string = list(string)
        for idx in range(len(string)):
            if string[idx] in self.alphabet:
                pass

            else:
                return False

        return True

    def language_evaluation(self, string, initial_state):
        """
        :type string: a string
        :returns: Final state of the language
        """
        if not initial_state in self.states:
            raise Exception("Undefined state", initial_state, "defined states are", self.states)

        if not self.is_string_a_language(string):
            raise Exception("string is not a language", string, "Allowed alphabets are", self.alphabet)

        states_undergone = [initial_state]
        string = list(string)

        for alphabet in string:
            if alphabet == "": #if empty string
                states_undergone.append(states_undergone[-1]) #stay at the same position
            else:
                states_undergone.append(self.transition_function.check_fuction(from_state=states_undergone[-1],
                                                                              alphabet=alphabet))

        return states_undergone[-1]


def load_dfa_data_from_txt(path="DFA_data"):
    """
    :param path: path of the datafile. default is DFA_data
    :return: returns DFA data. states, alphabet, transition function, start_state, accept state.
    :data: 0 is states, 1 is alphabets, 2 is transitions, 3 is starting position, 5 is accepting states.
    """
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = data.split("\n")
    data = [data[1].split(", "), data[3].split(", "), data[5].split(", "), data[7], data[9].split(", ")]
    return data[0], data[1], data[2], data[3], data[4]


def user_interface():
    print("Hi, welcome to the DFA simulator.")

    while(True):
        print("Specify input data path. If you want to use the default input(DFA_data), just press enter.")
        data_path = input(">> ")
        if data_path == "":
            data_path = "DFA_data"
        try:
            data = load_dfa_data_from_txt(data_path)
            break
        except FileNotFoundError as e:
            print(e)
            print("try again\n")

    aTransitionTable = TransitionTable(data)
    aDFA = DFA(data[0], data[1], aTransitionTable, data[3], data[4])
    print("Print data successfully loaded.\n")

    while(True):
        print("Please specify the initial state(optional), and the language to be tested.")
        initial_state = input("initial state is: ")
        if initial_state == "":
            initial_state = aDFA.start_state
        language = input("language is: ")
        try:
            last_state = aDFA.language_evaluation(string=language, initial_state=initial_state)
            if last_state in aDFA.accept_state:
                print ("last state is %s" %last_state)
                print("네\n")
            else:
                print ("last state is %s" %last_state)
                print("아니요\n")
        except Exception as e:
            print("Exception occurred.", e)
            print("\n")



if __name__ == '__main__':
    print(sys.version)
    print("This python code is optimized for python 3.4.3\n")

    user_interface()
