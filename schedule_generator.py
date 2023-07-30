from Documents.excel_controller import retrieve_company_postcodes, retrieve_break_times, write_to_excel, clean_excel
from itertools import permutations
from Maps.duration_matrix import compute_duration_matrix
from sys import maxsize

# initialize global variables
AVERAGE_COMPANY_COST = 15 * 60  # 15min
LONGER_COMPANY_COST = 20 * 60  # 20min
LUNCH_COST = 60 * 60  # 1hr
TEA_COST = 45 * 60  # 45min
MAX_DEVIATION = 60 * 60  # 1hr
MAX_COST_DAILY = (11 * 60 * 60) - (60 + 45) * 60  # 11hr - lunch(1hr) - tea (45min)
SCHEDULE_DAYS = 8


"""
    Calculates (n -1) Hamiltonian paths between all source arguement and all other vertices, and shortlists the path 
    for each vertex with the shortest duration. 
"""
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

    return [shortest_path, min_path]


"""
    Retrieves pertinent information from input.xslx, cleans up output.xslx, and creates a mapping between postal codes 
    of companies and node_indices for easier reference in other methods 
"""
def preprocessing():
    # ensure past output is cleared from the excel output.xslx sheet
    clean_excel()

    # retrieve postal codes from input.xslx
    profitable_companies, unprofitable_companies = retrieve_company_postcodes()

    # establish mapping for {node_index : [postal_code, num_visits_todo]}
    node_postalcode_mapping = {}
    for index in range(len(unprofitable_companies)):
        node_postalcode_mapping[index] = [unprofitable_companies[index], 24]
    for index in range(len(profitable_companies)):
        node_postalcode_mapping[len(unprofitable_companies) + index] = [profitable_companies[index], 16]

    # compute duration matrix from postcode list
    # postcode_list will be sorted by unprofitable companies > profitable companies for easier reference
    postcode_list = unprofitable_companies + profitable_companies
    matrix = compute_duration_matrix(postcode_list)

    return profitable_companies, unprofitable_companies, node_postalcode_mapping, matrix

"""
    Inserts periods for more profitable companies, after computing the shortest Hamiltonian path between them, into 
    the baseline schedule. 
"""
def schedule_filler(path, sublist):
    sublist_collection = []
    for a_index in range(len(path)):
        longest_sublist = []
        if path[a_index] in sublist:
            b_start = sublist.index(path[a_index])
            b_index = b_start
            while path[a_index] == sublist[b_index]:
                longest_sublist.append(path[a_index])
                if b_index + 1 < len(sublist) and a_index + 1 < len(path):
                    a_index += 1
                    b_index += 1
                else:
                    break
            sublist_collection.append([longest_sublist, a_index])

    last_value = sorted(sublist_collection, key=lambda x: len(x[0]), reverse=True)[0][0][-1]
    sublist_index = sublist.index(last_value)
    values_to_add = []

    for i in range(1, 5):
        values_to_add.append(sublist[sublist_index + i])

    insertion_point = sorted(sublist_collection, key=lambda x: len(x[0]), reverse=True)[0][1]

    return values_to_add, insertion_point

"""
    Main function to generate the 8-day schedule and write onto the output.xslx.
"""
def schedule_generator():
    profitable_companies, unprofitable_companies, node_postalcode_mapping, matrix = preprocessing()

    # compute the shortest path between unprofitable companies
    unprofitable_shortest_paths = []
    for source in range(len(unprofitable_companies)):
        unprofitable_shortest_paths.append(
            shortest_tour([sublist[:len(unprofitable_companies)] for sublist in matrix[:len(unprofitable_companies)]],
                          source=source))
    unprofitable_shortest_path = sorted(unprofitable_shortest_paths, key=lambda x: x[1])[0]

    # compute the shortest tour through all vertices originating from difference source vertex
    shortest_tours = []
    for source in range(len(matrix)):
        shortest_tours.append(shortest_tour(matrix, source=source))
    sorted_shortest_tours = sorted(shortest_tours, key=lambda x: x[1])

    # assign baseline schedule for each day
    schedule = []
    for day in range(SCHEDULE_DAYS):
        company_path = sorted_shortest_tours[day].copy()
        # compute total duration of tour and total time spent on company visits
        company_path[1] = company_path[1] + LONGER_COMPANY_COST + (len(company_path[0]) - 1) * AVERAGE_COMPANY_COST
        for key, value in node_postalcode_mapping.items():
            node_postalcode_mapping[key] = [value[0], value[1] - 1]
        schedule.append(company_path)

    baseline_schedule = schedule.copy()

    # append visits to profitable companies to bring all weights down to length of schedule i.e. 8
    # locate subset of unprofitable_shortest_tour in each sequence in baseline schedule, append full
    # unprofitable_shortest_tour on 1st subset occurrence
    for index in range(len(schedule)):
        company_path = schedule[index][0].copy()
        duration = schedule[index][1]

        values_to_add, insertion_point = schedule_filler(company_path, unprofitable_shortest_path[0] * 2)

        if insertion_point == len(company_path) - 1:
            company_path.extend(values_to_add)
        else:
            company_path[insertion_point:insertion_point] = values_to_add
        duration += len(unprofitable_shortest_path) * AVERAGE_COMPANY_COST

        schedule[index][0] = company_path
        schedule[index][1] = duration

    # append TSP cycle originating from the last company in schedule of each day
    for index in range(len(schedule)):
        company_path = schedule[index][0].copy()
        duration = schedule[index][1]

        last_company = company_path[-1]
        nearest_point_position = matrix[last_company].index(min(matrix[last_company]))

        company_path.extend(shortest_tours[nearest_point_position][0])
        duration += shortest_tours[nearest_point_position][1] + \
                    len(shortest_tours[nearest_point_position][0]) * AVERAGE_COMPANY_COST

        schedule[index][0] = company_path
        schedule[index][1] = duration

    # convert company_indices back to postal code mappings
    # append lunch and tea timeslots
    lunch_period, tea_period = retrieve_break_times()
    for index in range(len(schedule)):
        final_company_path = []
        company_path = schedule[index][0].copy()
        duration = schedule[index][1]

        for company_index in company_path:
            final_company_path.append(str(node_postalcode_mapping[company_index][0]))

        final_company_path.insert(lunch_period - 1, "Lunch")
        final_company_path.insert(tea_period - 1, "Tea")

        duration += LUNCH_COST + TEA_COST

        write_to_excel(final_company_path, duration)


if __name__ == '__main__':
    schedule_generator()
