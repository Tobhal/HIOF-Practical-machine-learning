# Part 2 Task
In this part, you will implement genetic algorithm (GA) to solve a NP-hard combinatorial optimization problem ─ The Multiple Depots Vehicle Routing Problem (MDVRP).

Vehicle routing problem (VRP) is a classical combinatorial optimization. VRP formulations are used to model a vast range of issues in many application fields, transportation, supply chain management, production planning, and telecommunication, to name but a few. A typical VRP can be stated as follows: a set of geographically dispersed customers with known demands are serviced by a homogenous fleet of vehicles with limited capacity. Each customer is to be fully serviced exactly once, and each vehicle is assumed to start and end at the same depot. The primary objective is to minimize the total distance travelled by all vehicles. However, in a large number of practical situations and to satisfy real-life scenarios, additional constraints are usually defined for variants of the VRP.

In this project, you need to solve the multi-depot VRP (MDVRP), which is an extension of the classical VRP except that there are multiple depots with many vehicles, and every customer should be serviced a vehicle based at one of several depots. Like the typical VRP, in the MDVRP, every vehicle route must start and end at the same depot. The challenge is to make a schedule for each vehicle individually so that the vehicles drive in the most efficient way, optimizing one or several objectives.The MDVRP is NP-hard, which means that an efficient algorithm for solving the problem to optimality is unavailable.

# Problem Formulation:
Formally, the MDVRP can be defined as follows. We are given a set of depot locations and a set of customer locations, which are assumed to be disjoint (even if two points share the exact physical coordinates, they are still handled as different entities). Each customer is characterized by their own demand. A fleet of vehicles with limited capacity is based at each depot. Each vehicle originates from one depot, services the customers assigned to that depot and returns to the same depot. The MDVRP consists of determining the routes for multiple depots with multiple vehicles per depot in parallel. Further, each depot has a set of customers. The route should also optimize predefined objective(s) as well as satisfy the following conditions:

1. every customer appears on exactly one route.
2. every route starts and ends at the originating depot.
3. capacity limit: the total demand of the customers on any route does not exceed a vehicle’s capacity.
4. route limit: the total duration of a route does not exceed a preset value (for this project, it is only for those problems for which this value is mentioned in the test data).

# Algorithm
As mentioned earlier, to solve the MDVRP, you need to implement the genetic algorithm (GA) that has been already discussed in lectures. In order to get the optimal/near-optimal results, you may check several forms of representation, genetic operators, and selection mechanism. It would be beneficial to test whether elitism gives a better solution.

Note that, GA parameter values (population size, generation number, crossover rate, and mutation rate) are correlated and your GA will successfully find the optimal values if you use appropriate parameter values. However, there is no definite rule to find the appropriate parameter values. Therefore, you should test different set of parameter values to decide the appropriate values.

# Things To Do
To test your code, we uploaded several benchmark test data and their solutions. The description of problem and solution data file formats is also included. Your code must have the option to read the test data according to the given format.

Since the MDVRP is an NP-hard problem, and GA is a heuristic algorithm, your implementation may not achieve the optimal total distances mentioned in the solutions for the test problems. It is not uncommon, and we are aware of this. While testing your implementation, we will accept if your produced solutions are within 15% of the known optimal values mentioned in the uploaded solutions.

# Report:
You should write a report answering the points below.
1. Describe the Chromosome representation that you used in your implementation. Also, mention another representation that could be used for this problem and why this representation is also suitable. Defend your choice of the most suitable representation.
2. Describe whether the crossover and mutation operators will produce infeasible off-spring(s) after executing. If yes, how did you handle that? If not, why not?
3. In GA, the parameter values (population size, generation number, crossover rate, and mutation rate) often have some form of relationship. Considering that you tested several sets of parameter values, what relationship did you observe among these parameter values?

# Sources
- https://hiof.instructure.com/courses/5088/files/folder/Lecture%20Slides/W_10?preview=1015987
- https://www.kite.com/python/answers/how-to-generate-a-random-color-for-a-matplotlib-plot-in-python

## Easy solution
- https://github.com/mpinta/evovrp

## Research
- https://ieeexplore.ieee.org/document/8679429
- https://github.com/markusmkim/GA-MDVRP
- https://github.com/Nikronic/Optimized-MDVRPc
- https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.207.9651&rep=rep1&type=pdf
- https://ieeexplore.ieee.org/abstract/document/4840417

- https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjvzvGt39v0AhU6RPEDHZRJDJkQFnoECAMQAQ&url=https%3A%2F%2Fwww.mdpi.com%2F2073-8994%2F13%2F10%2F1923%2Fpdf&usg=AOvVaw1irdCIQ9mRkipScDTFDtp4
    - Page 9: Giant Tour Best Cost Crossover

- https://www.baberuthleague.org/media/11222/3-Team%20Double%20Elimination%20Bracket.pdf

- https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult
- https://machinelearningmastery.com/differential-evolution-global-optimization-with-python/
- https://scikit-opt.github.io
- https://scikit-opt.github.io/scikit-opt/#/en/README?id=_2-genetic-algorithm

# To read?
- https://hiof.instructure.com/courses/5088/files/folder/Lecture%20Slides/W_11?preview=1021815