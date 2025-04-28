from collections import defaultdict, deque

class NFA:
    def __init__(self, states, alphabet, transitions, initial, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial = initial
        self.finals = finals

class DFA:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = dict()
        self.initial = None
        self.finals = set()

def nfa_to_dfa(nfa):
    dfa = DFA()
    dfa.alphabet = nfa.alphabet

    def move(states, symbol):
        next_states = set()
        for state in states:
            if symbol in nfa.transitions.get(state, {}):
                next_states.update(nfa.transitions[state][symbol])
        return next_states

    start_set = frozenset([nfa.initial])
    queue = deque()
    queue.append(start_set)

    dfa.start_state = start_set
    dfa.states.add(start_set)
    dfa.transitions[start_set] = {}

    while queue:
        current_set = queue.popleft()
        dfa.transitions[current_set] = {}

        for symbol in nfa.alphabet:
            next_set = move(current_set, symbol)
            next_set_frozen = frozenset(next_set)
            if not next_set:
                continue

            if next_set_frozen not in dfa.states:
                dfa.states.add(next_set_frozen)
                queue.append(next_set_frozen)

            dfa.transitions[current_set][symbol] = next_set_frozen

    for state_set in dfa.states:
        if any(state in nfa.finals for state in state_set):
            dfa.finals.add(state_set)

    return dfa


def shunt(regex):
    operators = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
    associativity = {'*': 'L', '+': 'L', '?': 'L', '.': 'L', '|': 'L'}
    postfix = ''
    stack = []

    # Add explicit concatenation
    new_regex = ''
    prev = None
    for c in regex:
        if prev is not None:
            if (prev not in '(|' and c not in '|)*+?)'):
                new_regex += '.'
        new_regex += c
        prev = c

    for c in new_regex:
        if c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            if stack:
                stack.pop()
        elif c in operators:
            while stack and stack[-1] != '(' and (operators[c] < operators[stack[-1]] or
                                                  (operators[c] == operators[stack[-1]] and associativity[c] == 'L')):
                postfix += stack.pop()
            stack.append(c)
        else:
            postfix += c
    while stack:
        postfix += stack.pop()
    return postfix


class state:
    label = None
    edge1 = None
    edge2 = None


class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pofix):
    nfaStack = []

    for c in pofix:
        if c == '?':
            nfa1 = nfaStack.pop()
            initial = state()
            accept = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            nfa1.accept.edge1 = accept
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        elif c == '+':
            nfa1 = nfaStack.pop()
            initial = nfa1.initial
            accept = state()
            nfa1.accept.edge1 = initial
            nfa1.accept.edge2 = accept
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)

        elif c == '*':
            nfa1 = nfaStack.pop()
            initial = state()
            accept = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        elif c == '.':
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            nfa1.accept.edge1 = nfa2.initial
            newNFA = nfa(nfa1.initial, nfa2.accept)
            nfaStack.append(newNFA)
        elif c == '|':
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        else:
            accept = state()
            initial = state()
            initial.label = c
            initial.edge1 = accept
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
    return nfaStack.pop()


def followArrowE(state, visited=None):
    if visited is None:
        visited = set()
    states = set()
    if state not in visited:
        visited.add(state)
        states.add(state)
        if state.label is None:
            if state.edge1 is not None:
                states |= followArrowE(state.edge1, visited)
            if state.edge2 is not None:
                states |= followArrowE(state.edge2, visited)
    return states


def match(infix, string):
    postfix = shunt(infix)
    nfa = compile(postfix)
    currentState = set()
    nextState = set()
    currentState |= followArrowE(nfa.initial)
    for s in string:
        for c in currentState:
            if c.label == s:
                nextState |= followArrowE(c.edge1)
        currentState = nextState
        nextState = set()
    return (nfa.accept in currentState)

import json

def load_tests(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def run_tests(tests):
    for test in tests:
        name = test['name']
        regex = test['regex']
        print(f"Running tests for regex: {name} -> {regex}")

        for case in test['test_strings']:
            string = case['input']
            expected = case['expected']
            result = match(regex, string)
            if result == expected:
                print(f"  [OK] Input: '{string}' -> Expected: {expected}, Got: {result}")
            else:
                print(f"  [FAIL] Input: '{string}' -> Expected: {expected}, Got: {result}")
        print()


if __name__ == "__main__":
    tests = load_tests('tests.json')  # path to your JSON test file
    run_tests(tests)

