import json
from tube.components import Station, Line, Connection

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
        try :
            with open(filepath) as jsonfile:
                data = json.load(jsonfile)
        except:
            return None

        ## LINES
        for i in range(len(data["lines"])):
            try : 
                id = str(data["lines"][i]['line'])
            except : 
                raise TypeError("Line Id must be a String!")
            
            try : 
                name = str(data["lines"][i]['name'])
            except : 
                raise TypeError("Line name must be a String!")

            self.lines[id] = Line(id = id, name = name)
        
        ## STATIONS
        for i in range(len(data["stations"])):
            try :
                id = str(data["stations"][i]['id'])
            except:
                raise TypeError("StationId must be a String!")

            try : 
                name = str(data["stations"][i]['name'])
            except:
                raise TypeError("Station name must be a String!")

            try :   
                zone = str(data["stations"][i]['zone'])
            except:
                raise TypeError("Zone must be a String!")

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
            try :
                station_1 = data["connections"][i]['station1']
            except:
                raise TypeError("StationId must be a String!")

            try :
                station_2 = data["connections"][i]['station2']
            except:
                raise TypeError("StationId must be a String!")
            
            try: 
                time = int(data["connections"][i]['time'])
            except :
                raise TypeError("Time must be an Integer!")

            try : 
                line = str(data["connections"][i]['line'])
            except :
                raise TypeError("Line must be a String!")

            self.connections.append(Connection(stations = {self.stations[station_1], self.stations[station_2]},
                                               line = self.lines[line], time = time))
        return 


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("../data/london.json")
    
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
