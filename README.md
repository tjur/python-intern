# python-intern

Solutions were written using Python 3.6.0.

## Task 1

`hack-calculator`just calls 2 functions: `letter_power` for calculating power of letters and `phrase_power_basic` for calculating power of phrases for a basic version of a problem (where phrases is {'ba':10, 'baa': 20}).

`letter_power` iterates over letters from a hack and simply increases power according to a letter base power and number of its repetitions.

`phrase_power_basic` uses `baa|ba` regular expression (`baa` must be before `ba` because we want to match it first - it gives more power) to find all (exclusive) occurences of phrases in a hack.

### Dynamic version of a problem

When we want to calculate hack power for dynamically provided letters and phrases then we don't have to change `letter_power`.
However, `phrase_power_basic` should be replaced with `phrase_power_dynamic`. It uses dynamic programming to evaluate maximal phrase power of a given hack. Auxilliary function `find_max_phrase_power(phrases, hack, start_pos, end_pos, d)` returns maximal phrase power for `hack[start_pos:end_pos]`. Because partial results are stored in `d` array, we can calculate phrase power for the whole hack in a quadratic time and memory complexity.

## Task 2

The program simply reads following lines from log file. For every line it parses different parts in separate functions. That functions also make some validation. If the line is correct, stripped url is returned and `requests_url_count` dictionary is updated. Otherwise `invalid_lines_count` is increased. Finally, the program prints content of the dictionary in the order specified in the task.
