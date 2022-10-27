from network.graph import NeighbourGraphBuilder
from tube.map import TubeMap
from tube.components import Station, Line, Connection

class PathFinder:

    def __init__(self, tubemap):
        self.tubemap = tubemap
        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        self.name_map = {}
        for i in self.tubemap.stations.keys():
            self.name_map[self.tubemap.stations[i].name] = i
            
    def search_list(self, arr, ele, dict):
        ''' search_list is a binary search algorithm which goes through all the keys in
            the array of keys whose values are available in the form of a dictionary and 
            eventually return the position where the element should go in that list.

            Args:
                arr : the key array,
                ele : element to insert,
                dict : key value mapping for keys in array arr

            Returns:
                postion of the element in arr
        '''
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
        '''
            get_stations take the shortest path connections extracted from the 
            djisktra's algorithm and return them as a list of stations

            Args:
                connections : List of connections extracted from Djisktra's,
                start_station_name : Name of the start station

            Returns:
                stations : List of sequence of stations in all the connections
        '''
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
        '''
            djisktras take the start and end station ids along with the graph and
            return a list of connections that lead to the shortest path

            Args:
                start_id : start station id,
                end_id : end station id,
                graph : network graph

            Returns:
                prev_connection : prev_connections of different station ids along 
                shortest path
                previous : the previous id of different station ids along the 
                shortest path 
                shortest_path : length of the shortest path
        '''
        ## stores current minimum path length for each explored stations
        scores = {start_id : 0}
        ## stores all the explored stations
        explored_stations = [start_id]
        ## bool variable that checks if the end station is detached
        end_detached = False
        start_point = start_id
        shortest_path = 0
        ## stores current previous station in the shorted path for a station
        previous = {}
        ## stores current previous connection in the shorted path for a station
        prev_connection = {}
        ## stores all the stations which are poped from explored stations
        completed =  set()

        while not end_detached:
            explored_stations.pop(0)
            completed.add(start_point)
            ## This loop goes through all the possible path from start_point and 
            ## adds them to the explored nodes and updates their path length in 
            ## scores dictionary
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
                        explored_stations.remove(i)
                        explored_stations.insert(self.search_list(explored_stations, val, scores), i)

                if i not in explored_stations:
                    explored_stations.insert(self.search_list(explored_stations, val, scores), i)
            
            start_point = explored_stations[0]  
            
            if start_point == end_id:
                end_detached = True
                shortest_path = scores[end_id]

        return prev_connection, previous, shortest_path

    def get_shortest_path(self, start_station_name, end_station_name):
        ''' get_shortest_path is the main function which is called in order to 
            return a sequence of stations along the shortest path

            Args:
                start_station_name : start station name,
                end_station_name : end station name,

            Returns:
                stations : List of sequence of stations in all the connections
        '''
        ## if the name of stations are incorrect
        if start_station_name not in self.name_map.keys() or end_station_name not in self.name_map.keys():
            return None

        start_id = self.name_map[start_station_name]
        end_id = self.name_map[end_station_name]

        ## if start id is same as the end id
        if start_id == end_id:
            return [self.tubemap.stations[start_id]]

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
