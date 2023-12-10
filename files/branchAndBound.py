import heapq
from math import sqrt
import numpy as np

import time

# classe nó para facilitar o algoritmo
class Node:
    def __init__(self, solution, estimative, level, minEdgesGraph, cost):
        self.solution = solution
        self.estimative = estimative
        self.cost = cost
        self.level = level
        self.minEdgesGraph = minEdgesGraph

    def __lt__(self, nodeToCompare) : # preciso definir como comparar nós
        if self.estimative != nodeToCompare.estimative:
            return self.estimative < nodeToCompare.estimative
        return self.cost < nodeToCompare.cost

# calculo distancias entre vertices
def calculateCost(a, b):
    return sqrt(  ((b['coordX'] - a['coordX'])**2) + ((b['coordY'] - a['coordY'])**2) )

# encontro menores arestas de cada vértice
def minimiumEdges(vertexPosition, vertexNumber, coord):
    edge1 = 100000000000
    edge2 = 100000000000
    position1 = 0
    position2 = 0

    for i in range(1, vertexNumber+1):
        if (i == vertexPosition):
            continue
        cost = calculateCost(coord[vertexPosition], coord[i])
        if (cost < edge1):
            edge2 = edge1
            edge1 = cost
            edge1 = cost
            position2 = position1
            position1 = i
        elif (cost < edge2):
            edge2 = cost
            position2 = i

    return (edge1, position1, edge2, position2)

# encontro estimativa inicial (menores arestas de cada vértice)
def findFirstEstimative(coord, vertexNumber):
    estimative = 0
    minCostsAllVertex = np.array([
        {"edge1": {"vertex": 0, "cost": 0}, "edge2": {"vertex": 0, "cost": 0}} for _ in range(vertexNumber+1)
    ])

    for i in range(1, vertexNumber+1):
        edge1, position1, edge2, position2 = minimiumEdges(i, vertexNumber, coord)
        minCostsAllVertex[i]['edge1']['cost'] = edge1
        minCostsAllVertex[i]['edge1']['vertex'] = position1
        minCostsAllVertex[i]['edge2']['cost'] = edge2
        minCostsAllVertex[i]['edge2']['vertex'] = position2
        estimative += edge1 + edge2

    return estimative/2, minCostsAllVertex

# calculo nova estimativa com base no novo vertice a ser considerado na solução
def newBound(oldEstimative, newVertex, pathChoices, coord, minCostsAllVertex):
    lastVertexChosed = pathChoices[-1]

    newCostToNewVertex = calculateCost(coord[lastVertexChosed], coord[newVertex])

    newEstimative = oldEstimative * 2

    newCostsEdges = np.array(minCostsAllVertex)

    # faço as verificacoes necessárias para alterar somente o custo de adicionar a aresta do novo vértice ao calculo da estimativa
    if (newCostsEdges[lastVertexChosed]['edge1']['vertex'] != newVertex and \
        newCostsEdges[lastVertexChosed]['edge2']['vertex'] != newVertex):
            if (newCostsEdges[lastVertexChosed]['edge2']['cost'] < newCostsEdges[lastVertexChosed]['edge1']['cost']):
                newEstimative -= newCostsEdges[lastVertexChosed]['edge1']['cost']

                newCostsEdges[lastVertexChosed]['edge1']['cost'] = newCostToNewVertex
                newCostsEdges[lastVertexChosed]['edge1']['vertex'] = newVertex

                newEstimative += newCostToNewVertex
            else:
                newEstimative -= newCostsEdges[lastVertexChosed]['edge2']['cost']

                newCostsEdges[lastVertexChosed]['edge2']['cost'] = newCostToNewVertex
                newCostsEdges[lastVertexChosed]['edge2']['vertex'] = newVertex

                newEstimative += newCostToNewVertex

    if (newCostsEdges[newVertex]['edge1']['vertex'] != lastVertexChosed and \
        newCostsEdges[newVertex]['edge2']['vertex'] != lastVertexChosed):
            if (newCostsEdges[newVertex]['edge2']['cost'] < newCostsEdges[newVertex]['edge1']['cost']):
                newEstimative -= newCostsEdges[newVertex]['edge1']['cost']

                newCostsEdges[newVertex]['edge1']['cost'] = newCostToNewVertex
                newCostsEdges[newVertex]['edge1']['vertex'] = lastVertexChosed

                newEstimative += newCostToNewVertex
            else:
                newEstimative -= newCostsEdges[newVertex]['edge2']['cost']

                newCostsEdges[newVertex]['edge2']['cost'] = newCostToNewVertex
                newCostsEdges[newVertex]['edge2']['vertex'] = lastVertexChosed
                
                newEstimative += newCostToNewVertex

    return (newEstimative / 2, newCostsEdges)    

# algoritmo de branch and bound 
def branchAndBound(coord, vertexNumber):
    start_time = time.time()

    estimative, minEdgesGraph = findFirstEstimative(coord, vertexNumber)
    root = Node(solution=[1], estimative=estimative, level=1, minEdgesGraph=minEdgesGraph, cost=0)

    prirorityQueue = [root]
    heapq.heapify(prirorityQueue)

    bestSolution = np.inf
    solution = []

    while len(prirorityQueue) > 0:
        
        currentNode = heapq.heappop(prirorityQueue)

        if currentNode.level > vertexNumber:    # encontrei nova melhor solução
            if bestSolution > currentNode.cost:
                bestSolution = currentNode.cost
                solution = currentNode.solution
        
        elif (currentNode.estimative < bestSolution):
            time_now = time.time()
            if (time_now - start_time > 1800):
                print("Não resolvi em menos de 30 minutos")
                return solution, bestSolution
            
            if currentNode.level < vertexNumber: # se não cheguei em folha, calculo novas estimativas
                for k in range(1, vertexNumber+1):
                    if not(currentNode.solution.__contains__(k)):
                        estimativeWithK, newChosedEdges = newBound(currentNode.estimative, k, currentNode.solution, coord, currentNode.minEdgesGraph) 
                        if (estimativeWithK < bestSolution):
                            costToUseK = calculateCost(coord[currentNode.solution[-1]], coord[k])
                            
                            newNode = Node(solution=currentNode.solution + [k], estimative=estimativeWithK, level=currentNode.level + 1, minEdgesGraph=newChosedEdges, cost=(costToUseK + 
                            currentNode.cost))
                            
                            heapq.heappush(prirorityQueue, newNode)

            elif (currentNode.solution[-1] != 1): # analiso caso em que já tenho algum vértice além do inicial na solução

                finalEstimative, finalEdges = newBound(currentNode.estimative, 1, currentNode.solution, coord, currentNode.minEdgesGraph) 

                if finalEstimative < bestSolution and currentNode.level == vertexNumber:
                    costToBegin = calculateCost(coord[currentNode.solution[-1]], coord[1]) # calculo custo do ultimo vertice escolhido indo até o inicial  

                    newNode = Node(solution=currentNode.solution + [1], estimative=finalEstimative, level=currentNode.level + 1, minEdgesGraph=finalEdges, cost=(costToBegin + 
                    currentNode.cost))
                    
                    heapq.heappush(prirorityQueue, newNode)   

    return solution, bestSolution
