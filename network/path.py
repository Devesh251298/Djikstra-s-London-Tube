from graph import NeighbourGraphBuilder
import sys
sys.path.append("../tube")
sys.path.append("../")
from tube import *

class PathFinder:

    def __init__(self, tubemap):
        self.tubemap = tubemap
        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        # print(self.graph)
        self.name_map = {}
        for i in self.tubemap.stations.keys():
            self.name_map[self.tubemap.stations[i].name] = i
            
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

    def get_stations(self, connections, start_station_name):
        stations = []
        start_station = Station(name = start_station_name, id = "", zones = [])
        for i in range(len(connections)-1,-1,-1):
            for j in connections[i].stations:
                if j.name == start_station.name:
                    stations.append(j)
                else:
                    start_station_hold = j
            start_station = start_station_hold
        stations.append(start_station)
        return stations

    def djisktras(self, start_id, end_id, graph):
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
            # print(start_point, sorted_list)
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
                    val = scores[start_point]+time
                    if val < scores[i]:
                        scores[i] = val
                        previous[i] = start_point
                        prev_connection[i] = prev
                        sorted_list.remove(i)
                        sorted_list.insert(self.search_list(sorted_list, val, scores), i)

                if i not in sorted_list:
                    sorted_list.insert(self.search_list(sorted_list, val, scores), i)
            start_point = sorted_list[0]  
            if start_point == end_id:
                end_detached = True
                shortest_path = scores[end_id]

        return prev_connection, previous, shortest_path

    def get_shortest_path(self, start_station_name, end_station_name):
        start_id = self.name_map[start_station_name]
        end_id = self.name_map[end_station_name]

        if start_id not in self.graph.keys() or end_id not in self.graph.keys():
            return None

        if start_id == end_id:
            for i in self.graph[start_id].keys():
                time = float("inf")
                nearest = []
                for j in self.graph[start_id][i]:
                    if j.time < time:
                        time = j.time
                        nearest = j
            stations = self.get_stations([nearest], start_station_name)
            stations.append(stations[0])
            return stations

        prev_connection, previous, shortest_path = self.djisktras(start_id, end_id, self.graph) 
        id = end_id
        connections = []
        while id!=start_id:
            connections.append(prev_connection[id])
            id = previous[id]

        return self.get_stations(connections, start_station_name) 


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
