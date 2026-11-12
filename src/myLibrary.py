def calculate_waiting_time(queue_length, ride_capacity, ride_duration):
    cycles = queue_length / ride_capacity
    return cycles * ride_duration