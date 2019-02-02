import numpy as np
import math


class Graph:
    def __init__(self, vertex_count, adjacency_matrix=None):
        self.vertex_count = vertex_count
        if adjacency_matrix is None:
            self.adjacency_matrix = np.zeros(shape=(vertex_count, vertex_count))
        else:
            self.adjacency_matrix = adjacency_matrix


def transform_graph_into_covariation_matrix(graph):
    matrix_size = graph.vertex_count
    matrix_omega_waved = np.zeros(shape=(matrix_size, matrix_size))
    for i in range(matrix_size):
        for j in range(matrix_size):
            if i == j:
                matrix_omega_waved[i][j] = 1
            elif graph.adjacency_matrix[i][j] == 1:
                matrix_omega_waved[i][j] = np.random.uniform()
                if matrix_omega_waved[i][j] < 0.5:
                    matrix_omega_waved[i][j] -= 1

    matrix_a = np.zeros(shape=(matrix_size, matrix_size))
    for i in range(matrix_size):
        d_i = 0
        for k in range(matrix_size):
            if k != i:
                d_i += abs(matrix_omega_waved[i][k])
        if d_i != 0:
            for j in range(matrix_size):
                matrix_a[i][j] = 2 * matrix_omega_waved[i][j] / (3 * d_i)

    matrix_omega = (matrix_a + matrix_a.transpose()) / 2

    for i in range(matrix_size):
        for j in range(matrix_size):
            if i == j:
                matrix_omega[i][j] = 1
            elif abs(matrix_omega[i][j]) < 0.1:
                if matrix_omega[i][j] < 0:
                    matrix_omega[i][j] = -0.1
                elif matrix_omega[i][j] > 0:
                    matrix_omega[i][j] = 0.1

    matrix_omega_inverted = np.linalg.inv(matrix_omega)

    matrix_sigma = np.zeros(shape=(matrix_size, matrix_size))
    for i in range(matrix_size):
        for j in range(matrix_size):
            matrix_sigma[i][j] = matrix_omega_inverted[i][j] / math.sqrt(matrix_omega_inverted[j][j] * matrix_omega_inverted[i][i])

    return matrix_sigma


s = 3
edg = np.zeros(shape=(s, s))
edg[0][1] = 1
edg[1][0] = 1
edg[1][2] = 1
edg[2][1] = 0
a = Graph(s, edg)
print(transform_graph_into_covariation_matrix(a))