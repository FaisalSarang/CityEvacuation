from flask import Flask, render_template, request, jsonify
from collections import defaultdict, deque

app = Flask(__name__)

# Virtual super-source and super-sink IDs
SUPER_SOURCE = '__SUPER_SOURCE__'
SUPER_SINK = '__SUPER_SINK__'

class EdmondsKarp:
    def __init__(self, graph):
        self.graph = graph
        self.residual_graph = defaultdict(lambda: defaultdict(int))
        self.flow_graph = defaultdict(lambda: defaultdict(int))
        for u in graph:
            for v, capacity in graph[u].items():
                self.residual_graph[u][v] = capacity
    
    def bfs(self, source, sink, parent):
        visited = set([source])
        queue = deque([source])
        
        while queue:
            u = queue.popleft()
            
            for v in self.residual_graph[u]:
                if v not in visited and self.residual_graph[u][v] > 0:
                    visited.add(v)
                    queue.append(v)
                    parent[v] = u
                    if v == sink:
                        return True
        return False
    
    def max_flow(self, source, sink):
        parent = {}
        max_flow_value = 0
        paths = []
        
        while self.bfs(source, sink, parent):
            path_flow = float('inf')
            s = sink
            path = []
            
            while s != source:
                path.append(s)
                path_flow = min(path_flow, self.residual_graph[parent[s]][s])
                s = parent[s]
            path.append(source)
            path.reverse()
            
            # Convert inf to large number for JSON
            if path_flow == float('inf'):
                path_flow = 999999
            
            paths.append({'path': path, 'flow': int(path_flow)})
            
            max_flow_value += path_flow
            v = sink
            
            while v != source:
                u = parent[v]
                self.residual_graph[u][v] -= path_flow
                self.residual_graph[v][u] += path_flow
                if v in self.graph.get(u, {}):
                    self.flow_graph[u][v] += path_flow
                else:
                    self.flow_graph[v][u] -= path_flow
                v = parent[v]
            
            parent = {}
        
        edge_flows = {}
        for u in self.graph:
            for v in self.graph[u]:
                flow = self.flow_graph[u][v]
                if flow == float('inf'):
                    flow = 0
                edge_flows[f"{u}-{v}"] = int(flow)
        
        return int(max_flow_value), paths, edge_flows

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    nodes = data['nodes']
    edges = data['edges']
    
    # Build base graph from edges
    graph = defaultdict(dict)
    for edge in edges:
        from_node = edge['from']
        to_node = edge['to']
        capacity = edge['capacity']
        graph[from_node][to_node] = capacity
    
    # Check if using multiple sources/sinks (new API) or single (old API)
    if 'sources' in data and 'sinks' in data:
        sources = data['sources']  # List of {id, cars}
        sinks = data['sinks']      # List of {id, rate} - rate is cars/min throughput
        
        # Add super-source -> each real source with UNLIMITED capacity
        # Sources don't limit flow rate - only edges do
        # The 'cars' value is just for tracking how many need to evacuate
        for src in sources:
            graph[SUPER_SOURCE][src['id']] = 999999  # Unlimited throughput
        
        # Add each real sink -> super-sink with UNLIMITED capacity
        # Sinks are exits - cars leave the system, no capacity limit
        for snk in sinks:
            graph[snk['id']][SUPER_SINK] = 999999  # Unlimited throughput
        
        # Run Edmonds-Karp from super-source to super-sink
        ek = EdmondsKarp(graph)
        max_flow_value, paths, edge_flows = ek.max_flow(SUPER_SOURCE, SUPER_SINK)
        
        # Clean up paths: remove super-source and super-sink
        cleaned_paths = []
        for p in paths:
            clean_path = [node for node in p['path'] if node not in (SUPER_SOURCE, SUPER_SINK)]
            if len(clean_path) >= 2:
                cleaned_paths.append({'path': clean_path, 'flow': p['flow']})
        
        # Remove super-source/sink from edge_flows
        edge_flows = {k: v for k, v in edge_flows.items() 
                      if SUPER_SOURCE not in k and SUPER_SINK not in k}
        
        return jsonify({
            'max_flow': max_flow_value,
            'paths': cleaned_paths,
            'num_routes': len(cleaned_paths),
            'edge_flows': edge_flows
        })
    else:
        # Old single source/sink API (backward compatibility)
        source_id = data['source']
        sink_id = data['sink']
        
        ek = EdmondsKarp(graph)
        max_flow_value, paths, edge_flows = ek.max_flow(source_id, sink_id)
        
        return jsonify({
            'max_flow': max_flow_value,
            'paths': paths,
            'num_routes': len(paths),
            'edge_flows': edge_flows
        })

if __name__ == '__main__':
    app.run(debug=True)