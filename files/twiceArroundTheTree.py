import networkx
import branchAndBound

def twiceAroundTheTree(coord, edgesWeight):
    adjacencyList = networkx.from_numpy_array(edgesWeight) # crio grafo
    minimumSpanningTree = networkx.minimum_spanning_tree(adjacencyList, algorithm='kruskal') # encontro arvore geradora minima

    H = networkx.dfs_preorder_nodes(minimumSpanningTree, source=1) # caminho pelos vertices da arvore geradora minima
    hamiltonianCycle = list(H) 
    hamiltonianCycle.append(1) #adiciono vertice inicial ao final da solucao

    weightSol = 0
    for i in range(len(hamiltonianCycle)-1):
        weightSol += (branchAndBound.calculateCost(coord[hamiltonianCycle[i]], coord[hamiltonianCycle[i+1]]))

    return hamiltonianCycle, weightSol