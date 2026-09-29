# Dungeon Generator & Validator

**Graph Theory Group Homework**

## Group Members
1. Padhang Abiyu Fikri - 5025251014
2. Aditya Lingga Mardika - 5025251158
3. Dzulfiqar Rafi'ussunnah - 5025251011
4. Muhammad Faris Alfarrel - 5025251002
---

## Project Description
This project implements the concept of Hamiltonian Graphs into a procedural generation system for a dungeon-themed game[cite: 1]. The core gameplay requires the player to visit every room (vertex) exactly once without reusing any tunnel (edge), which mathematically translates to finding a Hamiltonian Path[cite: 1].

The program consists of two main components:
1. **Generator**: Generates dungeons guaranteed to have at least one valid solution, as well as invalid dungeons that are impossible to clear.
2. **Validator**: Uses a search algorithm to verify and output the paths of the generated dungeon.

---

## 1. Dungeon Generator Algorithm

The generator models the dungeon as an undirected graph where rooms are vertices and tunnels are edges.

*   **`generate_valid` Function (Valid Dungeon):** 
    To ensure the dungeon is clearable, the algorithm first creates a base spanning path by shuffling the order of all rooms. This guarantees the existence of a Hamiltonian Path[cite: 1]. To prevent the graph from being too linear or repetitive, the algorithm overlays multiple paths (limiting similarity via the `similarity` function) and adds random noise edges. The result is a branched dungeon that is guaranteed to be valid.
*   **`generate_invalid` Function (Invalid Dungeon):** 
    The algorithm intentionally designs graphs that violate Hamiltonian properties. There are two modes:
    1.  `star`: Forms a star graph where one room acts as the center. If the graph has >= 4 rooms, it is impossible to visit all the outer rooms without passing through the center room more than once.
    2.  `disconnected`: Splits the graph into two disconnected components, ensuring no continuous path can cover all rooms.

---

## 2. Validator Algorithm

Since the Hamiltonian Cycle/Path problem is NP-complete[cite: 1], the validator uses a **Depth-First Search (DFS) with Backtracking** algorithm.

**How Backtracking Works:**
The algorithm attempts to start exploring from every room. When in a room, the function marks it as visited and tries to enter an unvisited neighboring tunnel. If it reaches a dead end before all rooms are visited, the algorithm backtracks and tries another route. If the path length equals the total number of rooms, the path is printed as a valid solution[cite: 1].

**Validator Optimization (Pruning):**
To avoid time-consuming brute-force computation on graphs with no solutions, the validator is equipped with two early exit checks:
1.  **Connectedness Check:** Using the `is_connected` function, the validator rejects the graph if there are any isolated rooms disconnected from the main network[cite: 1].
2.  **Vertex Degree Check:** A Hamiltonian Path can have at most 2 vertices with a degree of 1 (the start and end points of the route)[cite: 1]. The function checks the degree of every vertex[cite: 1]. If there are more than 2 rooms with only 1 tunnel (`len(adj[v]) == 1`), the graph is mathematically impossible to have a Hamiltonian Path, so the DFS is aborted.

---

## 3. Sample Cases

Below are the sample outputs of the program based on N=8 (8 rooms):

### Valid Case
**Input Edges:** 
`[(0, 1), (0, 3), (0, 4), (0, 5), (0, 7), (1, 2), (1, 4), (1, 5), (1, 6), (2, 5), (2, 6), (2, 7), (3, 4), (3, 5), (3, 6), (4, 7), (6, 7)]`

**Output Validator:**
```text
Valid! 10 path(s):
0 -> 3 -> 4 -> 1 -> 6 -> 7 -> 2 -> 5
0 -> 4 -> 3 -> 6 -> 7 -> 2 -> 1 -> 5
... (other routes)
