PRODUCTIONS = {
    0: "L->E",
    1: "E->E+T",
    2: "E->T",
    3: "T->T*F",
    4: "T->F",
    5: "F->F^A",
    6: "F->A",
    7: "A->-A",
    8: "A->(E)",
    9: "A->n",
}

def lex(data):
    '''
    Method to return token.
    '''
    num = ""
    for i in data:
        if i in ("*", "-", "+", "^", "(", ")"):
            return (i, None)
        elif i.isdigit():
            num += i
    if num:
        return ("num", int(num))

def tokenize_input(input_string):
    '''
    Method to match lexical units
    '''
    num=''
    tokens=[]
    for i in input_string:
        if i in ("*", "-", "+", "^", "(", ")"):
            if num:
                tokens.append(lex(num))
                num=''
            tokens.append(lex(i))
        elif i.isdigit():
            num += i
        elif not i.isspace():
            print("Invalid Character:"+i)
            exit()
    if num:
        tokens.append(lex(num))
    tokens.append(('$', None))
    return tokens
        
if __name__ == "__main__":
    tokens = tokenize_input(input("Enter String to tokenize: "))
    print(tokens)
