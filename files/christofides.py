import networkx
import branchAndBound

def christofides(coord, edgesWeight):
    adjacencyList = networkx.from_numpy_array(edgesWeight) #crio grafo
    minimumSpanningTree = networkx.minimum_spanning_tree(adjacencyList, algorithm='kruskal') #encontro arvore geradora minima

    vertexDegrees = [0 for i in range(0, len(minimumSpanningTree)) ] 
    
    #acho todos os graus dos vertices
    for i in minimumSpanningTree.edges:
        vertexDegrees[i[0]] += 1
        vertexDegrees[i[1]] += 1
    
    #acho vertices de grau impar
    vertexOddDegrees = []
    for i in range(len(vertexDegrees)):
        if (vertexDegrees[i] % 2 == 1 and not(vertexOddDegrees.__contains__(i))):
            vertexOddDegrees.append(i)

    subgraphOddDegrees = adjacencyList.subgraph(vertexOddDegrees) # crio subgrafo com os vertices de grau impar

    minMatching = networkx.min_weight_matching(subgraphOddDegrees) #encontro o matching de peso minimo entre os vertices de grau impar
    
    multigraph = networkx.MultiGraph(minMatching) #crio um multigrafo com as arestas do matching e da AGM
    for i in minimumSpanningTree.edges:
        multigraph.add_edge(i[0], i[1])
    
    E = networkx.eulerian_circuit(multigraph, source=1) #encontro o circuito euleriano e então removo todos os vertices repetidos (formo ciclo hamiltoniano)
    
    eulerianCircuit = (list(E))

    hamiltonianCycle = []
    for i in eulerianCircuit:
        if not(hamiltonianCycle.__contains__(i[0])):
            hamiltonianCycle.append(i[0])
        if not(hamiltonianCycle.__contains__(i[1])):
            hamiltonianCycle.append(i[1])
    
    hamiltonianCycle.append(1) #adiciono vertice inicial ao final da solucao

    weightSol = 0
    for i in range(len(hamiltonianCycle)-1):
        weightSol += (branchAndBound.calculateCost(coord[hamiltonianCycle[i]], coord[hamiltonianCycle[i+1]]))

    return hamiltonianCycle, weightSol