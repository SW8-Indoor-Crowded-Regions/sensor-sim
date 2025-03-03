#!/usr/bin/env python3
"""
Interactive Graph Editor with Dynamic Dijkstra Calculation, Population Display,
State Export/Import, Fastest Path Highlighting, UI Buttons, and Zoom/Pan Functionality.

The window is divided into:
  - A top UI panel (height = 125 pixels) for buttons and instructions.
  - A bottom simulation area where the layout, nodes, edges, etc. are drawn using world coordinates.

Zooming (with the scroll wheel) is implemented so that the zoom is centered around the mouse pointer.
Panning is achieved by dragging the background when no node is clicked.

Keyboard shortcuts still work; modes persist until changed.

Ensure you have 'layout.png' in the same directory.
"""

import pygame
import heapq
import random
import sys
import math
import json

# ------------------------- Constants -------------------------
UI_PANEL_HEIGHT = 125
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SIM_AREA_HEIGHT = WINDOW_HEIGHT - UI_PANEL_HEIGHT

# ------------------------- Global Variables for Zoom/Pan & Drag -------------------------
zoom_factor = 1.0
pan_offset = [0, 0]  # [offset_x, offset_y]
dragging_background = False

# ------------------------- Button Class & Helper -------------------------

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self, surface, font):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def set_mode(new_mode):
    global mode, edge_start
    mode = new_mode
    edge_start = None

def set_mode_callback(new_mode):
    return lambda: set_mode(new_mode)

# ------------------------- Simulation Classes -------------------------

class Room:
    def __init__(self, name, population, max_capacity, poi):
        self.name = name
        self.population = population
        self.max_capacity = max_capacity
        self.poi = poi

    def __str__(self):
        return f"{self.name} ({self.poi}): {self.population}/{self.max_capacity}"

class TravelNode:
    def __init__(self, name, poi):
        self.name = name
        self.population = 0
        self.max_capacity = 999
        self.poi = poi

    def __str__(self):
        return f"{self.name} ({self.poi}): {self.population}/{self.max_capacity}"

class Door:
    def __init__(self, from_node, to_node, distance):
        self.from_node = from_node
        self.to_node = to_node
        self.distance = distance
        self.manual_weight = None

# ------------------------- Simulation Logic -------------------------

def effective_edge_weight(door):
    return door.manual_weight if door.manual_weight is not None else door.distance

def compute_travel_time(door, nodes, speed=1.0):
    dest = nodes[door.to_node]
    base_time = effective_edge_weight(door) / speed
    lag = 1 + (dest.population / dest.max_capacity)
    return base_time * lag

def dijkstra(graph, nodes, source, target, speed=1.0):
    distances = {node: float('inf') for node in nodes}
    previous = {node: None for node in nodes}
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        current_time, current_node = heapq.heappop(queue)
        if current_node == target:
            break
        for door in graph.get(current_node, []):
            travel_time = compute_travel_time(door, nodes, speed)
            new_time = current_time + travel_time
            if new_time < distances[door.to_node]:
                distances[door.to_node] = new_time
                previous[door.to_node] = current_node
                heapq.heappush(queue, (new_time, door.to_node))
    return distances, previous

