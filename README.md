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

Write and cover what regular expressions are, what they are used for;

a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown). Be careful that idea is to interpret the given regular expressions dinamycally, not to hardcode the way it will generate valid strings. You give a set of regexes as input and get valid word as an output

b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

c. Bonus point: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)

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
def parse_regex(regex):
    """Parses the regex dynamically and generates a valid matching string."""
    steps = []
    i = 0
    result = ""
    chosen = ""

    def choose(options):
        return random.choice(options.split("|"))

    while i < len(regex):
        char = regex[i]
        if char == "(":
            # Extract group content
            end_idx = regex.find(")", i)
            group_content = regex[i + 1:end_idx]
            chosen = choose(group_content)
            result += chosen
            steps.append(f"Choose from ({group_content}) → {chosen}")
            i = end_idx  # Move to closing )
            #print(result)
        elif char == "+":
            # Repeat previous character at least once, up to 5 times
            repeated = chosen * random.randint(1, 5)
            result += repeated
            steps.append(f"Repeat '{chosen}' (1-5 times) → {repeated}")

        elif char == "?":
            # Previous character is optional
            if random.choice([True, False]):
                steps.append(f"Optional '{chosen}' → Kept")
            else:
                steps.append(f"Optional '{chosen}' → Removed")
                result = result[:-1]  # Remove last character

        elif char == "*":
            # Repeat previous character 0 to 5 times
            repeated = chosen * random.randint(0, 5)
            result += repeated
            steps.append(f"Repeat '{chosen}' (0-5 times) → {repeated}")
            
        elif char == "{":
            # Handle {n} repetitions
            end_idx = regex.find("}", i)
            repeat_count = int(regex[i + 1:end_idx])
            repeated = result[-1] * (repeat_count - 1)  # -1 since already added
            result += repeated
            steps.append(f"Repeat '{result[-1]}' {repeat_count} times → {repeated}")
            i = end_idx  # Move past }

        else:
            # Normal character, just append it
            result += char
            steps.append(f"Append '{char}' → {char}")
            chosen = char
        i += 1  # Move to next character

    return result, steps
```
The parse_regex function dynamically processes a given regular expression and generates a valid matching string by following the regex rules. It loops through each sequence of characters in the regex string and identifies different components like groups (enclosed in parentheses), quantifiers (+, ?, *, {n}), and literal characters. The function randomly chooses one of the options in the alternation (e.g., (a|b)), and for quantifiers, it repeats the selected character according to the specified rule (e.g., + for 1-5 times, ? for optional, and * for 0-5 times). The function also keeps track of each processing step and appends the corresponding string to the result.

### Processing Steps Trace

The parse_regex function also provides the steps of how the regex is interpreted. And it is interpreted the following way:

1. Identify alternations and pick random choices
2. Apply quantifiers to define repetition counts
3. Assemble the final token sequence
4. Return a valid generated word

## Testing

Several test cases validate the approach:

```python
    # Given regex
    regex = "(a|b)(c|d)E+G?P(Q|R|S)T(UV|W|X)*Z+1(0|1)*2(3|4){5}36"

    # Generate a valid string and show steps
    valid_string, process_steps = parse_regex(regex)
```

Generated outputs showcases the expected output matching with the given regex constraints.

![alt text](image-1.png)

![alt text](image-2.png)
## Conclusions

The implementation generates words that are based on a given regular expression. The program is dynamic when it comes to parsing and interpretation of various regular expression which ensures that it can handle different regex inputs. The processing sequence is traced, which illustrates the structured approach to regex interpretation. The next step would be to improve the algorithm to handle more complex nested expressions and some other additional regex operations.

## References

1. Regular Expressions and Automata Theory – Course Materials.