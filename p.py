import re
import sys


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

        # Check if we can transition to a final state with an empty string as the input symbol
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
    # for line in lines[6:]:
    #     transition = line.replace("\n", "").split(" ")
    #     if transition[1] == "e":
    #         transition[1] = ""
    #     if transition[2] == "e":
    #         transition[2] = ""
    #     if transition[4] == "e":
    #         transition[4] = []
    #     transition_function[(transition[0], transition[1], transition[2])] = (
    #         transition[3],
    #         list(transition[4]),
    #     )
file.close()

fileHTML = open(pathFileHTML, "r")
isiHTML = fileHTML.read()
isiHTML = isiHTML.replace("\n", "").replace("    ", "")
fileHTML.close()


# states = {
#     "q0",
#     "q1",
#     "q2",
#     "q3",
#     "q4",
#     "q5",
#     "q6",
#     "q7",
#     "q8",
#     "q9",
#     "q10",
#     "11",
#     "q12",
#     "q13",
# }
# input_symbols = {
#     "<",
#     ">",
#     "html",
#     "/html",
#     "id",
#     "=",
#     '"',
#     "/head",
#     "head",
#     "class",
#     "/body",
#     "body",
# }
# stack_symbols = {"Z", "S"}
# initial_state = "q0"
# initial_stack_symbol = "Z"
# final_states = {"q3"}
transition_function = {
    ("q0", "<", "Z"): ("q0", ["S", "Z"]),  # opening tag html
    ("q0", "html", "S"): ("q1", []),
    ("q1", ">", "Z"): ("q8", ["S", "Z"]),
    ("q1", "<", "S"): ("q2", []),  # closing tag html
    ("q2", "/html", "Z"): ("q2", ["S", "Z"]),
    ("q2", ">", "S"): ("q3", []),
    ("q3", "", "Z"): ("q3", []),
    # ^ done
    ("q1", "id", "Z"): ("q4", ["S", "Z"]),
    ("q1", "class", "Z"): ("q4", ["S", "Z"]),
    ("q1", "style", "Z"): ("q4", ["S", "Z"]),
    ("q4", "=", "S"): ("q5", []),
    ("q5", '"', "Z"): ("q5", ["S", "Z"]),
    ("q5", "", ""): ("q5", []),
    ("q5", '"', "S"): ("q1", []),
    # ^ done
    ("q8", "<", "S"): ("q6", []),
    ("q6", "head", "Z"): ("q6", ["S", "Z"]),
    ("q6", ">", "S"): ("q7", []),
    ("q7", "<", "Z"): ("q7", ["S", "Z"]),
    ("q7", "/head", "S"): ("q7", []),
    ("q7", ">", "Z"): ("q11", ["S", "Z"]),
    # ^ done
    ("q6", "id", "S"): ("q9", []),
    ("q6", "class", "S"): ("q9", []),
    ("q6", "style", "S"): ("q9", []),
    ("q9", "=", "Z"): ("q10", ["S", "Z"]),
    ("q10", '"', "S"): ("q10", []),
    ("q10", "", ""): ("q10", []),
    ("q10", '"', "Z"): ("q6", ["S", "Z"]),
    # ^ done
    ("q11", "<", "S"): ("q12", []),
    ("q12", "body", "Z"): ("q12", ["S", "Z"]),
    ("q12", ">", "S"): ("q13", []),
    ("q13", "<", "Z"): ("q13", ["S", "Z"]),
    ("q13", "/body", "S"): ("q13", []),
    ("q13", ">", "Z"): ("q1", ["S", "Z"]),
    # ^ done
    ("q12", "id", "S"): ("q14", []),
    ("q12", "class", "S"): ("q14", []),
    ("q12", "style", "S"): ("q14", []),
    ("q14", "=", "Z"): ("q15", ["S", "Z"]),
    ("q15", '"', "S"): ("q15", []),
    ("q15", "", ""): ("q15", []),
    ("q15", '"', "Z"): ("q12", ["S", "Z"]),
    # ^ done
    ("q7", "title", "S"): ("q16", []),
    ("q16", ">", "Z"): ("q17", ["S", "Z"]),
    ("q17", "<", "S"): ("q17", []),
    ("q17", "/title", "Z"): ("q18", ["S", "Z"]),
    ("q18", ">", "S"): ("q7", []),
    # ^ done
    ("q16", "id", "Z"): ("q19", ["S", "Z"]),
    ("q16", "class", "Z"): ("q19", ["S", "Z"]),
    ("q16", "style", "Z"): ("q19", ["S", "Z"]),
    ("q19", "=", "S"): ("q20", []),
    ("q20", '"', "Z"): ("q20", ["S", "Z"]),
    ("q20", "", ""): ("q20", []),
    ("q20", '"', "S"): ("q16", []),
    # ^ done
    ("q7", "link", "S"): ("q21", []),
    ("q21", "rel", "Z"): ("q22", ["S", "Z"]),
    ("q22", "=", "S"): ("q23", []),
    ("q23", '"', "Z"): ("q23", ["S", "Z"]),
    ("q23", "", ""): ("q23", []),
    ("q23", '"', "S"): ("q24", []),
    ("q24", "/", "Z"): ("q25", ["S", "Z"]),
    ("q25", ">", "S"): ("q7", []),
    # ^ pending
    ("q24", "id", "Z"): ("q26", ["S", "Z"]),
    ("q24", "class", "Z"): ("q26", ["S", "Z"]),
    ("q24", "style", "Z"): ("q26", ["S", "Z"]),
    ("q24", "href", "Z"): ("q26", ["S", "Z"]),
    ("q26", "=", "S"): ("q27", []),
    ("q27", '"', "Z"): ("q27", ["S", "Z"]),
    ("q27", "", ""): ("q27", []),
    ("q27", '"', "S"): ("q24", []),
    # ^ pending
    ("q21", "id", "Z"): ("q28", ["S", "Z"]),
    ("q21", "class", "Z"): ("q28", ["S", "Z"]),
    ("q21", "style", "Z"): ("q28", ["S", "Z"]),
    ("q21", "href", "Z"): ("q28", ["S", "Z"]),
    ("q28", "=", "S"): ("q29", []),
    ("q29", '"', "Z"): ("q29", ["S", "Z"]),
    ("q29", "", ""): ("q29", []),
    ("q29", '"', "S"): ("q21", []),
    # ^ pending revisi
    ("q7", "script", "S"): ("q30", []),
    ("q30", ">", "Z"): ("q31", ["S", "Z"]),
    ("q31", "<", "S"): ("q31", []),
    ("q31", "/script", "Z"): ("q31", ["S", "Z"]),
    ("q31", ">", "S"): ("q7", []),
    # ^ pending revisi
    ("q30", "id", "Z"): ("q32", ["S", "Z"]),
    ("q30", "class", "Z"): ("q32", ["S", "Z"]),
    ("q30", "style", "Z"): ("q32", ["S", "Z"]),
    ("q30", "src", "Z"): ("q32", ["S", "Z"]),
    ("q32", "=", "S"): ("q33", []),
    ("q33", '"', "Z"): ("q33", ["S", "Z"]),
    ("q33", "", ""): ("q33", []),
    ("q33", '"', "S"): ("q30", []),
    # ^ pending revisi
    ("q13", "script", "S"): ("q34", []),
    ("q34", ">", "Z"): ("q35", ["S", "Z"]),
    ("q35", "<", "S"): ("q35", []),
    ("q35", "/script", "Z"): ("q35", ["S", "Z"]),
    ("q35", ">", "S"): ("q13", []),
    # ^ pending
    ("q34", "id", "Z"): ("q36", ["S", "Z"]),
    ("q34", "class", "Z"): ("q36", ["S", "Z"]),
    ("q34", "style", "Z"): ("q36", ["S", "Z"]),
    ("q34", "src", "Z"): ("q36", ["S", "Z"]),
    ("q36", "=", "S"): ("q37", []),
    ("q37", '"', "Z"): ("q37", ["S", "Z"]),
    ("q37", "", ""): ("q37", []),
    ("q37", '"', "S"): ("q34", []),
    # ^ pending
    ("q13", "h1", "S"): ("q38", []),
    ("q38", ">", "Z"): ("q39", ["S", "Z"]),
    ("q39", "<", "S"): ("q39", []),
    ("q39", "/h1", "Z"): ("q39", ["S", "Z"]),
    ("q39", ">", "S"): ("q13", []),
    # ^ pending
    ("q38", "id", "Z"): ("q40", ["S", "Z"]),
    ("q38", "class", "Z"): ("q40", ["S", "Z"]),
    ("q38", "style", "Z"): ("q40", ["S", "Z"]),
    ("q40", "=", "S"): ("q41", []),
    ("q41", '"', "Z"): ("q41", ["S", "Z"]),
    ("q41", "", ""): ("q41", []),
    ("q41", '"', "S"): ("q38", []),
    # ^ pending
    ("q13", "h2", "S"): ("q42", []),
    ("q42", ">", "Z"): ("q43", ["S", "Z"]),
    ("q43", "<", "S"): ("q43", []),
    ("q43", "/h2", "Z"): ("q43", ["S", "Z"]),
    ("q43", ">", "S"): ("q13", []),
    # ^ pending
    ("q42", "id", "Z"): ("q44", ["S", "Z"]),
    ("q42", "class", "Z"): ("q44", ["S", "Z"]),
    ("q42", "style", "Z"): ("q44", ["S", "Z"]),
    ("q44", "=", "S"): ("q45", []),
    ("q45", '"', "Z"): ("q45", ["S", "Z"]),
    ("q45", "", ""): ("q45", []),
    ("q45", '"', "S"): ("q42", []),
    # ^ pending
    ("q13", "h3", "S"): ("q46", []),
    ("q46", ">", "Z"): ("q47", ["S", "Z"]),
    ("q47", "<", "S"): ("q47", []),
    ("q47", "/h3", "Z"): ("q47", ["S", "Z"]),
    ("q47", ">", "S"): ("q13", []),
    # ^ pending
    ("q46", "id", "Z"): ("q48", ["S", "Z"]),
    ("q46", "class", "Z"): ("q48", ["S", "Z"]),
    ("q46", "style", "Z"): ("q48", ["S", "Z"]),
    ("q48", "=", "S"): ("q49", []),
    ("q49", '"', "Z"): ("q49", ["S", "Z"]),
    ("q49", "", ""): ("q49", []),
    ("q49", '"', "S"): ("q46", []),
    # ^ pending
    ("q13", "h4", "S"): ("q50", []),
    ("q50", ">", "Z"): ("q51", ["S", "Z"]),
    ("q51", "<", "S"): ("q51", []),
    ("q51", "/h4", "Z"): ("q51", ["S", "Z"]),
    ("q51", ">", "S"): ("q13", []),
    # ^ pending
    ("q50", "id", "Z"): ("q52", ["S", "Z"]),
    ("q50", "class", "Z"): ("q52", ["S", "Z"]),
    ("q50", "style", "Z"): ("q52", ["S", "Z"]),
    ("q52", "=", "S"): ("q53", []),
    ("q53", '"', "Z"): ("q53", ["S", "Z"]),
    ("q53", "", ""): ("q53", []),
    ("q53", '"', "S"): ("q50", []),
    # ^ pending
    ("q13", "h5", "S"): ("q54", []),
    ("q54", ">", "Z"): ("q55", ["S", "Z"]),
    ("q55", "<", "S"): ("q55", []),
    ("q55", "/h5", "Z"): ("q55", ["S", "Z"]),
    ("q55", ">", "S"): ("q13", []),
    # ^ pending
    ("q54", "id", "Z"): ("q56", ["S", "Z"]),
    ("q54", "class", "Z"): ("q56", ["S", "Z"]),
    ("q54", "style", "Z"): ("q56", ["S", "Z"]),
    ("q56", "=", "S"): ("q57", []),
    ("q57", '"', "Z"): ("q57", ["S", "Z"]),
    ("q57", "", ""): ("q57", []),
    ("q57", '"', "S"): ("q54", []),
    # ^ pending
    ("q13", "h6", "S"): ("q58", []),
    ("q58", ">", "Z"): ("q59", ["S", "Z"]),
    ("q59", "<", "S"): ("q59", []),
    ("q59", "/h6", "Z"): ("q59", ["S", "Z"]),
    ("q59", ">", "S"): ("q13", []),
    # ^ pending
    ("q58", "id", "Z"): ("q60", ["S", "Z"]),
    ("q58", "class", "Z"): ("q60", ["S", "Z"]),
    ("q58", "style", "Z"): ("q60", ["S", "Z"]),
    ("q60", "=", "S"): ("q61", []),
    ("q61", '"', "Z"): ("q61", ["S", "Z"]),
    ("q61", "", ""): ("q61", []),
    ("q61", '"', "S"): ("q58", []),
    # ^ pending
}


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
print(isiHTML)
tokens = re.findall(
    r'/html|/head|/body|/title|/link|/script|/h1|/h2|/h3|/h4|/h5|/h6|<|>|/|html|head|body|link|title|id|class|style|rel|href|script|src|h1|h2|h3|h4|h5|h6|=|"[^"]*"',
    isiHTML,
)
newTokens = []
for i in range(len(tokens)):
    if tokens[i][0] == '"' and tokens[i][-1] == '"' and len(tokens[i]) > 1:
        newTokens.append('"')
        newTokens.append('"')
    else:
        newTokens.append(tokens[i])

print(newTokens)
# print(states)
# print(input_symbols)
# print(stack_symbols)
# print(initial_state)
# print(initial_stack_symbol)
# print(final_states)
# for transition in transition_function:
#     print(transition, end=": ")
#     print(transition_function.get(transition))
if pda.process(newTokens):
    print("Accepted")
else:
    print("Syntax Error")
