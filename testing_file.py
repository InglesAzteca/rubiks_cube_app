# from main import DetermineAlgorithm, read_state_from_text_file
#
# c, a = read_state_from_text_file("algorithms/solved")
#
# d = DetermineAlgorithm()
#
# alg = d.search_through_f2l_algorithms(c)
# print(alg)

from main import CubeColoring

c = CubeColoring()
print(c.edge_indices["top"] + c.edge_indices["middle"])

# x = ["U2"]
# y = x[0].replace("1", "")
# print(y)
