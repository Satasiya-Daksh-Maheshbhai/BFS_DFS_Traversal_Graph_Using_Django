from django.shortcuts import render
from collections import deque, defaultdict

def graph_view(request):
    nodes = []
    edges = []
    traversal_result = ""
    mode = ""

    if request.method == "POST":
        edge_input = request.POST.get("edges")
        start = request.POST.get("start")
        mode = request.POST.get("mode")  # bfs or dfs

        graph = defaultdict(list)
        node_set = set()

        for pair in edge_input.split(","):
            u, v = pair.strip().split()
            graph[u].append(v)
            node_set.add(u)
            node_set.add(v)

        for k in graph:
            graph[k].sort()

        nodes = [{"id": n, "label": n.upper()} for n in sorted(node_set)]

        numbered_edges = []
        step = 1

        # ---------- BFS ----------
        if mode == "bfs":
            visited = set([start])
            q = deque([start])
            order = [start]

            while q:
                u = q.popleft()
                for v in graph[u]:
                    if v not in visited:
                        visited.add(v)
                        q.append(v)
                        order.append(v)
                        numbered_edges.append({
                            "from": u,
                            "to": v,
                            "label": str(step)
                        })
                        step += 1

            traversal_result = "-".join(order)

        # ---------- DFS ----------
        if mode == "dfs":
            visited = set()
            order = []

            def dfs(u):
                nonlocal step
                visited.add(u)
                order.append(u)
                for v in graph[u]:
                    if v not in visited:
                        numbered_edges.append({
                            "from": u,
                            "to": v,
                            "label": str(step)
                        })
                        step += 1
                        dfs(v)

            dfs(start)
            traversal_result = "-".join(order)

        edges = numbered_edges

    return render(request, "index.html", {
        "nodes": nodes,
        "edges": edges,
        "result": traversal_result,
        "mode": mode
    })
