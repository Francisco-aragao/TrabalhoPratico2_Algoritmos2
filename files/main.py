import numpy as np

import branchAndBound
import christofides 
import twiceArroundTheTree

import time
import os

from memory_profiler import memory_usage
from functools import partial

#funções chamando os métodos de resolução do problema do caixeiro viajante
def TSP_BranchAndBound(coord, vertexNumber):
    start_time = time.time()

    maxMemory, solution = memory_usage(partial(branchAndBound.branchAndBound, coord, vertexNumber), interval=1.0, max_usage=True, retval=True)
    end_time = time.time()

    print(f"Tempo gasto Branch and Bound: {end_time - start_time} seconds")
    print("Maximo uso memória ", maxMemory)

    print("solução branch and bound ", solution[1])
    print("peso branch and bound ", solution[0])

# crio matriz com pesos de cada aresta dada as coordenadas dos vértices
def createEdgeDistances(coord, vertexNumber):
    edgesDistances = np.zeros((vertexNumber+1, vertexNumber+1), dtype=float)

    for i in (range(0, len(coord))):
        for j in (range(0, len(coord) )):
            if (i == 0 or j == 0):
                edgesDistances[i][j] = 0
            elif (i == j):
                edgesDistances[i][j] = 0
            else:
                edgesDistances[i][j] = branchAndBound.calculateCost(coord[i], coord[j])
    return edgesDistances

def TSP_TwiceAroundTheTree(coord, vertexNumber):
    edgesDistances = createEdgeDistances(coord, vertexNumber)
    
    start_time = time.time()

    maxMemory, solution = memory_usage(partial(twiceArroundTheTree.twiceAroundTheTree, coord, edgesDistances), interval=1.0, max_usage=True, retval=True)

    end_time = time.time()

    print(f"\nTempo gasto Twice around the Tree: {end_time - start_time} seconds")
    print("Maximo uso memória ", maxMemory)

    print("solucao twice around the tree ", solution[1])
    print("peso twice around the tree ", solution[0])
    return

def TSP_Christofides(coord, vertexNumber):
    edgesDistances = createEdgeDistances(coord, vertexNumber)
    
    start_time = time.time()

    maxMemory, solution = memory_usage(partial(christofides.christofides, coord, edgesDistances), interval=1.0, max_usage=True, retval=True)

    end_time = time.time()

    print(f"\nTempo gasto Christofides: {end_time - start_time} seconds")
    print("Maximo uso memória ", maxMemory)

    print("solucao christofides ", solution[1])
    print("peso christofides ", solution[0])
    return


weights = 0

folderPath = 'data/' # os arquivos de entrada precisam estar na pasta 'data'
files = os.listdir(folderPath)

# Leio cada arquivo da pasta data
for eachFile in files:
    
    completFilePath = os.path.join(folderPath, eachFile)

    if os.path.isfile(completFilePath):

        with open(completFilePath, 'r') as file:

            for _ in range(3): # não leio informacoes adicionais do arquivo
                next(file)
            
            vertexNumber = 0
            for line in file:
                print(line)
                values = line.split()
                vertexNumber = int(values[-1]) # leio numero de vertices
                break

            print("Número de vértices ", vertexNumber)

            coord = np.array([ #vetor de coordenadas de cada vertice
                {"coordX": 0, "coordY": 0} for _ in range(vertexNumber+1)
            ])
 
            for _ in range(2): #ignoro proximas duas linhas da entrada
                next(file)

            for line in file:  #leio coordenadas
                if (line.startswith("EOF")):
                    break
                values = line.split()
                vertex = int(values[0])
                coordX = float(values[1])
                coordY = float(values[2])
                coord[vertex]['coordX'] = coordX
                coord[vertex]['coordY'] = coordY
        
        TSP_BranchAndBound(coord, vertexNumber)
        TSP_TwiceAroundTheTree(coord, vertexNumber) 
        TSP_Christofides(coord, vertexNumber)
