
# Evacuation Route Finder

**Evacuation Route Finder** is an interactive tool designed to identify optimal evacuation paths during emergencies like fire outbreaks or natural disasters in buildings and enclosed spaces. The application uses AI and graph-based algorithms to dynamically compute and visualize the safest and fastest evacuation routes.

## Features

- **Dynamic Graph Representation**: Create building layouts as dynamic graphs with customizable nodes and edges.
- **Real-time Pathfinding**: Calculate optimal paths considering real-time obstacles and blocked paths.
- **Delay Customization**: Add delays to specific nodes to simulate real-world scenarios.
- **Interactive Visualization**: Visualize nodes, edges, and paths with color-coded indications for obstacles, blocked paths, and exits.
- **Customizable Layouts**: Choose from a default graph layout or design custom layouts using the editing mode.
- **Simulation Tools**: Simulate delays, blockages, and obstacles to evaluate evacuation efficiency.

## Technologies Used

- **Python**: Core programming language.
- **Pygame**: For graphical user interface and interactive visualization.
- **NetworkX**: For graph creation and manipulation.
- **Heapq**: For priority queue operations in the pathfinding algorithm.

## How It Works

1. **Graph Representation**: The building layout is represented as a graph, where:
   - Nodes represent rooms or checkpoints.
   - Edges represent paths between nodes with weights indicating traversal difficulty or distance.

2. **Pathfinding Algorithm**: The tool uses a modified Dijkstra's algorithm to find the shortest path from a start node to exit nodes.

3. **Visualization**: Routes are displayed in real-time, with paths, obstacles, and exits clearly marked.

## Controls

### Viewing Mode
- **Left Click**: Add/remove obstacles.
- **Right Click**: Block/unblock paths.
- **Mouse Scroll**: Increase/decrease delay at a node.
- **ESC**: Exit the application.

### Editing Mode
- **Left Click**: Add a new node or create edges.
- **Right Click**: Add an exit node.
- **D**: Delete a selected node.
- **E**: Add edges between nodes.
- **ESC**: Exit edit mode.

## Use Cases

- Emergency evacuation planning for buildings and facilities.
- Simulation of evacuation scenarios for training purposes.
- Optimizing building safety by analyzing evacuation strategies.

## Future Enhancements

- Integration with real-time sensors for automated path updates.
- Support for 3D building layouts.
- Machine learning models for predicting evacuation patterns.
