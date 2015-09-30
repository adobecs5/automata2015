import sys

__author__ = 'CJeon'
"""
Automata 예비프로젝트 1-2 Mealy Machine 시뮬레이터
madeby 전철호
"""


class FunctionTable(object):
    """
    Class for function table.
    :type states: a list of allowed states in the language.
    :type alphabet: a list of allowed alphabets in the language.
    :type function: a list of functions in the language. len(transitions) = states * alphabet
    """

    def __init__(self, states, alphabets, functions):
        """
        :param data: data read from the txt, processed by load_dfa_data_from_txt
        :return: Nothing.
        """
        self.states = []
        self.alphabet = []
        self.function = []
        for state in states:
            self.add_states(state)

        for alphabet in alphabets:
            self.add_alphabet(alphabet)

        for function in functions:
            """
            functions are saved as a list of functions.
            A function is composed of (from, alphabet, to).
            Example: if S1+1 => S2, then ("S1", "1", "S2")
            all three components are strings.
            """
            function = function.split(" ")
            from_state = function[0].replace("(", "")
            alphabet = function[1]
            result = function[2].replace(")", "")
            self.add_function(from_state, alphabet, result)

    def add_states(self, new_state):
        """
        :param new_state: a new state, in type string.
        :return: Exception is raised if new_state is a duplicate.
        """
        assert new_state not in self.states
        self.states.append(new_state)

    def add_alphabet(self, new_alphabet):
        """
        :param new_alphabet: a new alphabet, in type string.
        :return: Exception is raised if new_alphabet is a duplicate.
        """
        assert new_alphabet not in self.alphabet
        self.alphabet.append(new_alphabet)

    def add_function(self, from_state, alphabet, result):
        """
        :param from_state: from state, where the transition begins
        :param alphabet: an input alphabet
        :param result: a result
        :return: Exception is raised if certain state or alphabet is undefined.
        """
        # check if all input are defined.
        assert from_state in self.states
        assert alphabet in self.alphabet
        # assert result in self.states

        # define a new function
        new_function = [from_state, alphabet, result]

        # check if new function is duplicate
        assert new_function not in self.function

        self.function.append(new_function)

    def check_function(self, from_state, alphabet):
        """
        :type self: self.
        from_state: starting state
        alphabet: input to starting state
        :returns "result"of the function, or exception
        """
        if from_state not in self.states:
            raise(Exception("Undefined function %s, %s", from_state, self.transitions))

        if alphabet not in self.alphabet:
            raise(Exception("Undefined function %s, %s", self.alphabet, self.alphabet))

        for function in self.function:
            if function[0] == from_state and function[1] == alphabet:
                return function[2]

        raise(Exception("Such function is not defined. %s, %s", from_state, alphabet))


class Mealy(object):
    """
    Definition of DFA.
    """
    states = []
    start_state = ""
    input_alphabet = []
    output_alphabet = []
    transition_function = None  # type function table
    output_function = None  # type function table

    def __init__(self, states, start_state, input_alphabet, output_alphabet, transition_function, output_function):
        # Assign data to the object
        self.states = states
        self.input_alphabet = input_alphabet
        self.output_alphabet = output_alphabet
        self.transition_function = transition_function
        self.start_state = start_state[0]
        self.output_function = output_function

    def is_string_a_language(self, string):
        """
        :type string: a string.
        :string: a sequence of alphabets.
        If string is composed of allowed alphabets, return true, else, false.
        :returns: True or False
        """

        string = list(string)
        for idx in range(len(string)):
            if string[idx] in self.input_alphabet:
                pass

            else:
                return False

        return True

    def language_evaluation(self, string, initial_state):
        """

        :type self: object - the mealy machine
        :type string: a string
        :returns: Final state of the language
        """
        if initial_state not in self.states:
            raise Exception("Undefined state", initial_state, "defined states are", self.states)

        if not self.is_string_a_language(string):
            raise Exception("string is not a language", string, "Allowed alphabets are", self.input_alphabet)

        states_undergone = [initial_state]
        outputs_undergone = []
        string = list(string)

        for alphabet in string:
            if alphabet == "":  # if empty string
                states_undergone.append(states_undergone[-1])  # stay at the same position
            else:
                states_undergone.append(self.transition_function.check_function(from_state=states_undergone[-1],
                                                                               alphabet=alphabet))
                outputs_undergone.append(self.output_function.check_function(from_state=states_undergone[-1],
                                                                             alphabet=alphabet))

        return "".join(outputs_undergone)


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


def user_interface():
    print("Hi, welcome to the Mealy simulator.")

    while True:
        print("Specify input data path. If you want to use the default input(mealy_data), just press enter.")
        data_path = input(">> ")
        if data_path == "":
            data_path = "mealy_data"
        try:
            data = load_dfa_data_from_txt(data_path)
            break
        except FileNotFoundError as e:
            print(e)
            print("try again\n")

    a_transition_table = FunctionTable(states = data[0], alphabets=data[2], functions=data[4])
    a_output_table = FunctionTable(states = data[0], alphabets=data[2], functions=data[5])
    a_mealy = Mealy(states = data[0], start_state=data[1], input_alphabet=data[2],
                    output_alphabet=data[3], transition_function=a_transition_table, output_function=a_output_table)
    print("Print data successfully loaded.")

    while(True):
        print("\nPlease specify the initial state(optional), and the language to be tested.")
        initial_state = input("initial state is: ")
        if initial_state == "":
            initial_state = a_mealy.start_state
        language = input("language is: ")
        try:
            result = a_mealy.language_evaluation(string=language, initial_state=initial_state)
            print(result)
        except Exception as e:
            print("Exception occurred.", e)
            print("\n")



if __name__ == '__main__':
    print(sys.version)
    print("This python code is optimized for python 3.4.3\n")

    user_interface()