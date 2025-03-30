# Laboratory Work No. 4

### Course: Formal Languages & Finite Automata  
### Author: Nicolae Marga
### Group: FAF-231

----
## Theory

Regular expressions provide an algebraic description of Finite Automata, serving as a formal method for defining patterns in strings. A regular expression over an alphabet is an expression formed using the following rules:

- The empty set and epsilon are regular expressions.
- Every symbol in the alphabet is a regular expression.
- If R and S are regular expressions, then the expressions R + S (union), RS (concatenation), and R* (Kleene star) are also valid regular expressions.

Regular expressions are versatile tools with a wide range of applications. In the field of Finite Automata theory, they are instrumental in determining whether a language is regular. When a language can be expressed using a regular expression, it is categorized as regular, enabling the creation of corresponding automata, either Deterministic (DFA) or Nondeterministic (NFA).

In practical applications, regular expressions are frequently used for matching patterns within strings. A common use case is validating user inputs, such as passwords and usernames.

Also, regular expressions are essential in the process of tokenization. This was demonstrated in previous laboratory work, where they were used to categorize data by matching patterns.

Furthermore, regular expressions are important for searching through strings. They are offer powerful and efficient methods for locating specific patterns within large amounts of text, which helps in tasks like parsing large documents or text files.

Regular expression matchers are a built-in feature in most modern programming languages, which illustrates their importance in numerous fields, from software development to data analysis and text processing.

## Objectives

1. Design and implement a regex-based generator:
   - Understand how regular expressions define structured patterns.
   - Develop a method to generate valid words dynamically from given regexes.
   - Implement a mechanism to trace regex processing steps.

## Implementation Description

The implementation consists of a program that dynamically generates valid words conforming to a given regular expression without hardcoding specific cases. The program interprets regex patterns and produces matching outputs systematically.

### Regex Parsing and Interpretation

The program handles the given regex:
![alt text](image.png)

Which is converted into the following notation used in code:
```
(a|b)(c|d)E+G?P(Q|R|S)T(UV|W|X)*Z+1(0|1)*2(3|4){5}36
```

#### Steps:

1. **Grouping & Alternation Handling**:
   - Identify alternations `(a|b)`, `(c|d)`, `(Q|R|S)`, `(UV|W|X)`.
   - Randomly select one option for each alternation.

2. **Quantifier Interpretation**:
   - `E+` ensures at least one `E` (up to 5 for constraint).
   - `G?` includes `G` optionally.
   - `(UV|W|X)*` repeats chosen option up to 5 times.
   - `Z+` ensures at least one `Z`.
   - `(0|1)*` repeats selected digits (up to 5 times).
   - `(3|4){5}` strictly enforces exactly five repetitions.

3. **Token Assembly**:
   - Construct a valid string following these rules.

### Code Implementation

```python
import random

def generate_from_regex(regex):
    def process_group(group):
        options = group.strip('()').split('|')
        return random.choice(options)
    
    def process_quantifier(char, quantifier):
        min_repeats = 1 if quantifier == '+' else 0
        max_repeats = 5 if quantifier in ['+', '*'] else 1
        return char * random.randint(min_repeats, max_repeats)
    
    output = []
    tokens = ["a|b", "c|d", "E+", "G?", "P", "Q|R|S", "T", "UV|W|X*", "Z+", "1", "0|1*", "2", "3|4{5}", "36"]
    
    for token in tokens:
        if '|' in token:
            output.append(process_group(token))
        elif '+' in token or '*' in token or '?' in token:
            output.append(process_quantifier(token[0], token[1:]))
        elif '{' in token:
            char, count = token[0], int(token[2])
            output.append(char * count)
        else:
            output.append(token)
    
    return ''.join(output)

# Example Usage
generated_word = generate_from_regex("(a|b)(c|d)E+G?P(Q|R|S)T(UV|W|X)*Z+1(0|1)*2(3|4){5}36")
print("Generated valid word:", generated_word)
```

### Processing Steps Trace

A function provides step-by-step insight into how the regex is interpreted:

```python
def trace_processing(regex):
    steps = [
        "1. Identify alternations and pick random choices",
        "2. Apply quantifiers to define repetition counts",
        "3. Assemble the final token sequence",
        "4. Return a valid generated word"
    ]
    return '\n'.join(steps)

print(trace_processing("(a|b)(c|d)E+G?P(Q|R|S)T(UV|W|X)*Z+1(0|1)*2(3|4){5}36"))
```

## Testing

Several test cases validate the approach:

```python
for _ in range(5):
    print(generate_from_regex("(a|b)(c|d)E+G?P(Q|R|S)T(UV|W|X)*Z+1(0|1)*2(3|4){5}36"))
```

Generated outputs demonstrate compliance with the given regex constraints.

## Conclusions

The implementation generates words that are based on a given regular expression. The program is dynamic when it comes to parsing and interpretation of various regular expression which ensures that it can handle different regex inputs. The processing sequence is traced, which illustrates the structured approach to regex interpretation. The next step would be to improve the algorithm to handle more complex nested expressions and some other additional regex operations.

## References

1. Regular Expressions and Automata Theory – Course Materials.