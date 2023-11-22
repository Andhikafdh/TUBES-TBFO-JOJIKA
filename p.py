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


states = {"q0", "q1", "q2"}
input_symbols = {"<", ">"}
stack_symbols = {"Z", "S"}
initial_state = "q0"
initial_stack_symbol = "Z"
final_states = {"q2"}
transition_function = {
    ("q0", "<", "Z"): ("q0", ["S", "Z"]),
    # ("q0", "<", "S"): ("q0", ["S", "S"]),
    ("q0", ">", "S"): ("q0", []),
    ("q0", "", "Z"): ("q2", []),
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
print(pda.process(temp))
