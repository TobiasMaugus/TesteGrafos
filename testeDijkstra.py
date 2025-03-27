def count_metrics(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()


    vertices = set()
    edges = set()
    arcs = set()
    required_vertices = set()
    required_edges = set()
    required_arcs = set()
    section = None

    for line in lines:
        line = line.strip()

        if line.startswith("ReN."):
            section = "ReN"
            continue
        elif line.startswith("ReE."):
            section = "ReE"
            continue
        elif line.startswith("EDGE"):
            section = "EDGE"
            continue
        elif line.startswith("ReA."):
            section = "ReA"
            continue
        elif line.startswith("ARC"):
            section = "ARC"
            continue

        if line and section:
            parts = line.split("\t")

            if section == "ReN":
                try:
                    node = int(parts[0].replace("N", ""))
                    demand = int(parts[1])
                    s_cost = int(parts[2])
                    aux = (node, (demand, s_cost))
                    required_vertices.add(aux) 
                    vertices.add(node)  
                except ValueError:
                    continue  

            elif section in ["ReE", "EDGE"]:
                try:
                    u, v = int(parts[1]), int(parts[2]) 
                    vertices.update([u, v]) #vertices q nao estavam em ReN
                    edge = (min(u, v), max(u, v)) 

                    t_cost = int(parts[3]) 

                    edges.add((edge, (t_cost))) 

                    if section == "ReE":
                        demand = int(parts[4]) 
                        s_cost = int(parts[5]) 
                        required_edges.add((edge, (t_cost, demand, s_cost)))
                except ValueError:
                    continue

            elif section in ["ReA", "ARC"]:
                try:
                    u, v = int(parts[1]), int(parts[2])
                    vertices.update([u, v]) #vertices q nao estavam em ReN
                    arc = (u, v)
                    t_cost = int(parts[3]) 

                    arcs.add((arc, (t_cost)))
                    if section == "ReA":
                        demand = int(parts[4]) 
                        s_cost = int(parts[5]) 
                        required_arcs.add((arc, (t_cost, demand, s_cost)))
                except ValueError:
                    continue

    return vertices, edges, arcs, required_vertices, required_edges, required_arcs


def calcula_graus(vertices, edges, arcs):
    graus = {}
    
    for v in vertices:
        graus[v] = [0, 0, 0]
        #[grau, grau de entrada, grau de saída]
       
    for (u, v), _ in edges:
        graus[u][0] += 1
        graus[v][0] += 1
    
    for (u, v), _ in arcs:
        graus[v][1] += 1  #grau entrada
        graus[u][2] += 1  #grau saida
        
    
    graus_set = tuple((v, tuple(degrees)) for v, degrees in graus.items())
    
    return graus_set

def calcula_densidade(NumVertices, NumEdges, NumArcs):
    edges_max=(NumVertices*(NumVertices-1))/2
    arcs_max=(NumVertices*(NumVertices-1))
    densidade = (NumEdges+NumArcs)/(edges_max+arcs_max)
    return densidade

def dijkstra(start_node, edges, arcs):
    # Inicializa as distâncias e os predecessores
    distancias = {start_node: 0}
    predecessores = {start_node: None}
    
    # Conjunto de nós não visitados
    nos_nao_visitados = set([start_node])
    
    # Enquanto houver nós não visitados
    while nos_nao_visitados:
        # Encontra o nó com a menor distância
        current_node = min(nos_nao_visitados, key=lambda node: distancias.get(node, float('inf')))
        
        
        # Remove o nó da lista de nós não visitados
        nos_nao_visitados.remove(current_node)

        # Verifica as arestas não direcionadas (edges)
        for (u, v), t_cost in edges:
            if u == current_node:
                neighbor = v
            elif v == current_node:
                neighbor = u
            else:
                continue
            
            # Atualiza a distância e o predecessor
            nova_distancia = distancias[current_node] + t_cost
            if neighbor not in distancias or nova_distancia < distancias[neighbor]:
                distancias[neighbor] = nova_distancia
                predecessores[neighbor] = current_node
                nos_nao_visitados.add(neighbor)  # Adiciona o nó vizinho à lista de não visitados
        
        # Verifica os arcos direcionados (arcs)
        for (u, v), t_cost in arcs:
            if u == current_node:
                neighbor = v
                nova_distancia = distancias[current_node] + t_cost
                if neighbor not in distancias or nova_distancia < distancias[neighbor]:
                    distancias[neighbor] = nova_distancia
                    predecessores[neighbor] = current_node
                    nos_nao_visitados.add(neighbor)  # Adiciona o nó vizinho à lista de não visitados
    
    return distancias, predecessores





file_path = "CBMix11.dat" 
vertices, edges, arcs, required_vertices, required_edges, required_arcs = count_metrics(file_path)
graus = calcula_graus(vertices, edges, arcs)
dist, pred = dijkstra(list(vertices)[3], edges, arcs)
print(dist)
print(pred)
print(calcula_densidade(len(vertices), len(edges), len(arcs)))

#TODO
# 1. Quantidade de vértices; OK
# 2. Quantidade de arestas; OK
# 3. Quantidade de arcos; OK
# 4. Quantidade de vértices requeridos; OK
# 5. Quantidade de arestas requeridas; OK
# 6. Quantidade de arcos requeridos; OK
# 7. Densidade do grafo (order strength) OK
# 8. Componentes conectados; OK
# 9. Grau mínimo dos vértices; OK?
# 10. Grau máximo dos vértices; OK?
# 11. Intermediação - Mede a frequência com que um nó aparece nos caminhos mais curtos;
# 12. Caminho médio;
# 13. Diâmetro;
#
# Importante: Muitas dessas métricas utilizam os resultados da matriz de caminhos mais curtos de múltiplas fontes.
# Assim, como um dos produtos da Etapa 1, é necessário desenvolver o algoritmo que gera tal matriz,
# assim como a matriz de predecessores.