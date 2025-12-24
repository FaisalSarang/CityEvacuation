# City Evacuation Planning Simulator

A web-based simulator implementing the **Edmonds-Karp algorithm** to compute maximum evacuation flow for city road networks during emergency scenarios like hurricanes or wildfires.

## Overview

When natural disasters strike, the ability to quickly and efficiently evacuate residents from high-risk areas is critical. This project models a city's road network as a directed graph and uses the maximum flow algorithm to determine the city's optimal evacuation capacity—providing city planners with actionable insights on infrastructure bottlenecks.

## Features

- **Interactive Map Interface**: Click to add intersections, draw roads, set evacuation sources and safe zones
- **Real-time Visualization**: Watch the Edmonds-Karp algorithm find augmenting paths and compute max flow
- **Bottleneck Detection**: Identifies critical roads where capacity improvements would most impact evacuation efficiency
- **Fire Spread Simulation**: Visualize how spreading fires affect evacuation routes
- **Flow Animation**: See cars moving along evacuation routes based on computed flow

## Project Structure

```
city_evacuation/
├── app.py              # Flask backend with Edmonds-Karp algorithm
├── templates/
│   └── index.html      # Frontend (HTML/CSS/JavaScript)
└── README.md
```

## Installation

```bash
# Install dependencies
pip install flask

# Run the application
python app.py

# Open in browser
# http://localhost:5000
```

## Usage

1. **Add Nodes**: Click on the canvas to place intersections
2. **Add Edges**: Select edge mode, click two nodes to connect them with a road capacity
3. **Set Source**: Mark neighborhoods as evacuation starting points
4. **Set Sink**: Mark locations as safe zones
5. **Run Simulation**: Click "Run" to compute maximum evacuation flow

## Algorithm

The Edmonds-Karp algorithm finds maximum flow by:

1. Initialize residual graph with original road capacities
2. Use BFS to find the shortest augmenting path from source to sink
3. Identify the bottleneck (minimum capacity) along the path
4. Update the residual graph by subtracting flow from forward edges and adding to backward edges
5. Repeat until no augmenting path exists
6. Return total maximum flow

## Technical Details

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (Canvas API)
- **Algorithm**: Edmonds-Karp (BFS-based Ford-Fulkerson)
- **Time Complexity**: O(VE²) where V = vertices, E = edges

## Course Context

Developed as part of **CS 5800 Algorithms** at Northeastern University, demonstrating practical application of:
- Graph algorithms and directed weighted graphs
- Breadth-First Search (BFS) for shortest path finding
- Maximum Flow / Min-Cut theorem
