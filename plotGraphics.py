import matplotlib.pyplot as plt

vertices = [52, 70, 107, 124, 200, 318, 575, 724, 1084, 1577, 1889, 2152, 2392]

# Grafico das solucoes encontradas
optimal = [7542, 675, 44303, 59030, 29437, 42029, 6773, 41910, 239297, 22249, 316536, 64253, 378032]
values_christofides = [8235.198, 775.039, 48379.607, 63071.622, 32045.584, 47643.238, 7594.845, 46770.281, 258620.572, 24054.873, 343073.261, 72000.007, 416299.652]
values_twice_around_the_three = [10116.014, 873.351, 54238.036, 74140.959, 40030.866, 58145.441, 9438.933, 57779.667, 315268.348, 31223.096, 449811.488, 95076.215, 523132.906]

plt.figure(figsize=(10, 6))
plt.plot(vertices, optimal, marker='o', label='Ótimo', linestyle='-', color='blue')
plt.plot(vertices, values_christofides, marker='o', label='Christofides', linestyle='-', color='green')
plt.plot(vertices, values_twice_around_the_three, marker='o', label='Twice Around the Three', linestyle='-', color='red')

plt.xlabel('Número de Vértices')
plt.ylabel('Valores')
plt.title('Comparação de Algoritmos')
plt.legend()

plt.grid(True)
plt.show()

# Grafico de tempo
time_christofides = [0.309, 0.274, 0.317, 0.331, 1.187, 3.347, 11.035, 18.714, 30.156, 41.940, 53.440, 131.348, 405.337]

time_twice_around_the_three = [0.187, 0.221, 0.198, 0.300, 0.508, 0.802, 3.194, 5.056, 5.316, 10.874, 16.811, 21.650, 27.809]

plt.figure(figsize=(12, 6))
plt.plot(vertices, time_christofides, marker='o', label='Christofides', linestyle='-', color='green')
plt.plot(vertices, time_twice_around_the_three, marker='o', label='Twice Around the Three', linestyle='-', color='red')

plt.xlabel('Número de Vértices')
plt.ylabel('Tempo (s)')
plt.title('Comparação de Tempos')
plt.legend()

plt.grid(True)
plt.show()

# Grafico de memória
memory_christofides = [436.859, 449.140, 314.718, 454.648, 430.957, 452.093, 425.92, 530.464, 648.375, 1000.875, 1366.0, 1709.890, 2067.632]
memory_twice_around_the_three = [476.234, 449.140, 314.718, 454.648, 776.968, 458.0, 698.078, 953.101, 663.480, 722.273, 1224.746, 1171.320, 1389.375]

plt.figure(figsize=(12, 6))
plt.plot(vertices, memory_christofides, marker='o', label='Christofides', linestyle='-', color='green')
plt.plot(vertices, memory_twice_around_the_three, marker='o', label='Twice Around the Three', linestyle='-', color='red')

plt.xlabel('Número de Vértices')
plt.ylabel('Memória (MB)')
plt.title('Comparação de Memória')
plt.legend()

plt.grid(True)
plt.show()