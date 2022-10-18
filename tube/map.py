import json
import sys
from components import Station, Line, Connection

class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap (list of Connections)
    """
    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances

    def import_from_json(self, filepath):
        with open(filepath) as jsonfile:
            data = json.load(jsonfile)
        
        ## LINES
        for i in range(len(data["lines"])):
            id = data["lines"][i]['line']
            name = data["lines"][i]['name']
            self.lines[id] = Line(id = id, name = name)
        
        ## STATIONS
        for i in range(len(data["stations"])):
            id = data["stations"][i]['id']
            name = data["stations"][i]['name']
            zone = data["stations"][i]['zone']
            if zone[-2:] == ".5":
                zones = []
                val = int(float(zone))
                zone = {val,val+1}
            else:
                zone = {int(zone)}
            if id not in self.stations.keys():
                self.stations[id] = Station(id = id, name = name, zones = zone)
            else : 
                self.stations.zones.add(zone)


        
        ## CONNECTIONS
        for i in range(len(data["connections"])):
            station_1 = data["connections"][i]['station1']
            station_2 = data["connections"][i]['station2']
            time = data["connections"][i]['time']
            line = data["connections"][i]['line']
            self.connections.append(Connection(stations = {self.stations[station_1], self.stations[station_2]},
                                               line = self.lines[line], time = int(time)))
        return 


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])


if __name__ == "__main__":
    test_import()
