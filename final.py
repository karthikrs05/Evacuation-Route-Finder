import networkx as nx  
import pygame  
from pygame.locals import *  
import heapq  
import math  

win_width = 1200
win_height = 800  
NODE_SIZE = 20  

white =  (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green =  (0,255,0)
gray =  (128,128,128)
yellow =  (255,255,0)

txt_size = 24  

pygame.init()  
screen = pygame.display.set_mode((win_width, win_height))  
pygame.display.set_caption("Evacuation Route Finder")  
clock = pygame.time.Clock()  
font = pygame.font.Font(None, txt_size)  

def find(graph, start, end):
    queue = [(0, start)]  
    visited, costs = {}, {start: 0}  
    while queue:
        _, current = heapq.heappop(queue)  
        if current == end: break  
        for nextNode in graph.neighbors(current):  

            if nextNode in obstacles or (current, nextNode) in blocked_edges or (nextNode, current) in blocked_edges:
                continue

            cost = costs[current] + graph.edges[current, nextNode]['weight'] + graph.nodes[nextNode].get('delay', 0)

            if nextNode not in costs or cost < costs[nextNode]:
                costs[nextNode], visited[nextNode] = cost, current  
                heapq.heappush(queue, (cost, nextNode))  

    path = []  
    node = end  
    while node != start:  
        path.append(node)  
        node = visited.get(node)  
        if not node: return [], 0  
    return [start] + path[::-1], costs.get(end, 0)  

def DefaultGraph():
    
    g = nx.Graph()  

    nodes = {
        (100,100): "A1", (300,100): "A2", (500,100): "A3", (700,100): "A4", (900,100): "A5",  
        (100,250): "B1", (300,250): "H1", (500,250): "H2", (700,250): "H3", (900,250): "B5",  
        (100,400): "C1", (300,400): "H4", (500,400): "H5", (700,400): "H6", (900,400): "C5",  
        (100,600): "E1", (500,600): "E2", (900,600): "E3"  
    }

    for pos, label in nodes.items():
        g.add_node(pos, pos=pos, label=label, delay=0)  

    edges = [((x,y), (x+200,y), 2) for y in [100,250,400] for x in range(100,900,200)]

    edges += [((x,y), (x,y+150), 3) for x in range(100,1000,200) for y in [100,250]]

    edges += [((x,400), (x,600), 4) for x in [100,500,900]]

    edges += [((300,250), (500,400), 4), ((700,250), (500,400), 4), 
             ((300,400), (500,600), 4), ((700,400), (500,600), 4)]

    for e in edges:
        g.add_edge(e[0], e[1], weight=e[2])  
    return g  

def draw(graph, paths, times, buttons, mode="view", selected=None, drawing=None):
    
    screen.fill((240,240,245))  

    for e in graph.edges:

        color = red if e in blocked_edges or (e[1],e[0]) in blocked_edges else gray
        start_pos = graph.nodes[e[0]]['pos']  
        EndPos = graph.nodes[e[1]]['pos']  
        pygame.draw.line(screen, color, start_pos, EndPos, 3)  

    for path, color, offset in zip(paths, [red,blue,yellow], [(0,0),(4,4),(-4,-4)]):
        if path:  
            for i in range(len(path)-1):  
                start = tuple(x+o for x,o in zip(graph.nodes[path[i]]['pos'], offset))  
                end = tuple(x+o for x,o in zip(graph.nodes[path[i+1]]['pos'], offset))  
                pygame.draw.line(screen, color, start, end, 5)  

    for e in graph.edges:
        start_pos = graph.nodes[e[0]]['pos']  
        EndPos = graph.nodes[e[1]]['pos']  
        weight = graph.edges[e[0], e[1]]['weight']  
        Xmid = (start_pos[0] + EndPos[0]) // 2  
        Ymid = (start_pos[1] + EndPos[1]) // 2  
        weight_text = font.render(str(weight), True, black)  
        weight_rect = weight_text.get_rect(center=(Xmid, Ymid))  
        pygame.draw.rect(screen, white, weight_rect.inflate(10,10))  
        screen.blit(weight_text, weight_rect)  

    for node, data in graph.nodes(data=True):

        color = red if node in obstacles else green if "E" in data['label'] else blue
        if node == selected: color = yellow  
        pygame.draw.circle(screen, color, data['pos'], NODE_SIZE)  

        for text, yoffset in [(data['label'],-45), (f"d:{data['delay']}s" if data['delay']>0 else "",45)]:
            if text:  
                surf = font.render(text, True, black if yoffset<0 else gray)  
                rect = surf.get_rect(center=(data['pos'][0], data['pos'][1]+yoffset))  
                pygame.draw.rect(screen, white, rect.inflate(10,10))  
                screen.blit(surf, rect)  

    if drawing:
        pygame.draw.line(screen, yellow, graph.nodes[drawing[0]]['pos'], pygame.mouse.get_pos(), 3)

    pygame.draw.rect(screen, (220,220,225), (0,win_height-150,win_width,150))  
    pygame.draw.line(screen, gray, (0,win_height-150), (win_width,win_height-150), 2)  

    if mode == "view":

        screen.blit(font.render("Times:", True, black), (20, win_height-140))  
        for i,t in enumerate(times):  
            if t > 0:
                screen.blit(font.render(f"Exit {i+1}: {t:.1f}s", True, black), (40, win_height-110+i*30))

        if buttons:
            screen.blit(font.render("Start:", True, black), (win_width//2-font.size("Start:")[0]//2, win_height-140))
            x,y,w,h = win_width//2-250, win_height-110, 60, 30  
            for i,(pos,btn) in enumerate(buttons.items()):
                rect = pygame.Rect(x+(i%8)*(w+10), y+(i//8)*(h+10), w, h)  
                pygame.draw.rect(screen, green if btn['selected'] else gray, rect)  
                pygame.draw.rect(screen, black, rect, 1)  
                text = font.render(btn['label'], True, black)  
                screen.blit(text, text.get_rect(center=rect.center))  
                btn['rect'] = rect  

        helpText = ["Left Click: Toggle obstacles", "Right Click: Block/Unblock path", 
                    "Scroll: Add/Remove delay", "ESC: Exit"]
        screen.blit(font.render("Help:", True, black), (win_width-300, win_height-140))  
        for i,line in enumerate(helpText):  
            screen.blit(font.render(line, True, black), (win_width-280, win_height-110+i*30))
    else:

        screen.blit(font.render("Edit Mode Controls:", True, black), (20, win_height-140))  
        left = ["Left Click: Add new node", "Right Click: Add exit node", "D: Delete selected node"]  
        right = ["E: Add edge between nodes", "B: Toggle node blocking", "ESC: Exit edit mode"]  
        for i,(l,r) in enumerate(zip(left,right)):  
            screen.blit(font.render(l, True, black), (40, win_height-110+i*25))  
            screen.blit(font.render(r, True, black), (win_width//2, win_height-110+i*25))  

    pygame.display.flip()  

def getNode(graph, pos):
    return next((n for n in graph.nodes() if math.dist(graph.nodes[n]['pos'], pos) <= NODE_SIZE), None)  

def getEdge(graph, pos):
    for e in graph.edges():  
        start, end = graph.nodes[e[0]]['pos'], graph.nodes[e[1]]['pos']  
        length = math.dist(start, end)  
        if length == 0: continue  

        t = max(0, min(1, sum((p-s)*(e-s) for p,s,e in zip(pos,start,end))/length**2))
        if math.dist(pos, (start[0]+t*(end[0]-start[0]), start[1]+t*(end[1]-start[1]))) <= 5:
            return e  
    return None  

def get_weight():
    popup = pygame.Surface((200, 100))  
    popup.fill(white)  
    pygame.draw.rect(popup, black, popup.get_rect(), 2)  
    popup.blit(font.render("Weight (1-9):", True, black), (10, 10))  
    while True:
        screen.blit(popup, ((win_width-200)//2, (win_height-100)//2))  
        pygame.display.flip()  
        event = pygame.event.wait()  
        if event.type == KEYDOWN:  
            if K_1 <= event.key <= K_9: return event.key - K_0  
            if event.key == K_ESCAPE: return None  

def edit(graph):
    count, selected, drawing = 1, None, None  
    while True:
        clock.tick(60)  
        draw(graph, [], [], {}, "edit", selected, drawing)  
        for event in pygame.event.get():  
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return graph  
            elif event.type == MOUSEBUTTONDOWN and event.pos[1] < win_height-150:  
                node = getNode(graph, event.pos)  
                if event.button == 1:  
                    if not node:  
                        graph.add_node(event.pos, pos=event.pos, label=f"N{count}", delay=0)
                        count += 1
                    elif drawing:  
                        if node != drawing[0]:  
                            if (w := get_weight()): graph.add_edge(drawing[0], node, weight=w)
                        drawing = selected = None
                    else:  
                        selected, drawing = node, (node, None)
                elif event.button == 3 and not node:  
                    num = sum(1 for n in graph.nodes if 'E' in graph.nodes[n]['label']) + 1
                    graph.add_node(event.pos, pos=event.pos, label=f"E{num}", delay=0)
            elif event.type == KEYDOWN:  
                pos = pygame.mouse.get_pos()  
                node = getNode(graph, pos)  
                if event.key == K_d and node:  
                    graph.remove_node(node)
                    selected = drawing = None
                elif event.key == K_e:  
                    selected = drawing = None
                elif event.key == K_b and node:  
                    if node in obstacles: obstacles.remove(node)
                    else: obstacles.add(node)

def main():
    graph = start = None  
    mode = "select"  
    while True:
        clock.tick(60)  
        if mode == "select":

            screen.fill((240,240,245))  
            text = font.render("Choose Graph", True, black)  
            screen.blit(text, text.get_rect(center=(win_width//2, win_height//2-100)))  

            default = pygame.Rect(win_width//2-225, win_height//2-30, 200, 60)  
            custom = pygame.Rect(win_width//2+25, win_height//2-30, 200, 60)  

            for btn,txt in [(default,"Default"),(custom,"Custom")]:  
                pygame.draw.rect(screen, gray, btn)  
                pygame.draw.rect(screen, black, btn, 2)  
                text = font.render(txt, True, black)  
                screen.blit(text, text.get_rect(center=btn.center))  

            pygame.display.flip()  

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()  
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    if default.collidepoint(event.pos):  
                        graph, mode = DefaultGraph(), "view"
                    elif custom.collidepoint(event.pos):  
                        graph, mode = edit(nx.Graph()), "view"

        elif mode == "view":
            if not start:
                start = next(iter(graph.nodes()))  
                exits = [n for n in graph.nodes() if 'E' in graph.nodes[n]['label']]  
                buttons = {pos: {'label': data['label'], 'selected': pos == start, 'rect': None} 
                          for pos, data in graph.nodes(data=True) if 'E' not in data['label']}  
                paths = []  
                times = []  
                for exit in exits:  
                    path, time = find(graph, start, exit)
                    paths.append(path)
                    times.append(time)

            draw(graph, paths, times, buttons)  
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()  
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    pos = event.pos  
                    for node_pos, btn in buttons.items():
                        if btn['rect'] and btn['rect'].collidepoint(pos):  
                            start = node_pos  
                            for b in buttons.values(): b['selected'] = False  
                            btn['selected'] = True  
                            paths = []  
                            times = []  
                            for exit in exits:  
                                path, time = find(graph, start, exit)
                                paths.append(path)
                                times.append(time)
                            break
                    node = getNode(graph, pos)  
                    if node:
                        if event.button == 1:  
                            if node in obstacles: obstacles.remove(node)
                            else: obstacles.add(node)
                        elif event.button == 4:  
                            graph.nodes[node]['delay'] += 1
                        elif event.button == 5:  
                            graph.nodes[node]['delay'] = max(0, graph.nodes[node]['delay']-1)
                    else:

                        edge = getEdge(graph, pos)  
                        if edge and event.button in [1,3]:  
                            if edge in blocked_edges or (edge[1],edge[0]) in blocked_edges:
                                blocked_edges.discard(edge)
                                blocked_edges.discard((edge[1],edge[0]))
                            else:
                                blocked_edges.add(edge)

                    if node or edge:
                        paths = []  
                        times = []  
                        for exit in exits:  
                            path, time = find(graph, start, exit)
                            paths.append(path)
                            times.append(time)

if __name__ == "__main__":
    obstacles = set()  
    blocked_edges = set()  
    main()  