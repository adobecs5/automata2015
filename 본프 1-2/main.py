__author__ = 'CJeon'
from Automata.nfa import nfa as nfa
a = nfa("example input 4") # if you have an input file
#a = nfa()
b = a.to_dfa()
print("\nDFA\n")
b.print_dfa()
c = b.minimize()
print("\nmDFA\n")
c.print_dfa()