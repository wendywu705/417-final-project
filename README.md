# 417 Final Project
Team 37: Kirby Fung, Wendy Wu, Ha Thu Nguyen

**Comparing the following heuristics for solving the 
8-puzzle using A\* search:**
- Manhattan Distance
- Inversion Distance
- Walking Distance
- Pattern Database
    - Fringe Database
    
**Comparison Metrics:**
- Run time
- Number of nodes expanded
- Length of solution (# tiles moved)

**To run the 8-puzzle or 15-puzzle:**

run in command line: `8puzzle.py $testfile`  
for example: `8puzzle.py tests/generated8.txt`

Or if running 15puzzle... same format.  
ie. `15puzzle.py tests/generated15.txt`

Results will be stored as `csv` files in the `results8` or `results15` directory depending on which Puzzle is run.

Test files can be written as text files or generated from the given test generators in the `tests` folder.
