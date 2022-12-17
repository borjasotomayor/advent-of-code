"""
Day 16
https://adventofcode.com/2022/day/16

1st star: 00:40:59
2nd star: 04:40:56

Hoo boy, this one was a doozy. In Part 1, I took the approach
of simulating the behaviour of the "player", basicaly following
the exact behaviours described in the problem, and exploring
all possible paths. That worked out fine with some memoization.

And then Part 2 came along... I kept going with my "simulation"
approach, which turned out to be way too complicated, because
I kept trying to model the behaviour of the player and the elephant
happening "in parallel" (not in the sense of using threads, but
trying to determine what can happen at each time step). This
made the problem space completely intractable.

Eventually, I had enough insights about how to simplify the
problem space:

- It turns out there's a lot of sequences of 0-valves that are 
  basically just used to get to another valve. If you load the 
  graph as a weighted graph (where, for example 
  42 -> 0 -> 0 -> 0 -> 37 is represented as just two nodes with 
  distance 4 between them), that cuts down on the size of the 
  graph considerably (from 66 nodes to 16 in my input)

- I used Floyd–Warshall to pre-compute the shortest distance between 
  each pair of valves, which comes in handy later on.

- You're only going to visit each valve at most once, so you can 
  treat the problem as "find the sequence of valves that will give 
  me the highest pressure before I run out of time". Using a weighted 
  graph with pairwise distances pre-computed makes computing the 
  total pressure much simpler.

- For Part 2, you and the elephant will never turn on the same valves, 
  so you can go divide the set of valves into two disjoint subsets, 
  compute the the total pressure for both and add them up. Then you go 
  through all possible pairs of disjoint sets, and return the maximum. 

My solution still takes 30-40 seconds to run, which I suspect I could
improve if I used bitfields to keep track of the remaining/open
valves, instead of using sets.
"""

import util
import math
import sys
import re


