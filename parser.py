from csv import reader
from lex import lex, PRODUCTIONS, tokenize_input

SHIFT = 1
REDUCE = 2
STOP = 3
ACCEPT = 4

def get_action(act: str):
    '''
    A simple function to return action along with required information
    (Example: Which production to use or Which state to shift).
    '''
    if not act:
        return (STOP, None)
    elif act == 'acc':
        return (ACCEPT, None)
    elif act[0] == 'r':
        return (REDUCE, int(act.lstrip('r')))
    elif act[0] == 's':
        return (SHIFT, int(act.lstrip('s')))

class CLRParser:
    '''
    A simple class to implement all the methods required for a CLR Parser
    '''
    def __init__(self):
        self.action = dict()
        self.goto = dict()
        # Load table into class
        with open('Parse_table.csv') as f:
            csv = reader(f)
            symbols = dict()
            for row in csv:
                if row[0] == 'State':
                    for i, sym in enumerate(row[1:], start=1):
                        symbols[i] = sym
                else:
                    state = int(row[0])
                    for i, act in enumerate(row[1:], start=1):
                        sym = symbols[i]
                        if sym.isupper():
                            self.goto[(state, sym)] = int(act) if act else None
                        else:
                            self.action[(state, sym)] = get_action(act)

    def parser(self, data):
        '''
        Method to follow the parsing steps.
        '''
        self.states = [0]
        self.symbols = [('$', None)]
        tokens = tokenize_input(data) # Creates a list of all the tokens from the input.
        i=0

        while True:
            # Quit if tokens are over and string has not been accepted.
            if i>len(tokens):
                print("Stop")
                return

            token  = tokens[i]

            # Get Action
            state = self.states[-1]
            action = self.action[(state, token[0])]
            print("\nStack: ",self.states)
            print("Symbols Stack: ", self.symbols)

            # Action related Logic
            if action[0] == ACCEPT:
                print("Accept")
                print("\nOutput:", self.symbols[-1][1])
                return
            elif action[0] == STOP:
                print("Stop")
                return
            elif action[0] == SHIFT:
                print("Shift State ", action[1])
                self.states.append(action[1])
                self.symbols.append(token)
                i=i+1
                continue
            elif action[0] == REDUCE:
                print("Reduce Using Production Number: ", action[1])
                self.reduce_action(action)
                 
    def reduce_action(self, action):
        '''
        Function to implement reduce logic along with attribute calculations.
        '''
        prod_len = len(PRODUCTIONS[action[1]]) - 3 # Length of RHS
        prod_lhs = PRODUCTIONS[action[1]][0]
        popped = []
        for i in range(prod_len):
            self.states.pop(-1)
            popped.insert(0, self.symbols.pop(-1))

        # Do SDT Calculations
        new_val = 0
        if prod_len == 1:
            new_val = popped[0][1]
        elif prod_len == 2:
            new_val = -popped[1][1]
        elif prod_len == 3:
            if popped[1][0] == '*':
                new_val = popped[0][1] * popped[2][1]
                print("\nSDT CALCULATION: ", popped[0][1], " * ", popped[2][1], " = ", new_val, "\n")
            if popped[1][0] == '+':
                new_val = popped[0][1] + popped[2][1]
                print("\nSDT CALCULATION: ", popped[0][1], " + ", popped[2][1], " = ", new_val, "\n")
            if popped[1][0] == '^':
                new_val = popped[0][1] ** popped[2][1]
                print("\nSDT CALCULATION: ", popped[0][1], " ^ ", popped[2][1], " = ", new_val, "\n")
            if popped[0][0] == '(':
                new_val = popped[1][1]

        # Pass calculated attributes
        self.symbols.append((prod_lhs, new_val))
        print('Next State', self.goto[(self.states[-1], prod_lhs)])
        self.states.append(self.goto[(self.states[-1], prod_lhs)])

if __name__ == "__main__":
    clrparser = CLRParser()
    clrparser.parser(input("Enter String: "))
