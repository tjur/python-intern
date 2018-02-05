import re


def hack_calculator(hack, letters={'a': 1, 'b': 2, 'c': 3}, phrases={'baa': 20, 'ba': 10}):
    try:
        power = letter_power(letters, hack) + phrase_power(phrases, hack)
        return power
    except ValueError:
        return 0

def letter_power(letters, hack):
    letters_count = dict.fromkeys(letters.keys(), 0) # letter -> number of already found repetitions
    power = 0
    for c in hack:
        if c not in letters:
            raise ValueError

        letters_count[c] += 1
        power += letters_count[c] * letters[c]
    return power

def phrase_power(phrases, hack):
    positions = get_positions_of_phrases(phrases, hack)
    power = 0
    for _, phrase in positions:
        power += phrases[phrase]
    return power

# returns a list of tuples (start pos of phrase, phrase - sorted by start positions (ascending)
def get_positions_of_phrases(phrases, hack):
    # here, for dynamically provided phrases, we should firstly
    # sort phrases dict by length of phrase (in descending order)
    # to always have the longest match
    regexp = '|'.join(phrases)
    positions = [(p.start(), p.group()) for p in re.finditer(regexp, hack)]
    return positions