class Valve:
    """
    Stores information about a valve (i.e., a node in our graph)
    """

    def __init__(self, name, flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        self.open = False

        # Set of neighbors
        self.neighbors = set()
        
        # Dictionary mapping valve label to distance
        # to that label. Note that, for a neighbor, 
        # this gives us the weight of the edge leading
        # to that neighbor
        self.dist = {}

    def __repr__(self):
        return f"Valve({self.name}, {self.flow_rate})"


def parse_input(input):
    """
    This function parses the input into a graph *and* converts it
    to a weighted graph. If you look at the provided input,
    there are several chains of nodes that look like this:

        PP -- QQ --  RR -- SS  
        17    00     00    22

    We'll never stop in QQ or RR because their valves have a flow
    rate of zero, so the above really represents the following:

        PP ------- SS
        17    3    22

    (i.e., it takes "3 minutes" to get from PP to SS)

    By removing these "intermediate zero flow nodes" we can greatly
    simplify the graph, and reduce the problem state (in the provided
    input, you go from a 66-node graph to a 16-node graph)

    On top of that, this function also runs Floyd–Warshall on the graph,
    as the pairwise distance between nodes will come in very handy.
    """
    
    # Regex for parsing each line
    pattern = re.compile(r"Valve (?P<valve>[A-Z][A-Z]) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valves? (?P<to_valves>[A-Z ,]+)")

    valves = {}

    # We'll be using these to compute the actual
    # neighbors and distances (as described in the dosctring)
    neighbors = {}
    dist = {}

    for line in input:
        match = pattern.match(line)
        valve_name = match.group("valve")
        flow_rate = int(match.group("flow_rate"))
        to_valves = match.group("to_valves").split(", ")

        v = Valve(valve_name, flow_rate)
        valves[valve_name] = v

        neighbors[valve_name] = to_valves

    # For every node in the graph, build its list of neighbors,
    # checking whether any of its neighbors is a "chain of 
    # zero-flow nodes" and, if so, reduce it to a single edge.
    for valve in valves.values():

        # We skip nodes with a zero flow rate, *except* the
        # origin node AA
        if valve.flow_rate == 0 and valve.name != "AA":
            continue

        for to_v in neighbors[valve.name]:
            # We'll use cur and prev to iterate over
            # each neighbor. prev is initalized to the
            # valve whose set of neighbors we are building,
            # and cur will be initialized to an immediate
            # neighbor. In the simplest case, cur has a flow
            # rate greater than zero, and it gets added directly
            # to the set of neighbors. Otherwise, we'll skip
            # through the nodes with zero flow
            prev = valve
            cur = valves[to_v]
            
            edge_weight = 1
            while cur.flow_rate == 0 and len(neighbors[cur.name]) == 2:
                edge_weight += 1
                next_valve_name = [v for v in neighbors[cur.name] if v != prev.name][0]

                # Update prev and cur
                prev = cur
                cur = valves[next_valve_name]

            valve.neighbors.add(cur)
            dist.setdefault(valve.name, {})[cur.name] = edge_weight
    
    # Get rid of the zero flow nodes (except AA)
    for v1 in list(valves.values()):
        if v1.flow_rate == 0 and v1.name != "AA":
            del valves[v1.name]

    # Floyd–Warshall: initialize the distances in the nodes
    # and then find the shortest pairwise distances.

    for v1 in valves.values():
        for v2 in valves.values():
            if v1 == v2:
                v1.dist[v1.name] = 0
            elif v2 in v1.neighbors:
                v1.dist[v2.name] = dist[v1.name][v2.name]
            else:
                v1.dist[v2.name] = sys.maxsize

    all_valves = valves.values()
    for vk in valves.values():
        for vi in valves.values():
            for vj in valves.values():
                if vi.dist[vj.name] > vi.dist[vk.name] + vk.dist[vj.name]:
                    vi.dist[vj.name] = vi.dist[vk.name] + vk.dist[vj.name]
    
    return valves


def find_path(graph, cur_node, remaining_valves, open_valves, time):
    """
    Recursively explore all the paths starting at cur_node that take
    "time" minutes or less (where following an edge reduces the time by the
    weight of the edge), and return the path with the highest
    score (i.e., highest pressure)    
    """

    # Open the valve at the current node
    remaining_valves = remaining_valves - {cur_node}
    open_valves = open_valves | {cur_node}

    # Compute the total pressure from all the open valves
    pressure = 0
    for ov in open_valves:
        pressure += graph[ov].flow_rate
        
    # If there's no more valves left to explore, we can
    # just compute the total pressure for the remaining time
    if len(remaining_valves) == 0:
        return [cur_node], pressure * time

    # Explore the paths starting with each of the remaining valves.
    best_path = []
    best_score = pressure * time
    for r in remaining_valves:
        dist = graph[cur_node].dist[r]
        if time - dist <= 1:
            continue
        tpres = (dist + 1) * pressure
        rpath, score = find_path(graph, r, remaining_valves, open_valves, time-dist-1)
        if tpres + score > best_score:
            best_score = tpres + score
            best_path = rpath

    # Return the best path and score
    return [cur_node] + best_path, best_score


def task1(graph):
    """
    Task 1: Find the best path starting at AA, with a time limit of 30
    """
    remaining_valves = set(graph.keys())
    remaining_valves.remove("AA")

    path, score = find_path(graph, "AA", remaining_valves, set(), 30)

    return score
    

def task2(graph):
    """
    Task 2: Divide the valves into all possible pairs of disjoint
    sets. For each pair, find the best score for each set (one for
    the player, another for the elephant). Add them together, and
    returning the maximum.
    """
    remaining_valves = list(graph.keys())
    remaining_valves.remove("AA")

    # The way we compute the disjoint sets, we're always
    # going to end up computing the same pair of subsets twice
    # (flipping whether they're assigned to the player or the elephant)
    # So, we keep track of the scores we've already computed.
    memo = {}

    best_score = 0

    # We compute the disjoint sets by essentially using a bitfield
    # where 0 assigns a valve to the player and 1 to the elephant
    # (and we iterate through all values from 0 to 2^valves)
    for i in range(0, 2**len(remaining_valves)):
        s = f"{i:b}".rjust(len(remaining_valves), "0")
        player = set()
        elephant = set()
        for incl, valve in zip(s, remaining_valves):
            if incl == "0":
                player.add(valve)
            else:
                elephant.add(valve)

        player = frozenset(player)
        elephant = frozenset(elephant)

        if player in memo:
            path1, score1 = memo[player]
        else:
            path1, score1 = find_path(graph, "AA", set(player), set(), 26)
            memo[player] = (path1, score1)

        if elephant in memo:
            path2, score2 = memo[elephant]
        else:
            path2, score2 = find_path(graph, "AA", set(elephant), set(), 26)
            memo[elephant] = (path2, score2)

        score = score1 + score2

        if score > best_score:
            best_score = score

    return best_score


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/16.in", sep="\n")
    input = util.read_strs("input/16.in", sep="\n")

    sample_graph = parse_input(sample)
    graph = parse_input(input)

    print("TASK 1")
    util.call_and_print(task1, sample_graph)
    util.call_and_print(task1, graph)

    print("\nTASK 2")
    util.call_and_print(task2, sample_graph)
    util.call_and_print(task2, graph)
