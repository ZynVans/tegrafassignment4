import random
from collections import defaultdict

def edge_set(p):
    return {tuple(sorted((p[i], p[i+1]))) for i in range(len(p) - 1)}

def similarity(p, q, n):
    # proporsi edge yang sama antar dua rute (0 = beda total, 1 = identik)
    return len(edge_set(p) & edge_set(q)) / (n - 1)

def generate_valid(n, k=3, max_sim=0.3, extra=None, seed=None):
    rnd = random.Random(seed)
    extra = n // 2 if extra is None else extra
    paths, tries = [], 5000
    while len(paths) < k and tries > 0:
        tries -= 1
        p = list(range(n))
        rnd.shuffle(p)
        if all(similarity(p, q, n) <= max_sim for q in paths):
            paths.append(p)
    edges = set()
    for p in paths:
        edges |= edge_set(p)
    for _ in range(extra):
        a, b = rnd.sample(range(n), 2)
        edges.add(tuple(sorted((a, b))))
    return sorted(edges), paths

def generate_invalid(n, mode="disconnected", seed=None):
    rnd = random.Random(seed)
    nodes = list(range(n))
    rnd.shuffle(nodes)
    edges = set()
    if mode == "star" and n >= 4:
        c = nodes[0]
        for v in nodes[1:]:
            edges.add(tuple(sorted((c, v))))
    else:  # dua komponen terpisah
        h = n // 2
        for grp in (nodes[:h], nodes[h:]):
            for i in range(len(grp) - 1):
                edges.add(tuple(sorted((grp[i], grp[i+1]))))
    return sorted(edges)

def is_connected(n, adj):
    seen, st = {0}, [0]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); st.append(v)
    return len(seen) == n

def find_paths(n, edges, limit=10):
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    if n == 1:
        return [[0]]
    if not is_connected(n, adj):
        return []
    if sum(1 for v in range(n) if len(adj[v]) == 1) > 2:
        return []
    res = []
    def dfs(path, vis):
        if len(res) >= limit:
            return
        if len(path) == n:
            if path[0] < path[-1]:  # buang duplikat arah terbalik
                res.append(path[:])
            return
        for v in adj[path[-1]]:
            if v not in vis:
                vis.add(v); path.append(v)
                dfs(path, vis)
                path.pop(); vis.remove(v)
    for s in range(n):
        dfs([s], {s})
    return res

def validate(n, edges):
    ps = find_paths(n, edges)
    if not ps:
        print("No valid path exists.")
    else:
        print(f"Valid! {len(ps)} path(s):")
        for p in ps:
            print(" -> ".join(map(str, p)))
    return bool(ps)

if __name__ == "__main__":
    n = 8
    e, planted = generate_valid(n, k=3, max_sim=0.3, seed=1)
    print("Edges:", e)
    validate(n, e)
    print()
    e2 = generate_invalid(n, "star", seed=1)
    print("Edges:", e2)
    validate(n, e2)