import re
import sys
import pyfiglet
import colorama

colorama.init()

class PDA:
    def __init__(
        self,
        states,
        input_symbols,
        stack_symbols,
        initial_state,
        initial_stack_symbol,
        final_states,
        transition_function,
    ):
        self.states = states
        self.input_symbols = input_symbols
        self.stack_symbols = stack_symbols
        self.initial_state = initial_state
        self.initial_stack_symbol = initial_stack_symbol
        self.final_states = final_states
        self.transition_function = transition_function

    def process(self, string):
        current_state = self.initial_state
        stack = [self.initial_stack_symbol]

        for symbol in string:
            if (current_state, symbol, stack[-1]) in self.transition_function:
                current_state, new_stack_symbols = self.transition_function[
                    (current_state, symbol, stack[-1])
                ]
                stack.pop()
                for new_stack_symbol in reversed(new_stack_symbols):
                    stack.append(new_stack_symbol)
            else:
                return False

        if (current_state, "", stack[-1]) in self.transition_function:
            current_state, new_stack_symbols = self.transition_function[
                (current_state, "", stack[-1])
            ]
            stack.pop()
            for new_stack_symbol in reversed(new_stack_symbols):
                stack.append(new_stack_symbol)

        if current_state in self.final_states and len(stack) == 0:
            return True
        else:
            return False


pathFilePda = "pda/" + sys.argv[1]
pathFileHTML = "html/" + sys.argv[2].replace('"', "")

with open(pathFilePda, "r") as file:
    lines = file.readlines()
    states = lines[0].replace("\n", "").split(" ")
    input_symbols = lines[1].replace("\n", "").split(" ")
    input_symbols = [symbol if symbol != "e" else '"' for symbol in input_symbols]
    stack_symbols = lines[2].replace("\n", "").split(" ")
    initial_state = lines[3].replace("\n", "")
    initial_stack_symbol = lines[4].replace("\n", "")
    final_states = lines[5].replace("\n", "").split(" ")
    transition_function = {}
    for line in lines[6:]:
        transition = line.replace("\n", "").split(" ")
        if transition[1] == "e":
            transition[1] = ""
        if transition[2] == "e":
            transition[2] = ""
        if transition[4] == "e":
            transition[4] = []
        transition_function[(transition[0], transition[1], transition[2])] = (
            transition[3],
            list(transition[4]),
        )
file.close()

fileHTML = open(pathFileHTML, "r")
isiHTML = fileHTML.read()
isiHTML = isiHTML.replace("\n", "").replace("    ", "")
fileHTML.close()

def print_fancy(text, font='slant', color='green'):
    if color == 'red':
        color_code = colorama.Fore.LIGHTRED_EX
    elif color == 'green':
        color_code = colorama.Fore.LIGHTGREEN_EX
    else:
        color_code = colorama.Fore.RESET

    print(color_code + pyfiglet.figlet_format(text, font=font) + colorama.Style.RESET_ALL)

accept = "Accepted"
reject = "Syntax Error"
font = "slant"
green = "green"
red = "red"


pda = PDA(
    states,
    input_symbols,
    stack_symbols,
    initial_state,
    initial_stack_symbol,
    final_states,
    transition_function,
)

isiHTML = "".join(isiHTML.split())
tokens = re.findall(
    r'/html|/head|/body|/title|/link|/script|/button|/abbr|/form|/strong|/small|/table|/div|/tr|/th|/td|/h1|/h2|/h3|/h4|/h5|/h6|/em|/p|/b|<|>|html|head|body|link|title|button|form|input|img|id|class|style|method|rel|href|script|action|src|type|div|abbr|strong|small|table|!--|--|tr|td|h1|h2|h3|h4|h5|h6|em|p|=|alt|hr|th|br|/a|a|b|/|"[^"]*"',
    isiHTML,
)
newTokens = []
buka = False
comment = False
type = False
kutiptype = False
for i in range(len(tokens)):
    if tokens[i] == "!--":
        comment = True
        newTokens.append(tokens[i])
    elif tokens[i] == "--":
        comment = False
        newTokens.append(tokens[i])
    elif (
        tokens[i][0] == '"'
        and tokens[i][-1] == '"'
        and len(tokens[i]) > 1
        and not buka
        and not type
        and not comment
    ):
        newTokens.append('"')
        newTokens.append('"')
    elif tokens[i] == ">" and not comment:
        buka = True
        newTokens.append(tokens[i])
    elif tokens[i] == "<" and not comment:
        buka = False
        newTokens.append(tokens[i])

    elif (tokens[i] == "type" or tokens[i] == "method") and not comment:
        type = True
        newTokens.append(tokens[i])
    elif tokens[i] == "=" and type and not comment:
        kutiptype = True
        newTokens.append(tokens[i])
    elif (
        tokens[i][0] == '"'
        and tokens[i][-1] == '"'
        and len(tokens[i]) > 1
        and kutiptype
        and not comment
    ):
        kutiptype = False
        type = False
        newTokens.append('"')
        temp = tokens[i].replace('"', "") + '"'
        newTokens.append(temp)
    elif not buka and not comment:
        newTokens.append(tokens[i])

if pda.process(newTokens):
    print_fancy(accept, font, green)
else:
    print_fancy(reject, font, red)
