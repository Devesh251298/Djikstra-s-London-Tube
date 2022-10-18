import sys
sys.path.append("tube")
sys.path.append("network")
from network import *
from tube import *

def get_tubemap():

    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    return tubemap

def main():
    tubemap = get_tubemap()
    # print(tubemap.stations)
    path_finder = PathFinder(tubemap)
    # print(tubemap.stations.keys())

    for i in tubemap.stations.keys():
        for j in tubemap.stations.keys():
            print("From : ",tubemap.stations[i].name,", To : ", tubemap.stations[j].name)
            stations = path_finder.get_shortest_path(tubemap.stations[i].name, tubemap.stations[j].name)
            station_names = [station.name for station in stations]
            print(station_names)

    # stations = path_finder.get_shortest_path("South Kensington", "South Kensington")
    # station_names = [station.name for station in stations]
    # print(station_names)

if __name__ == '__main__':
    main()
