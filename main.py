import random
import re

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
def match_string(test_string, regex):
    """Matches the generated string against the regex."""
    if re.fullmatch(regex, test_string):
        return f"'{test_string}' matches the regex."
    else:
        return f"'{test_string}' does NOT match the regex."
if __name__ == "__main__":
    # Given regex
    regex = "(a|b)(c|d)E+G?P(Q|R|S)T(UV|W|X)*Z+1(0|1)*2(3|4){5}36"

    # Generate a valid string and show steps
    valid_string, process_steps = parse_regex(regex)

    # Display results
    print("Generated String:", valid_string)
    print("\nProcessing Steps:")
    for step in process_steps:
        print(step)
        
    print("Some valid strings:")
    for i in range(5):
        valid_string, process_steps = parse_regex(regex)
        print(match_string(valid_string, regex))
    print("Some invalid strings:")
    invalid_string = "bdRVUVUVUS46"
    print(match_string(invalid_string, regex))
    invalid_string = "acRVVVVVTS36"
    print(match_string(invalid_string, regex))
    invalid_string = "acEE36"
    print(match_string(invalid_string, regex))