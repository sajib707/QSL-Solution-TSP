import math
# Define the coordinates and names of the City Bank branches
locations = [
    {"id": 1, "name": "Uttara Branch", "lat": 23.8728568, "lon": 90.3984184},
    {"id": 2, "name": "City Bank Airport", "lat": 23.8513998, "lon": 90.3944536},
    {"id": 3, "name": "City Bank Nikunja", "lat": 23.8330429, "lon": 90.4092871},
    {"id": 4, "name": "City Bank Beside Uttara Diagnostic", "lat": 23.8679743, "lon": 90.3840879},
    {"id": 5, "name": "City Bank Mirpur 12", "lat": 23.8248293, "lon": 90.3551134},
    {"id": 6, "name": "City Bank Le Meridien", "lat": 23.827149, "lon": 90.4106238},
    {"id": 7, "name": "City Bank Shaheed Sarani", "lat": 23.8629078, "lon": 90.3816318},
    {"id": 8, "name": "City Bank Narayanganj", "lat": 23.8673789, "lon": 90.429412},
    {"id": 9, "name": "City Bank Pallabi", "lat": 23.8248938, "lon": 90.3549467},
    {"id": 10, "name": "City Bank JFP", "lat": 23.813316, "lon": 90.4147498}
]

# Define the starting location (Uttara Branch)
start_location = {"id": 1, "name": "Uttara Branch", "lat": 23.8728568, "lon": 90.3984184}

# Function to calculate the distance between two points using the Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers

    # Convert latitude and longitude to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate the differences between latitudes and longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply the Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance * 1000  # Convert distance to meters

# Create a list of distances between each pair of locations
distances = [[calculate_distance(loc1["lat"], loc1["lon"], loc2["lat"], loc2["lon"])
              for loc2 in locations]
             for loc1 in locations]

# Create a list of location IDs
location_ids = [loc["id"] for loc in locations]

# Function to find the next unvisited location with the minimum distance
def get_next_location(current_location, unvisited_locations):
    min_distance = float("inf")
    next_location = None
    for location in unvisited_locations:
        distance = distances[current_location - 1][location - 1]  # Adjust indexing here
        if distance < min_distance:
            min_distance = distance
            next_location = location
    return next_location

# Perform the TSP using the nearest neighbor algorithm
unvisited_locations = location_ids.copy()
unvisited_locations.remove(start_location["id"])

current_location = start_location["id"]
optimal_route = [start_location]

while unvisited_locations:
    next_location = get_next_location(current_location, unvisited_locations)
    optimal_route.append(locations[next_location - 1])
    unvisited_locations.remove(next_location)
    current_location = next_location

# Print the optimal route
total_distance = 0

for i in range(len(optimal_route) - 1):
    loc1 = optimal_route[i]
    loc2 = optimal_route[i+1]
    distance = distances[loc1["id"] - 1][loc2["id"] - 1]
    total_distance += distance
    print(f"{loc1['name']} (ID: {loc1['id']}) -> {loc2['name']} (ID: {loc2['id']}): {distance} meters")

# Print the total distance of the optimal route
print(f"Total Distance: {total_distance} meters")
