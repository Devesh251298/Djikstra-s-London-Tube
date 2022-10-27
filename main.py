from tube.map import TubeMap
from network.path import PathFinder

def get_tubemap():

    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    return tubemap

def main():
    tubemap = get_tubemap()
    # print(tubemap.stations)
    path_finder = PathFinder(tubemap)
    # print(tubemap.stations.keys())
    count = 0
    # for i in tubemap.stations.keys():
    #     for j in tubemap.stations.keys():
    #         count+=1
    #         print("From : ",tubemap.stations[i].name,", To : ", tubemap.stations[j].name)
    #         stations = path_finder.get_shortest_path(tubemap.stations[i].name, tubemap.stations[j].name)
    #         station_names = [station.name for station in stations]
    #         print(station_names)
    # print(count)

    stations = path_finder.get_shortest_path("Stockwell", "Stockwell")
    station_names = [station.name for station in stations]
    print(station_names)

if __name__ == '__main__':
    main()
