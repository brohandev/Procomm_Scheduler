from Documents.excel_controller import retrieve_company_postcodes
from itertools import permutations
from Maps.duration_matrix import compute_duration_matrix
from prettyprinter import pprint as pp
from sys import maxsize

MAX_COST = 11 * 60 * 60


def shortest_tour(matrix, source):
    # store all vertices apart from source vertex
    vertex = []
    for company in range(len(matrix)):
        if company != source:
            vertex.append(company)

    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    path_permutations_list = permutations(vertex)
    shortest_path = []

    for path_tuple in path_permutations_list:

        # store current path weight(cost)
        current_pathweight = 0

        # compute current path weight
        k = source
        for j in path_tuple:
            current_pathweight += matrix[k][j]
            k = j

        # update minimum
        if current_pathweight < min_path:
            min_path = current_pathweight
            shortest_path = [source] + list(path_tuple)

    return shortest_path, min_path


def preprocessing():
    # retrieve_supervisor_requirements()

    # retrieve postal codes from input.xslx
    profitable_companies, unprofitable_companies = retrieve_company_postcodes()

    # sort postcode_list to have least profitable companies in front and most profitable companies at the back
    postcode_list = unprofitable_companies + profitable_companies

    # compute duration matrix from postcode list
    matrix = compute_duration_matrix(postcode_list)

    # initialize number of times to visit each company
    company_weights = len(unprofitable_companies) * [24] + len(profitable_companies) * [16]

    shortest_paths = []
    for source in range(len(matrix)):
        shortest_paths.append(shortest_tour(matrix, source=source))
    pp(shortest_paths)


def generate_schedule():
    # process_nodes()
    # compute_hamiltonian_paths()
    # compute_schedule()
    pass


if __name__ == '__main__':
    preprocessing()
    generate_schedule()
    pass
