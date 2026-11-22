import math

####################################
########## ITINERARY ###############
###################################

def estimate_waiting_time(ride):
    capacity = ride["capacity"]
    duration = ride["duration"]
    queue_length = ride["queue_length"]

    if capacity <= 0:
        return 0

    batches = math.ceil(queue_length / capacity)

    return batches * duration


def generate_itinerary(attractions, vibe_categories, selected_vibe):

    # Find the categories associated with the selected vibe
    preferred_categories = vibe_categories.get(selected_vibe, [])

    itinerary = []

    # Loop through every attraction category
    for category, rides in attractions.items():

        if category in preferred_categories:

            for ride in rides:

                waiting_time = estimate_waiting_time(ride)

                itinerary.append({
                    "name": ride["name"],
                    "category": category,
                    "duration": ride["duration"],
                    "waiting_time": waiting_time,
                    "total_time": ride["duration"] + waiting_time,
                    "image": ride.get("image")
                })

    # Recommend attractions with shorter estimated waits first
    itinerary.sort(key=lambda ride: ride["waiting_time"])

    return itinerary