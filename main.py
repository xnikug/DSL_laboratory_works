class Grammar:
    def __init__(self, non_terminals, terminals, rules, start):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start = start

    def print_rules(self):
        for non_terminal in self.rules:
            print(f'{non_terminal} -> {" | ".join(self.rules[non_terminal])}')
        print()


    def is_cnf_form(self):
        for non_terminal in self.rules:
            for production in self.rules[non_terminal]:
                if len(production) == 0 or len(production) > 2:
                    return False
                if len(production) == 1 and production not in self.terminals:
                    return False
                if len(production) == 2 and any(symbol in self.terminals for symbol in production):
                    return False

        return True

    def eliminate_e_productions(self):
        nullable = set()

        # Find all nullable non-terminals
        for non_terminal in self.non_terminals:
            for production in self.rules[non_terminal]:
                if production == 'ε':
                    nullable.add(non_terminal)

        # Check for indirect nullable non-terminals
        changes = True
        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                if non_terminal not in nullable:
                    for production in self.rules[non_terminal]:
                        if all(symbol in nullable for symbol in production):
                            nullable.add(non_terminal)
                            changes = True
                            break

        # Eliminate epislon-productions
        new_rules = {}
        for non_terminal in self.rules:
            new_prods = []
            for production in self.rules[non_terminal]:
                if production != 'ε':
                    new_prods.extend(self._expand_nullable_prod(production, nullable))
            new_rules[non_terminal] = list(set(new_prods))

        self.rules = new_rules

    def _expand_nullable_prod(self, production, nullable):
        expansions = ['']

        for symbol in production:
            new_expansions = []
            if symbol in nullable:
                for expansion in expansions:
                    new_expansions.append(expansion + symbol)
                    new_expansions.append(expansion)
            else:
                for expansion in expansions:
                    new_expansions.append(expansion + symbol)
            expansions = new_expansions

        return [expansion for expansion in expansions if expansion]

    def eliminate_unit_prod(self):
        # Remove unit productions from grammar
        changes = True
        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                unit_productions = [prod for prod in self.rules[non_terminal] if prod in self.non_terminals]
                for unit in unit_productions:
                    new_productions = self.rules[unit]
                    if new_productions:
                        self.rules[non_terminal].extend(new_productions)
                        self.rules[non_terminal].remove(unit)
                        self.rules[non_terminal] = list(set(self.rules[non_terminal]))
                        changes = True

                self.rules[non_terminal] = [prod for prod in self.rules[non_terminal] if prod not in self.non_terminals]

    def eliminate_inaccessible_symbols(self):
        accessible = {self.start}
        flag = True 
        old_rules = self.rules.copy()

        while flag:
            flag = False
            for non_terminal in accessible.copy():
                for production in self.rules[non_terminal]:
                    for symbol in production:
                        if symbol in self.non_terminals and symbol not in accessible:
                            accessible.add(symbol)
                            flag = True

        self.non_terminals = list(accessible)
        self.rules = {nt: old_rules[nt] for nt in accessible}

    def eliminate_non_productive_symbols(self):
        productive = {self.start}
        changes = True

        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                if non_terminal not in productive:
                    for production in self.rules[non_terminal]:
                        if all(symbol in self.terminals or symbol in productive for symbol in production):
                            productive.add(non_terminal)
                            changes = True
                            break

        self.non_terminals = list(productive)

        # Dictionary to store the rules
        updated_rules = {}
        for nt in productive:
            productive_rules = []

            for production in self.rules[nt]:
                if all(symbol in self.terminals or symbol in productive for symbol in production):
                    productive_rules.append(production)

            updated_rules[nt] = productive_rules

        self.rules = updated_rules

    def _create_new_non_terminal(self):
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        for letter in alphabet:
            if letter not in self.non_terminals:
                self.non_terminals.append(letter)
                return letter

        for letter in alphabet:
            for num in range(10):
                new_symbol = f'{letter}{num}'
                if new_symbol not in self.non_terminals:
                    self.non_terminals.append(new_symbol)
                    return new_symbol


# Variant 21
if __name__ == '__main__':
    non_terminals = ['S', 'A', 'B', 'C', 'D']
    terminals = ['a', 'b', 'd']
    rules = {
        'S': ['dB', 'AC'],
        'A': ['d', 'dS', 'aBdB'],
        'B': ['a', 'aA', 'AC'],
        'C': ['bC', 'ε'],
        'D': ['ab']
    }
    grammar = Grammar(non_terminals, terminals, rules, 'S')
    if grammar.is_cnf_form():
        print("The grammar is in Chomsky Normal Form Already")

    grammar.eliminate_e_productions()
    print('1) Elimination of epsilon productions:')
    grammar.print_rules()

    grammar.eliminate_unit_prod()
    print('2) Elimination of unit productions:')
    grammar.print_rules()

    grammar.eliminate_inaccessible_symbols()
    print('3) Elimination of inaccessible symbols:')
    grammar.print_rules()

    print('4) Elimination of non-productive symbols:')
    grammar.print_rules()

    rhs_to_non_terminal = {}
    old_non_terminals = list(grammar.rules)

    new_rules = {}
    for non_terminal in list(grammar.rules):
        new_rules[non_terminal] = set()
        for production in grammar.rules[non_terminal]:
            # Case for productions with more than 2 symbols
            while len(production) > 2:
                # Extract the first two symbols
                first_two_symbols = production[:2]

                if first_two_symbols in rhs_to_non_terminal:
                    new_non_terminal = rhs_to_non_terminal[first_two_symbols]
                else:
                    new_non_terminal = grammar._create_new_non_terminal()
                    new_rules[new_non_terminal] = {first_two_symbols}
                    rhs_to_non_terminal[first_two_symbols] = new_non_terminal
                # Replace the first two symbols with the new non-terminal
                production = new_non_terminal + production[2:]

            new_rules[non_terminal].add(production)

    # Handle mixed productions
    for non_terminal, productions in list(new_rules.items()):
        temp_productions = productions.copy()
        for production in temp_productions:
            if len(production) == 2 and any(symbol in grammar.terminals for symbol in production):
                new_production = []
                for symbol in production:
                    if symbol in grammar.terminals:
                        if symbol in rhs_to_non_terminal:
                            new_non_terminal = rhs_to_non_terminal[symbol]
                        else:
                            new_non_terminal = grammar._create_new_non_terminal()
                            new_rules[new_non_terminal] = {symbol}
                            rhs_to_non_terminal[symbol] = new_non_terminal
                        new_production.append(new_non_terminal)
                    else:
                        new_production.append(symbol)
                productions.remove(production)
                productions.add(''.join(new_production))

    grammar.rules = {nt: new_rules[nt] for nt in old_non_terminals + list(set(new_rules) - set(old_non_terminals))}

    print('Conversion to Chomsky Normal Form:')
    grammar.print_rules()