# SimulatedAnnealing
Given a list of wizards and constraints, uses simulated annealing to find a satisfiable ordering that satisfies all given constraints and uses all possible wizards.

- Instance validator usage: python instance_validator.py [path to input file] [20, 35 or 50]
- Output validator usage: python output_validator.py [path_to_input_file] [path_to_output_file]
- Simulated annealing usage: python simulated_anneal.py [path_to_input_file]

Each input file must adhere to the following specifications.

- The first line of each input file must be a single integer W, the number of wizards in your problem.
This number may be between 1 and (20, 35 or 50), depending on which input file you’re working on.
For instance, input20.in must contain at most 20 wizards.
- The second line of each input file must contain the W unique, alphanumeric wizard names, separated
by a space. Each wizard name must be an alphanumeric string of maximum 10 characters. These
space-separated wizard names must be an ordering of the wizards (according to their relative ages)
- The third line of each input file must be a single integer C, the number of constraints in your problem.
This number may be between 1 and 500.
- The next C lines of your input file must contain constraints of the form:
<Wizard1 Wizard2 Wizard3>. Each constraint specifies that the age of Wizard3 is not in
between the ages of Wizard1 and Wizard2. Note: this does not mean Wizard1 is necessarily
younger than Wizard2.
- Each wizard must appear at least once in your constraints.


Sample input: 

4
Harry Hermione Severus Albus
3
Hermione Harry Severus
Severus Harry Albus
Severus Albus Hermione

