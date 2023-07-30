from prettyprinter import pprint as pp

matrix = [
    [-1, 689, 1185, 1172, 764, 891, 734, 753, 837, 766],
    [614, -1, 1127, 1016, 1070, 1198, 1041, 1059, 1144, 985],
    [1188, 1257, -1, 651, 675, 692, 747, 766, 737, 467],
    [1166, 1059, 524, -1, 987, 1003, 1059, 1078, 1048, 779],
    [768, 1178, 1006, 1153, -1, 287, 243, 262, 232, 377],
    [991, 1248, 1001, 1148, 525, -1, 396, 440, 599, 279],
    [688, 1099, 1048, 1158, 222, 322, -1, 137, 296, 348],
    [725, 1135, 1085, 1195, 259, 376, 161, -1, 333, 402],
    [810, 1220, 1059, 1206, 216, 339, 285, 304, -1, 429],
    [806, 1216, 866, 1091, 208, 224, 280, 299, 270, -1]
]

# matrix = [sublist[0:4] for sublist in matrix[0:4]]
# pp(matrix)

if __name__ == '__main__':
    path = [5, 9, 4, 8, 6, 7, 0, 1, 3, 2]
    sublist = [0, 1, 3, 2, 0, 1, 3, 2]

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

    pp(values_to_add)
    pp(insertion_point)
