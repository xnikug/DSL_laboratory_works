import random

def parse_regex(regex):
    """Parses the regex dynamically and generates a valid matching string."""
    steps = []
    i = 0
    result = ""

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

        elif char == "+":
            # Repeat previous character at least once, up to 5 times
            repeated = result[-1] * random.randint(1, 5)
            result += repeated
            steps.append(f"Repeat '{result[-1]}' (1-5 times) → {repeated}")

        elif char == "?":
            # Previous character is optional
            if random.choice([True, False]):
                steps.append(f"Optional '{result[-1]}' → Kept")
            else:
                steps.append(f"Optional '{result[-1]}' → Removed")
                result = result[:-1]  # Remove last character

        elif char == "*":
            # Repeat previous character 0 to 5 times
            repeated = result[-1] * random.randint(0, 5)
            result += repeated
            steps.append(f"Repeat '{result[-1]}' (0-5 times) → {repeated}")

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

        i += 1  # Move to next character

    return result, steps

# Given regex
regex = "(a|b)(c|d)E+G?P(Q|R|S)T(UV|W|X)*Z+1(0|1)*2(3|4){5}36"

# Generate a valid string and show steps
valid_string, process_steps = parse_regex(regex)

# Display results
print("Generated String:", valid_string)
print("\nProcessing Steps:")
for step in process_steps:
    print(step)
