import sys
sys.path.append("tube")
sys.path.append("network")
from network import *
from tube import *

def get_tubemap():
    """ Return an initialised TubeMap object

    Returns:
        tube.map.TubeMap: Initialised TubeMap object
    """
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    return tubemap

def main():
    tubemap = get_tubemap()
    
    path_finder = PathFinder(tubemap)

    # Examples usage of path_finder
    stations = path_finder.get_shortest_path('Stockwell', 'Ealing Broadway')
    station_names = [station.name for station in stations]
    print(station_names)

if __name__ == '__main__':
    main()

