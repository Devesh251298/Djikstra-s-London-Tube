from tube.map import TubeMap

class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code into several sub-methods, if needed)
    """


    def __init__(self):
        pass

    def build(self, tubemap):
        """ 
            Builds a graph encoding neighbouring connections between stations.

            ----------------------------------------------
                
            Args:
                tubemap (TubeMap) : tube map serving as a reference for building
                        the graph.

            Returns:
                graph (dict) : as described above.
                        If the input data (tubemap) is invalid,
                        the method should return an empty dict.
        """
        if not isinstance(tubemap, TubeMap):
            return {}
        graph = {}
        for i in range(len(tubemap.connections)):
            stations = [station.id for station in
                        tubemap.connections[i].stations]
            if stations[0] not in graph.keys():
                graph[stations[0]] = {stations[1]: [tubemap.connections[i]]}
            else:
                if stations[1] not in graph[stations[0]].keys():
                    graph[stations[0]][stations[1]] = [tubemap.connections[i]]
                else:
                    graph[stations[0]][stations[1]].append(
                        tubemap.connections[i])

            if stations[1] not in graph.keys():
                graph[stations[1]] = {stations[0]: [tubemap.connections[i]]}
            else:
                if stations[0] not in graph[stations[1]].keys():
                    graph[stations[1]][stations[0]] = [tubemap.connections[i]]
                else:
                    graph[stations[1]][stations[0]].append(
                        tubemap.connections[i])
        return dict(graph)


def test_graph():

    tubemap = TubeMap()
    tubemap.import_from_json("../data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build([1])

    print(graph)


if __name__ == "__main__":
    test_graph()
