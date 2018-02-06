import re


def hack_calculator(hack, letters=None, phrases=None):
    if letters is None:
        letters = {'a': 1, 'b': 2, 'c': 3}
    if phrases is None:
        phrases = {'baa': 20, 'ba': 10}

    try:
        power = letter_power(letters, hack) + phrase_power_basic(phrases, hack)
        return power
    except ValueError:
        return 0


# returns power of all letters in hack
# works for both basic and dynamic version of a problem
def letter_power(letters, hack):
    # create dict: letter -> number of already found repetitions
    letters_count = dict.fromkeys(letters.keys(), 0)
    power = 0
    for c in hack:
        if c not in letters:
            raise ValueError

        letters_count[c] += 1
        power += letters_count[c] * letters[c]
    return power


# solution for a basic version of a problem
# returns maximal phrase power when phrases = {'baa': 20, 'ba': 10}
def phrase_power_basic(phrases, hack):
    positions = get_positions_of_phrases(hack)
    power = 0
    for _, phrase in positions:
        power += phrases[phrase]
    return power


# returns a list of tuples (start pos of phrase, phrase)
# sorted by start positions (ascending)
def get_positions_of_phrases(hack):
    # 'baa' must be first in regexp to be matched before less profitable 'ba'
    regexp = 'baa|ba'
    positions = [(p.start(), p.group()) for p in re.finditer(regexp, hack)]
    return positions


# solution for a dynamic version of a problem
# returns maximal phrase power for hack
def phrase_power_dynamic(phrases, hack):
    d = [[None for i in range(len(hack)+1)] for j in range(len(hack)+1)]
    find_max_phrase_power(phrases, hack, 0, len(hack)+1, d)
    return d[0][len(hack)]


# returns maximal phrase power for hack[start_pos:end_pos]
# (start_pos is inclusive, end_pos is exclusive)
# it uses dynamic programming
# d is a 2D array for memorizing partial results
def find_max_phrase_power(phrases, hack, start_pos, end_pos, d):
    if d[start_pos][end_pos-1] is not None:
        return d[start_pos][end_pos-1]

    subhack = hack[start_pos:end_pos]
    subhack_points = phrases.get(subhack, 0)
    if len(subhack) <= 1:
        d[start_pos][end_pos-1] = subhack_points
        return subhack_points

    sublist_results = [
        find_max_phrase_power(phrases, hack, start_pos, start_pos+i, d) +
        find_max_phrase_power(phrases, hack, start_pos+i, end_pos, d)
        for i in range(1, end_pos-start_pos)
    ]

    sublist_max = max(sublist_results)
    d[start_pos][end_pos-1] = max(subhack_points, sublist_max)
    return d[start_pos][end_pos-1]
