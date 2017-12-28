import random
import math
import sys

def main(argv): 
""" 
	Reads the file, stores all constraints, and creates a randomly shuffled initial ordering. 
    Then, we run simulated annealing with backtracking and conservative random restarts.
"""
	if len(argv) != 1:
		print("Usage: python simulated_anneal.py [path_to_input_file]")
		return
	f = open(argv[0], 'r')
	wiz_num = int(f.readline())
	myConstraints = []
	numConstraints = int(f.readline())
	c = f.readline()
	initial_ordering = []
	while c:
		c = c.split()
		tempmin = min(c[0], c[1])
		tempmax = max(c[0], c[1])
		c[0] = tempmin
		c[1] = tempmax
		if c[0] not in initial_ordering:
			initial_ordering.append(c[0])
		if c[1] not in initial_ordering:
			initial_ordering.append(c[1])
		if c[2] not in initial_ordering:
			initial_ordering.append(c[2])
		myConstraints.append(c)
		c = f.readline()
	i = 0
	random.shuffle(initial_ordering)
	curr_ordering = initial_ordering
	curr_cost = constaint_counter(initial_ordering, myConstraints)
	b = 0 #backtracking counter
	while True:
		anneal_iter_ordering, iter_ordering_cost = anneal(myConstraints, curr_ordering)
		if iter_ordering_cost == len(myConstraints):
			print("SUCCESS")
			print(" ".join(map(str, anneal_iter_ordering)))
			break
		if iter_ordering_cost >= curr_cost:
			if iter_ordering_cost > curr_cost:
				i = 0
				print(iter_ordering_cost) # Found a better ordering through an iteration of simulated annealing, print cost to track progress.
				#if iter_ordering_cost == 499: # Checks near-complete orderings, mainly for debugging.
					#print(" ".join(map(str, anneal_iter_ordering))) 
			curr_cost = iter_ordering_cost
			curr_ordering = anneal_iter_ordering
			""" Comment out for efficiency, uncomment for maximum clarity or debugging.
			print(" ".join(map(str, anneal_iter_ordering))) 
			print(constraint_lister(curr_ordering, myConstraints))
			"""

		i += 1
		if i >= 30:
			if b > 20 and iter_ordering_cost < len(myConstraints)*0.95:
				random.shuffle(initial_ordering)
				curr_ordering = initial_ordering
				curr_cost = constaint_counter(initial_ordering, myConstraints)
				i = 0
				b = 0
			else:
				constraints_left = constraint_lister(anneal_iter_ordering, myConstraints)
				constraint_index = random.choice(xrange(len(constraints_left)))
				wiz_three_pos = anneal_iter_ordering.index(constraints_left[constraint_index][2])
				wiz_two_pos = anneal_iter_ordering.index(constraints_left[constraint_index][1])
				wiz_one_pos = anneal_iter_ordering.index(constraints_left[constraint_index][0])
				if abs(wiz_three_pos - wiz_two_pos) <= abs(wiz_three_pos - wiz_one_pos):
					curr_ordering = anneal_iter_ordering[:]
					curr_ordering[wiz_three_pos] = anneal_iter_ordering[wiz_two_pos]
					curr_ordering[wiz_two_pos] = anneal_iter_ordering[wiz_three_pos]
				else:
					curr_ordering = anneal_iter_ordering[:]
					curr_ordering[wiz_three_pos] = anneal_iter_ordering[wiz_one_pos]
					curr_ordering[wiz_one_pos] = anneal_iter_ordering[wiz_three_pos]
				curr_cost = constaint_counter(curr_ordering, myConstraints)
				print(curr_cost) # Cost loss indicates backtracking.
				b += 1
				i = 0

