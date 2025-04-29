#Pirvulescu Gabriela - Tema 2 LFA
from collections import deque
import json

class NFA:   #clasa NFA
    def __init__(self, states, alphabet, transitions, initial, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial = initial
        self.finals = finals

class DFA:     #clasa DFA
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = dict()
        self.initial = None
        self.finals = set()
        self.start_state = None

def Shunting_Yard(regex):     #functia Shunting-Yard: regex -> postfix
    operators = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
    associativity = {'*': 'L', '+': 'L', '?': 'L', '.': 'L', '|': 'L'}
    postfix = ''
    stack = []   #lista ce simuleaza un stack
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

class state:   #clasa de stare -> o folosim in thompson
    label = None
    edge1 = None
    edge2 = None

class nfa:
    initial = None
    accept = None
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def thompson(postfix):  #facem algoritm thompson: postfix -> nfa (scris cu states)
    nfaStack = []
    for c in postfix:
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

def create_nfa(nfa_thompson):   #cream un nfa de forma clasica: (Q, S, d, qi, F)
    states = set()
    transitions = {}
    alphabet = set()
    state_id_map = {}
    def collect_states(s, visited=set()):
        if s in visited:
            return
        visited.add(s)
        sid = id(s)
        state_id_map[s] = sid
        states.add(sid)
        if s.label is not None:
            alphabet.add(s.label)
            transitions.setdefault(sid, {}).setdefault(s.label, []).append(id(s.edge1))
            collect_states(s.edge1, visited)
        else:
            if s.edge1:
                transitions.setdefault(sid, {}).setdefault('', []).append(id(s.edge1))
                collect_states(s.edge1, visited)
            if s.edge2:
                transitions.setdefault(sid, {}).setdefault('', []).append(id(s.edge2))
                collect_states(s.edge2, visited)
    collect_states(nfa_thompson.initial)
    return NFA(
        states=states,
        alphabet=alphabet,
        transitions=transitions,
        initial=id(nfa_thompson.initial),
        finals={id(nfa_thompson.accept)}
    )

def nfa_to_dfa(nfa):   #subset construction -> transformarea nfa -> dfa
    dfa = DFA()
    dfa.alphabet = nfa.alphabet
    def move(states, symbol):
        next_states = set()
        for state in states:
            if symbol in nfa.transitions.get(state, {}):
                next_states.update(nfa.transitions[state][symbol])
        return next_states
    def lambda_closure(states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for next_state in nfa.transitions.get(state, {}).get('', []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure
    start_set = frozenset(lambda_closure({nfa.initial}))
    dfa.start_state = start_set
    dfa.states.add(start_set)
    dfa.transitions[start_set] = deque()
    queue = deque([start_set])
    while queue:
        current_set = queue.popleft()
        dfa.transitions[current_set] = {}
        for symbol in nfa.alphabet:
            move_set = move(current_set, symbol)
            closure = lambda_closure(move_set)
            frozen_closure = frozenset(closure)
            if not closure:
                continue
            if frozen_closure not in dfa.states:
                dfa.states.add(frozen_closure)
                queue.append(frozen_closure)
            dfa.transitions[current_set][symbol] = frozen_closure
    for state_set in dfa.states:
        if any(s in nfa.finals for s in state_set):
            dfa.finals.add(state_set)
    return dfa

def dfa_acceptance_check(dfa, string):    #validator cuvinte in DFA (ca la tema 1)
    current_state = dfa.start_state
    for symbol in string:
        if symbol not in dfa.alphabet:
            return False
        current_state = dfa.transitions.get(current_state, {}).get(symbol)
        if current_state is None:
            return False
    return current_state in dfa.finals

def match(regex, string):    #se verifica acceptarea unui string pentru un regex dat
    postfix = Shunting_Yard(regex)
    nfa_thompson = thompson(postfix)
    nfa_structured = create_nfa(nfa_thompson)
    dfa = nfa_to_dfa(nfa_structured)
    return dfa_acceptance_check(dfa, string)

def load_tests(filename):    #load teste din json
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def run_tests(tests):    #run teste din json
    for test in tests:
        name = test['name']
        regex = test['regex']
        print(f"Running tests for regex: {name} -> {regex}")
        for case in test['test_strings']:
            string = case['input']
            expected = case['expected']
            result = match(regex, string)   #True or False -> in fucntie de acceptare sau nu a cuv
            if result == expected:  #noi vrem expected = rezultatul nostru
                print(f"  [OK] Input: '{string}' -> Expected: {expected}, Got: {result}")
            else:
                print(f"  [FAIL] Input: '{string}' -> Expected: {expected}, Got: {result}")
        print()

if __name__ == "__main__":
    tests = load_tests('tests.json')
    run_tests(tests)