def reconstruct_path(previous, source, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path

def simulate_movement(nodes, graph):
    delta = {node: 0 for node in nodes}
    for node_name, node in nodes.items():
        if isinstance(node, TravelNode):
            continue
        outgoing = graph.get(node_name, [])
        if outgoing and node.population > 0:
            fraction = random.uniform(0.1, 0.3)
            leaving = max(int(node.population * fraction), 1)
            delta[node_name] -= leaving
            for _ in range(leaving):
                chosen = random.choice(outgoing)
                delta[chosen.to_node] += 1
        else:
            delta[node_name] += random.choice([-1, 0, 1])
    for node_name in nodes:
        nodes[node_name].population = max(nodes[node_name].population + delta[node_name], 0)

# ------------------------- State Export/Import Functions -------------------------

def export_state():
    state = {
        "nodes": {},
        "node_positions": node_positions,
        "graph": {},
        "source": source,
        "target": target,
        "manual_route": manual_route,
    }
    for key, node in nodes.items():
        node_type = "Room" if isinstance(node, Room) else "TravelNode"
        state["nodes"][key] = {
            "type": node_type,
            "population": node.population,
            "max_capacity": node.max_capacity,
            "poi": node.poi,
        }
    for key, edges in graph.items():
        state["graph"][key] = []
        for edge in edges:
            edge_dict = {
                "from_node": edge.from_node,
                "to_node": edge.to_node,
                "manual_weight": edge.manual_weight,
            }
            state["graph"][key].append(edge_dict)
    try:
        with open("state.json", "w") as f:
            json.dump(state, f, indent=2)
        print("State exported to state.json")
    except Exception as e:
        print("Error exporting state:", e)

def import_state():
    global nodes, node_positions, graph, source, target, manual_route
    try:
        with open("state.json", "r") as f:
            state = json.load(f)
        nodes = {}
        for key, value in state["nodes"].items():
            if value["type"] == "Room":
                nodes[key] = Room(key, value["population"], value["max_capacity"], value["poi"])
            else:
                nodes[key] = TravelNode(key, value["poi"])
                nodes[key].population = value["population"]
                nodes[key].max_capacity = value["max_capacity"]
        node_positions.clear()
        node_positions.update(state["node_positions"])
        graph = {}
        for key, edge_list in state["graph"].items():
            graph[key] = []
            for edge_dict in edge_list:
                edge_obj = Door(edge_dict["from_node"], edge_dict["to_node"], 0)
                edge_obj.manual_weight = edge_dict["manual_weight"]
                graph[key].append(edge_obj)
        source = state.get("source", source)
        target = state.get("target", target)
        manual_route.clear()
        manual_route.extend(state.get("manual_route", []))
        print("State imported from state.json")
    except Exception as e:
        print("Error importing state:", e)

# ------------------------- Interactive Graph Editing Setup -------------------------

nodes = {
    "Entrance": Room("Entrance", 10, 30, "Main Entrance"),
    "Lobby": Room("Lobby", 15, 50, "Reception Area"),
    "Exit": Room("Exit", 0, 20, "Emergency Exit")
}
graph = {
    "Entrance": [Door("Entrance", "Lobby", 5)],
    "Lobby": [Door("Lobby", "Entrance", 5), Door("Lobby", "Exit", 7)],
    "Exit": [Door("Exit", "Lobby", 7)]
}
node_positions = {
    "Entrance": [200, 315],
    "Lobby": [260, 315],
    "Exit": [310, 315]
}
new_room_counter = 1
new_travel_counter = 1

MODE_DRAG = "drag"
MODE_ADD_ROOM = "add_room"
MODE_ADD_TRAVEL = "add_travel"
MODE_ADD_EDGE = "add_edge"
MODE_DELETE = "delete"
MODE_EDIT_EDGE = "edit_edge"
MODE_CHOOSE = "choose"
MODE_MANUAL_ROUTE = "manual_route"
mode = MODE_DRAG

edge_start = None
pending_edges = []
edge_to_edit = None
weight_input = ""
prev_mode = None

source = "Lobby"
target = "Exit"
manual_route = []
selected_nodes = []

# ------------------------- Button Setup -------------------------
buttons = [
    Button(10, 40, 80, 30, "Add Room", set_mode_callback(MODE_ADD_ROOM)),
    Button(100, 40, 80, 30, "Add Travel", set_mode_callback(MODE_ADD_TRAVEL)),
    Button(190, 40, 80, 30, "Add Edge", set_mode_callback(MODE_ADD_EDGE)),
    Button(280, 40, 80, 30, "Edit Edge", set_mode_callback(MODE_EDIT_EDGE)),
    Button(370, 40, 80, 30, "Delete", set_mode_callback(MODE_DELETE)),
    Button(460, 40, 120, 30, "Choose Src/Tgt", set_mode_callback(MODE_CHOOSE)),
    Button(590, 40, 100, 30, "Manual Route", set_mode_callback(MODE_MANUAL_ROUTE)),
    Button(700, 40, 60, 30, "Save", export_state),
    Button(770, 40, 60, 30, "Load", import_state)
]

# ------------------------- Pygame Initialization -------------------------
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Interactive Graph Editor with Dynamic Dijkstra Calculation")
clock = pygame.time.Clock()

try:
    layout_image = pygame.image.load("layout.png").convert()
    sim_layout = pygame.transform.scale(layout_image, (WINDOW_WIDTH, SIM_AREA_HEIGHT))
except Exception as e:
    print("Error loading layout.png. Ensure it exists in the same directory.")
    sys.exit()

WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("Arial", 16)

SIMULATION_INTERVAL = 1000
simulation_event = pygame.USEREVENT + 1
pygame.time.set_timer(simulation_event, SIMULATION_INTERVAL)

speed = 1.0
node_radius = 5
dragging_node = None
drag_offset = (0, 0)
EDGE_CLICK_THRESHOLD = 5

# ------------------------- Main Loop -------------------------
while True:
    # Draw UI panel
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WINDOW_WIDTH, UI_PANEL_HEIGHT))
    for button in buttons:
        button.draw(screen, font)
    
    # Clear simulation area.
    pygame.draw.rect(screen, (0, 0, 0), (0, UI_PANEL_HEIGHT, WINDOW_WIDTH, SIM_AREA_HEIGHT))
    
    # Draw simulation background with zoom & pan.
    scaled_width = int(WINDOW_WIDTH * zoom_factor)
    scaled_height = int(SIM_AREA_HEIGHT * zoom_factor)
    scaled_layout = pygame.transform.scale(layout_image, (scaled_width, scaled_height))
    screen.blit(scaled_layout, (pan_offset[0], UI_PANEL_HEIGHT + pan_offset[1]))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Process UI button clicks.
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if mouse_pos[1] < UI_PANEL_HEIGHT:
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        button.callback()
                continue
        
        # Zoom with scroll wheel.
        if event.type == pygame.MOUSEWHEEL:
            mouse_screen = pygame.mouse.get_pos()
            if mouse_screen[1] >= UI_PANEL_HEIGHT:
                sim_mouse = (mouse_screen[0], mouse_screen[1] - UI_PANEL_HEIGHT)
                world_x = (sim_mouse[0] - pan_offset[0]) / zoom_factor
                world_y = (sim_mouse[1] - pan_offset[1]) / zoom_factor
                zoom_factor *= (1 + event.y * 0.1)
                if zoom_factor < 0.1:
                    zoom_factor = 0.1
                pan_offset[0] = sim_mouse[0] - world_x * zoom_factor
                pan_offset[1] = sim_mouse[1] - world_y * zoom_factor
        
        # For simulation events, adjust y-coordinate.
        sim_event = None
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            if event.pos[1] >= UI_PANEL_HEIGHT:
                sim_event = event
                sim_event.pos = (event.pos[0], event.pos[1] - UI_PANEL_HEIGHT)
            else:
                sim_event = event
        else:
            sim_event = event
        
        if sim_event.type == simulation_event and mode not in [MODE_MANUAL_ROUTE]:
            simulate_movement(nodes, graph)
        
        if sim_event.type == pygame.KEYDOWN:
            if sim_event.key == pygame.K_s:
                export_state()
            elif sim_event.key == pygame.K_l:
                import_state()
            elif mode == MODE_MANUAL_ROUTE:
                if sim_event.key == pygame.K_RETURN:
                    if len(manual_route) >= 2:
                        source = manual_route[0]
                        target = manual_route[-1]
                    mode = MODE_MANUAL_ROUTE
                elif sim_event.key == pygame.K_ESCAPE:
                    manual_route = []
                    mode = MODE_DRAG
            else:
                if sim_event.key == pygame.K_r:
                    mode = MODE_ADD_ROOM
                elif sim_event.key == pygame.K_t:
                    mode = MODE_ADD_TRAVEL
                elif sim_event.key == pygame.K_e:
                    mode = MODE_ADD_EDGE
                    edge_start = None
                elif sim_event.key == pygame.K_x:
                    mode = MODE_DELETE
                elif sim_event.key == pygame.K_f:
                    mode = MODE_EDIT_EDGE
                elif sim_event.key == pygame.K_c:
                    mode = MODE_CHOOSE
                elif sim_event.key == pygame.K_m:
                    mode = MODE_MANUAL_ROUTE
                    manual_route = []
                elif sim_event.key == pygame.K_ESCAPE:
                    mode = MODE_DRAG
                    edge_start = None
                    pending_edges = []
                    edge_to_edit = None
        
        # Use relative motion (event.rel) for smoother dragging.
        if sim_event.type == pygame.MOUSEMOTION:
            if dragging_node is not None and mode == MODE_DRAG:
                rel = sim_event.rel
                # Adjust node's world coordinate based on relative movement.
                dx = rel[0] / zoom_factor
                dy = rel[1] / zoom_factor
                node_positions[dragging_node][0] += dx
                node_positions[dragging_node][1] += dy
            # If background is dragged (when no node is selected).
            elif dragging_background:
                rel = sim_event.rel
                pan_offset[0] += rel[0]
                pan_offset[1] += rel[1]
        
        if sim_event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = sim_event.pos
            # Convert to world coordinates.
            world_pos = ((mouse_pos[0] - pan_offset[0]) / zoom_factor,
                         (mouse_pos[1] - pan_offset[1]) / zoom_factor)
            if mode == MODE_DRAG:
                found_node = False
                for n, pos in node_positions.items():
                    if math.hypot(world_pos[0]-pos[0], world_pos[1]-pos[1]) <= node_radius:
                        dragging_node = n
                        found_node = True
                        break
                if not found_node:
                    dragging_background = True
            elif mode == MODE_ADD_ROOM:
                new_name = f"Room{new_room_counter}"
                new_room_counter += 1
                initial_pop = random.randint(5, 15)
                nodes[new_name] = Room(new_name, initial_pop, 30, "New Room")
                node_positions[new_name] = [world_pos[0], world_pos[1]]
            elif mode == MODE_ADD_TRAVEL:
                new_name = f"Waypoint{new_travel_counter}"
                new_travel_counter += 1
                nodes[new_name] = TravelNode(new_name, "New Waypoint")
                node_positions[new_name] = [world_pos[0], world_pos[1]]
            elif mode == MODE_ADD_EDGE:
                for n, pos in node_positions.items():
                    if math.hypot(world_pos[0]-pos[0], world_pos[1]-pos[1]) <= node_radius:
                        if edge_start is None:
                            edge_start = n
                        else:
                            if n != edge_start:
                                dist = math.hypot(node_positions[edge_start][0]-node_positions[n][0],
                                                  node_positions[edge_start][1]-node_positions[n][1])
                                edge1 = Door(edge_start, n, dist)
                                edge2 = Door(n, edge_start, dist)
                                graph.setdefault(edge_start, []).append(edge1)
                                graph.setdefault(n, []).append(edge2)
                            edge_start = None
                        break
            elif mode == MODE_DELETE:
                for n, pos in list(node_positions.items()):
                    if math.hypot(world_pos[0]-pos[0], world_pos[1]-pos[1]) <= node_radius:
                        del nodes[n]
                        del node_positions[n]
                        if n in graph:
                            del graph[n]
                        for key in list(graph.keys()):
                            graph[key] = [edge for edge in graph[key] if edge.to_node != n]
                        break
            elif mode == MODE_CHOOSE:
                for n, pos in node_positions.items():
                    if math.hypot(world_pos[0]-pos[0], world_pos[1]-pos[1]) <= node_radius:
                        if isinstance(nodes[n], Room):
                            selected = n
                            if len(selected_nodes) == 0:
                                source = selected
                                selected_nodes.append(selected)
                            elif len(selected_nodes) == 1:
                                target = selected
                                selected_nodes.append(selected)
                                mode = MODE_DRAG
                            break
            elif mode == MODE_MANUAL_ROUTE:
                for n, pos in node_positions.items():
                    if math.hypot(world_pos[0]-pos[0], world_pos[1]-pos[1]) <= node_radius:
                        manual_route.append(n)
                        break
        
        if sim_event.type == pygame.MOUSEBUTTONUP:
            dragging_node = None
            dragging_background = False
    
    for key, edges in graph.items():
        for edge in edges:
            if edge.manual_weight is None and edge.from_node in node_positions and edge.to_node in node_positions:
                dx = node_positions[edge.from_node][0] - node_positions[edge.to_node][0]
                dy = node_positions[edge.from_node][1] - node_positions[edge.to_node][1]
                edge.distance = math.hypot(dx, dy)
    
    distances, previous = dijkstra(graph, nodes, source, target, speed)
    computed_route = []
    if distances[target] < float('inf'):
        computed_route = reconstruct_path(previous, source, target)
    
    if len(computed_route) > 1:
        for i in range(len(computed_route)-1):
            start = node_positions[computed_route[i]]
            end = node_positions[computed_route[i+1]]
            screen_start = (int(start[0] * zoom_factor + pan_offset[0]),
                            int(start[1] * zoom_factor + UI_PANEL_HEIGHT + pan_offset[1]))
            screen_end = (int(end[0] * zoom_factor + pan_offset[0]),
                          int(end[1] * zoom_factor + UI_PANEL_HEIGHT + pan_offset[1]))
            pygame.draw.line(screen, GREEN, screen_start, screen_end, 6)
    
    if len(computed_route) > 0:
        fastest_path_str = "Fastest Path: " + " -> ".join(computed_route)
        fastest_path_text = font.render(fastest_path_str, True, BLACK)
        screen.blit(fastest_path_text, (10, WINDOW_HEIGHT - 30))
    
    drawn_edges = set()
    for key, edges in graph.items():
        for edge in edges:
            edge_key = frozenset({edge.from_node, edge.to_node})
            if edge.from_node in node_positions and edge.to_node in node_positions and edge_key not in drawn_edges:
                start = node_positions[edge.from_node]
                end = node_positions[edge.to_node]
                screen_start = (int(start[0] * zoom_factor + pan_offset[0]),
                                int(start[1] * zoom_factor + UI_PANEL_HEIGHT + pan_offset[1]))
                screen_end = (int(end[0] * zoom_factor + pan_offset[0]),
                              int(end[1] * zoom_factor + UI_PANEL_HEIGHT + pan_offset[1]))
                pygame.draw.line(screen, RED, screen_start, screen_end, 2)
                mid_x = int((screen_start[0] + screen_end[0]) / 2)
                mid_y = int((screen_start[1] + screen_end[1]) / 2)
                weight_val = effective_edge_weight(edge)
                weight_text = font.render(f"{weight_val:.1f}", True, BLACK)
                screen.blit(weight_text, (mid_x, mid_y))
                drawn_edges.add(edge_key)
    
    for n, pos in node_positions.items():
        screen_pos = (int(pos[0] * zoom_factor + pan_offset[0]),
                      int(pos[1] * zoom_factor + UI_PANEL_HEIGHT + pan_offset[1]))
        col = GREEN if isinstance(nodes[n], TravelNode) else BLUE
        pygame.draw.circle(screen, col, screen_pos, node_radius)
        label = font.render(n, True, WHITE)
        screen.blit(label, (screen_pos[0] - node_radius, screen_pos[1] - node_radius - 15))
        d_val = distances.get(n, float('inf'))
        d_str = f"{d_val:.1f}" if d_val < 1e6 else "inf"
        d_label = font.render("d: " + d_str, True, BLACK)
        screen.blit(d_label, (screen_pos[0] + node_radius, screen_pos[1] + node_radius))
        pop_label = font.render("p: " + str(nodes[n].population), True, BLACK)
        screen.blit(pop_label, (screen_pos[0] - node_radius, screen_pos[1] - node_radius - 30))
    
    if len(manual_route) > 1:
        for i in range(len(manual_route)-1):
            start = node_positions[manual_route[i]]
            end = node_positions[manual_route[i+1]]
            screen_start = (int(start[0] * zoom_factor + pan_offset[0]),
                            int(start[1] * zoom_factor + UI_PANEL_HEIGHT + pan_offset[1]))
            screen_end = (int(end[0] * zoom_factor + pan_offset[0]),
                          int(end[1] * zoom_factor + UI_PANEL_HEIGHT + pan_offset[1]))
            pygame.draw.line(screen, ORANGE, screen_start, screen_end, 2)
    
    ui_mode_text = font.render(f"Mode: {mode}", True, BLACK)
    screen.blit(ui_mode_text, (10, 80))
    instructions = [
        "R: Add Room, T: Add Travel, E: Add Edge, F: Edit Edge, X: Delete,",
        "C: Choose Src/Tgt, M: Manual Route, S: Save, L: Load, ESC: Drag/Cancel",
        "Scroll: Zoom In/Out, Drag empty space: Pan"
    ]
    for i, line in enumerate(instructions):
        instr = font.render(line, True, BLACK)
        screen.blit(instr, (10, 100 + i*20))
    
    if mode == MODE_MANUAL_ROUTE:
        route_instr = font.render("Manual Route: Click nodes to add. ENTER finalizes, ESC cancels.", True, BLACK)
        screen.blit(route_instr, (10, UI_PANEL_HEIGHT - 20))
    
    pygame.display.flip()
    clock.tick(30)
