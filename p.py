import re


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


states = {
    "q0",
    "q1",
    "q2",
    "q3",
    "q4",
    "q5",
    "q6",
    "q7",
    "q8",
    "q9",
    "q10",
    "11",
    "q12",
    "q13",
}
input_symbols = {
    "<",
    ">",
    "html",
    "/html",
    "id",
    "=",
    '"',
    "/head",
    "head",
    "class",
    "/body",
    "body",
}
stack_symbols = {"Z", "S"}
initial_state = "q0"
initial_stack_symbol = "Z"
final_states = {"q3"}
transition_function = {
    ("q0", "<", "Z"): ("q0", ["S", "Z"]),  # opening tag html
    ("q0", "html", "S"): ("q1", []),
    ("q1", ">", "Z"): ("q8", ["S", "Z"]),
    ("q1", "<", "S"): ("q2", []),  # closing tag html
    ("q2", "/html", "Z"): ("q2", ["S", "Z"]),
    ("q2", ">", "S"): ("q3", []),
    ("q3", "", "Z"): ("q3", []),
    #
    ("q1", "id", "Z"): ("q4", ["S", "Z"]),
    ("q1", "class", "Z"): ("q4", ["S", "Z"]),
    ("q1", "style", "Z"): ("q4", ["S", "Z"]),
    ("q4", "=", "S"): ("q5", []),
    ("q5", '"', "Z"): ("q5", ["S", "Z"]),
    ("q5", "", ""): ("q5", []),
    ("q5", '"', "S"): ("q1", []),
    #
    ("q8", "<", "S"): ("q6", []),
    ("q6", "head", "Z"): ("q6", ["S", "Z"]),
    ("q6", ">", "S"): ("q7", []),
    ("q7", "<", "Z"): ("q7", ["S", "Z"]),
    ("q7", "/head", "S"): ("q7", []),
    ("q7", ">", "Z"): ("q11", ["S", "Z"]),
    #
    ("q6", "id", "S"): ("q9", []),
    ("q6", "class", "S"): ("q9", []),
    ("q6", "style", "S"): ("q9", []),
    ("q9", "=", "Z"): ("q10", ["S", "Z"]),
    ("q10", '"', "S"): ("q10", []),
    ("q10", "", ""): ("q10", []),
    ("q10", '"', "Z"): ("q6", ["S", "Z"]),
    #
    ("q11", "<", "S"): ("q12", []),
    ("q12", "body", "Z"): ("q12", ["S", "Z"]),
    ("q12", ">", "S"): ("q13", []),
    ("q13", "<", "Z"): ("q13", ["S", "Z"]),
    ("q13", "/body", "S"): ("q13", []),
    ("q13", ">", "Z"): ("q1", ["S", "Z"]),
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

temp = input("Enter the string: ")
tokens = re.findall(r"/html|/head|/body|<|>|/|html|head|body|id|class|=|\"", temp)
print(tokens)
print(pda.process(tokens))
