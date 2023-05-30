import requests
import tsp_solver.greedy

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

# Calculate the distances using the Google Maps Distance Matrix API
def calculate_distances(origins, destinations):
    # Google Maps API key here
    api_key = "YtPyDlF8RS8g0S6wRVkQuqcCNW2xK1"
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    # Extract the distances from the API response
    distances = []
    for row in data["rows"]:
        row_distances = []
        for element in row["elements"]:
            if element["status"] == "OK":
                row_distances.append(element["distance"]["value"])
            else:
                row_distances.append(float("inf"))  # Set unreachable distances to infinity
        distances.append(row_distances)

    return distances

# Create a list of locations' coordinates
locations_coords = [(loc["lat"], loc["lon"]) for loc in locations]

# Create a list of distances between each pair of locations
distances = calculate_distances(
    f"{start_location['lat']},{start_location['lon']}",
    "|".join([f"{loc['lat']},{loc['lon']}" for loc in locations if loc != start_location])
)

# Solve the TSP using the distances
tsp_solution = tsp_solver.greedy.solve_tsp(distances)

# Reconstruct the optimal route
optimal_route = [start_location] + [locations[idx] for idx in tsp_solution]

# Print the optimal route
for loc in optimal_route:
    print(f"{loc['name']} (ID: {loc['id']})")

# Print the total distance of the optimal route
total_distance = sum(distances[i][j] for i, j in zip(tsp_solution, tsp_solution[1:]))
print(f"Total Distance: {total_distance} meters")