# Potentially chooses a new ordering made by swapping two wizards in the old ordering.	
def choose_new(ordering, old_cost, temp, myConstraints): 
	if old_cost >= len(myConstraints)*0.90 and random.random() > 0.5: # Added to target wizards that are more	  
		constraints_left = constraint_lister(ordering, myConstraints) # likely to be in the wrong position.
		if constraints_left:
			first_candidate = ordering.index(random.choice(random.choice(constraints_left)))
			second_candidate = ordering.index(random.choice(random.choice(constraints_left)))
			while first_candidate == second_candidate:
				second_candidate = ordering.index(random.choice(random.choice(constraints_left)))
		else:
			return ordering, old_cost
	else:
		first_candidate = random.choice(xrange(len(ordering)))
		second_candidate = random.choice(xrange(len(ordering)))
		while first_candidate == second_candidate:
			second_candidate = random.choice(xrange(len(ordering)))		
	new_ordering = ordering[:]
	new_ordering[second_candidate] = ordering[first_candidate]
	new_ordering[first_candidate] = ordering[second_candidate] # Our old ordering randomly swaps two wizards.
	new_cost = constaint_counter(new_ordering, myConstraints)
	delta = new_cost - old_cost
	if delta >= 0: # If our new ordering satisfies more constraints than our old ordering, we return the new ordering.
		return new_ordering, new_cost
	else: # Even if delta is negative, our new ordering will be returned with probability e^(delta/temp). Otherwise return old ordering.
		acceptance_prob = math.exp(delta/temp)
		if acceptance_prob > random.random():
			return new_ordering, new_cost
		else:
			return ordering, old_cost

# Counts the number of constraints satisfied by our ordering, where myConstraints is a list of constraints.
def constaint_counter(ordering, myConstraints): 
	output_ordering_map = {k: v for v, k in enumerate(ordering)}
	constraints_satisfied = 0
	for i in range(len(myConstraints)):
		m = output_ordering_map 

		wiz_a = m[myConstraints[i][0]]
		wiz_b = m[myConstraints[i][1]]
		wiz_mid = m[myConstraints[i][2]]

		if ((wiz_mid > wiz_b and wiz_mid > wiz_a) or (wiz_mid < wiz_b and wiz_mid < wiz_a)):
			constraints_satisfied += 1
		elif (wiz_mid == wiz_b == wiz_a) or (wiz_mid == wiz_a) or (wiz_mid == wiz_b):
			constraints_satisfied += 1
	return constraints_satisfied

# Finds the constraints not satisfied and returns a list of them.
def constraint_lister(ordering, myConstraints): 
	output_ordering_map = {k: v for v, k in enumerate(ordering)}
	constraints_failed = []
	for i in range(len(myConstraints)):
		m = output_ordering_map 

		wiz_a = m[myConstraints[i][0]]
		wiz_b = m[myConstraints[i][1]]
		wiz_mid = m[myConstraints[i][2]]

		if not ((wiz_mid > wiz_b and wiz_mid > wiz_a) or (wiz_mid < wiz_b and wiz_mid < wiz_a)):
			constraints_failed.append(myConstraints[i])
	return constraints_failed

def anneal(myConstraints, initial_ordering): 
	""" 
		Runs simulated annealing with the ordering passed in. It randomly swaps wizards in the ordering at each step,
		and will overwrite the old ordering with the new ordering if the new ordering satisfies more constraints. To 
		prevent being trapped in a local optimum, it may overwrite the old ordering with the new ordering even if the 
		new ordering satisfies less constraints. As temperature lowers, simulated annealing will start off randomly
		exploring the search space but slowly becomes local search.
	"""
	initial_cost = constaint_counter(initial_ordering, myConstraints)
	temp = 1
	k = 1
	best_order = initial_ordering
	best_cost = initial_cost
	while temp > 0.0001:
		if temp == 1:
			ordering, new_cost = choose_new(initial_ordering, initial_cost, temp, myConstraints)
		else:
			ordering, new_cost = choose_new(ordering, old_cost, temp, myConstraints)
		if new_cost >= best_cost: # Keep track of the best state that simulated annealing has discovered.
			best_cost = new_cost
			best_order = ordering
		if best_cost == len(myConstraints):
			return best_order, best_cost
		temp -= 0.0001
		k += 1
		old_cost = new_cost
	return best_order, best_cost

if __name__ == '__main__':
	main(sys.argv[1:])