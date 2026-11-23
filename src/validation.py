import math
from email.message import EmailMessage
import ssl
import smtplib
import streamlit as st

context = ssl.create_default_context()

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


def calculate_total(adults, children):

    ticket_prices = {
        "Adult": 60,
        "Child": 40
    }

    total = (
        adults * ticket_prices["Adult"]
        + children * ticket_prices["Child"]
    )

    # Apply 10% family discount
    if adults >= 2 and children >= 2:
        total *= 0.9

    return total

def calculate_ride_time(ride):
    capacity = ride["capacity"]
    duration = ride["duration"]
    queue_length = ride["queue_length"]

    # Estimate the number of ride cycles needed
    if capacity <= 0:
        return None

    cycles = (queue_length + capacity - 1) // capacity

    waiting_time = cycles * duration
    total_time = waiting_time + duration

    return {
        "waiting_time": waiting_time,
        "ride_duration": duration,
        "total_time": total_time
    }


##########################
###### EMAIL ############
############################
def send_itinerary_email(
    recipient,
    itinerary,
    total_duration,
    park_name,
    park_location,
    park_hours
):
    sender = st.secrets["EMAIL_ADDRESS"].strip()
    password = st.secrets["EMAIL_APP_PASSWORD"].replace(" ", "").strip()
    message = EmailMessage()

    message["Subject"] = f"Your {park_name} Adventure Itinerary"
    message["From"] = sender
    message["To"] = recipient

    lines = [
        f"Welcome to {park_name}!",
        "",
        "YOUR ADVENTURE ITINERARY",
        "",
        f"Location: {park_location}",
        f"Opening Hours: {park_hours}",
        "",
        "Your Selected Attractions:",
        ""
    ]

    for index, ride in enumerate(itinerary, start=1):
        lines.extend([
            f"{index}. {ride['name']}",
            f"   Ride: {ride['ride_duration']} min",
            f"   Estimated wait: {ride['waiting_time']} min",
            f"   Total: {ride['total_time']} min",
            ""
        ])

    lines.extend([
        f"Total Estimated Duration: {total_duration} minutes",
        "",
        "Waiting times are illustrative estimates.",
        "Walking, breaks and loading times are excluded.",
        "",
        "Have a wonderful adventure!",
        "The WonderWorld Team"
    ])

    message.set_content("\n".join(lines))

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()

        smtp.login(sender, password)

        print("Gmail authentication successful!")

        smtp.send_message(message)

        print("Email accepted by Gmail!")