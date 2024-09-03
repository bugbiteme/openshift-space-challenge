# python code doing an api query to find a lisf of planets with coordonates

import requests
import json

my_coordinates = (15.23, 95.3)

def find_closest():
    url = "https://emergency-player1.apps.cluster-mj8xc.mj8xc.sandbox1025.opentlc.com/planets"
    response = requests.get(url)
    data = response.json()

    number_of_planets = 0
    # print all planet_name
    for planet in data:
        number_of_planets += 1

    print(f"number of planets: {number_of_planets}")
    

    # find closest planet to my_coordinates
    closest = None
    closest_distance = None
    for planet in data:
        planet_coordinates = (planet["galactic_latitude"], planet["galactic_longitude"])
        distance = abs(planet_coordinates[0] - my_coordinates[0]) + abs(planet_coordinates[1] - my_coordinates[1])
        if closest is None or distance < closest_distance:
            closest = planet
            closest_distance = distance

    return closest, closest_distance

if __name__ == "__main__":
    print(f"closest planet is: {find_closest()}")

