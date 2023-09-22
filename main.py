import json
from colorama import Fore, Style
# Lade die Daten aus der JSON-Datei
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

stations = data["stations"]
lines = data["lines"]

# Funktion zur Berechnung der kürzesten Route
def dijkstra(start, end):
    # Initialisierung der Entfernungen
    distances = {station["name"]: float("inf") for station in stations}
    distances[start] = 0

    # Vorgänger-Stationen für die Rückverfolgung der Route
    predecessors = {}

    # Set der unbesuchten Bahnhöfe
    unvisited = {station["name"] for station in stations}

    while unvisited:
        # Wählen Sie den Bahnhof mit der kürzesten Entfernung aus
        current_station = min(unvisited, key=lambda station: distances[station])

        # Überprüfen Sie alle benachbarten Bahnhöfe
        for connection in [c for s in stations if s["name"] == current_station for c in s["connections"]]:
            station_name = connection["stationName"]
            travel_time = connection["travelTime"]
            alt_distance = distances[current_station] + travel_time

            # Wenn eine kürzere Route gefunden wurde, aktualisieren Sie die Entfernung und Vorgänger
            if alt_distance < distances[station_name]:
                distances[station_name] = alt_distance
                predecessors[station_name] = current_station

        # Markieren Sie den aktuellen Bahnhof als besucht
        unvisited.remove(current_station)

        # Wenn der Zielbahnhof erreicht wurde, beenden Sie die Schleife
        if current_station == end:
            break

    # Rückverfolgung der Route
    if end not in predecessors:
        return None, None

    path = [end]
    while path[-1] != start:
        path.append(predecessors[path[-1]])

    # Umkehren des Pfads, um die Reihenfolge von Start zu Ziel zu erhalten
    path.reverse()

    # Bestimmen der verwendeten Linien
    used_lines = []
    for i in range(len(path) - 1):
        for station in stations:
            if station["name"] == path[i]:
                for connection in station["connections"]:
                    if connection["stationName"] == path[i + 1]:
                        used_lines.append(connection["line"])

    return path, used_lines

# Nutzereingabe für Start- und Endstation
start_station = input("Geben Sie den Startbahnhof ein: ")
end_station = input("Geben Sie den Zielbahnhof ein: ")

def display_route(start_station, end_station, stations, lines):
    shortest_route, used_lines = dijkstra(start_station, end_station)

    if not shortest_route or not used_lines:
        print("Es wurde keine Route gefunden.")
        return

    print("Kürzeste Route von {} nach {}: ".format(start_station, end_station))
    for i, station in enumerate(shortest_route):
        print("{}. Station: {}".format(i + 1, station))
        if i < len(shortest_route) - 1:
            print("  Linie: {}".format(used_lines[i]))

# Nutzereingabe für Start- und Endstation

# Anzeige der Route
display_route(start_station, end_station, stations, lines)


