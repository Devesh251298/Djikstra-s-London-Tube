from graph import NeighbourGraphBuilder
import sys
sys.path.append("../tube")
sys.path.append("../")
from tube import *

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide your code into several sub-methods)
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        self.name_map = {}
        for i in self.tubemap.stations.keys():
            self.name_map[self.tubemap.stations[i].name] = i


        
        # Feel free to add anything else needed here.
            
    def search_list(self, arr, ele, dict):
        if len(arr)==0:
            return 0
        if len(arr)==1:
            if ele >= dict[arr[0]]:
                return 1
            else:
                return 0
        if ele >= dict[arr[len(arr)//2]]:
            return len(arr)//2 + self.search_list(arr[len(arr)//2:],ele, dict)
        else:
            return self.search_list(arr[:len(arr)//2],ele, dict)

    def get_shortest_path(self, start_station_name, end_station_name):
        start_id = self.name_map[start_station_name]
        end_id = self.name_map[end_station_name]

        if start_id not in self.graph.keys() or end_id not in self.graph.keys():
            return None

        scores = {start_id : 0}
        sorted_list = [start_id]
        end_detached = False
        start_point = start_id
        shortest_path = 0
        previous = {}
        prev_connection = {}
        completed =  set()

        while not end_detached:
            sorted_list.pop(0)
            completed.add(start_point)
            for i in self.graph[start_point].keys():
                if i in completed:
                    continue
                if len(self.graph[start_point][i])==1:
                    time = self.graph[start_point][i][0].time
                    prev = self.graph[start_point][i][0]
                else:
                    time = float("inf")
                    prev = []
                    for j in self.graph[start_point][i]:
                        if j.time < time:
                            time = j.time
                            prev = j

                if i not in scores.keys():
                    val = scores[start_point]+time
                    previous[i] = start_point
                    prev_connection[i] = prev
                    scores[i] = val
                else:
                    if val < scores[i]:
                        scores[i] = val
                        previous[i] = start_point
                        prev_connection[i] = prev
                sorted_list.insert(self.search_list(sorted_list, val, scores), i)
            start_point = sorted_list[0]  
            if start_point == end_id:
                end_detached = True
                shortest_path = scores[end_id]

        id = end_id
        stations = []
        connections = []
        while id!=start_id:
            connections.append(prev_connection[id])
            id = previous[id]

        start_station = Station(name = start_station_name, id = "", zones = [])
        for i in range(len(connections)-1,-1,-1):
            for j in connections[i].stations:
                if j.name == start_station.name:
                    stations.append(j)
                else:
                    start_station_hold = j
            start_station = start_station_hold
        stations.append(start_station)
        """ Find ONE shortest path (in terms of duration) from start_station_name to end_station_name.

        For instance, get_shortest_path('Stockwell', 'South Kensington') should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.

        You can use the Dijkstra algorithm to find the shortest path from start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not exist.
        """

        return stations  # TODO


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()

    tubemap.import_from_json("../data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Stockwell", "South Kensington")
    print(stations)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    print(stations)
    
    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected


if __name__ == "__main__":
    test_shortest_path()
