from input_handler import load_dfa_data_from_txt as load_dfa_data_from_txt
from mealy_machine import FunctionTable as FunctionTable
from mealy_machine import Mealy as Mealy
from sys import version


def user_interface():
    print("Hi, welcome to the Hangul simulator.")

    data_path = "hangul_data"
    data = load_dfa_data_from_txt(data_path)

    a_transition_table = FunctionTable(states = data[0], alphabets=data[2], functions=data[4])
    a_output_table = FunctionTable(states = data[0], alphabets=data[2], functions=data[5])
    a_mealy = Mealy(states = data[0], start_state=data[1], input_alphabet=data[2],
                    output_alphabet=data[3], transition_function=a_transition_table, output_function=a_output_table)

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
    print(version)
    print("This python code is optimized for python 3.4.3\n")

    user_interface()