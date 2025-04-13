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