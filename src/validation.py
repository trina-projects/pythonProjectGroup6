import math
from email.message import EmailMessage
import ssl
import smtplib
import streamlit as st
import re
from datetime import date
import random
from database.attractions import attractions, shows
from src.init import (
    PARK_NAME,
    PARK_LOCATION,
    PARK_HOURS
)

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


####################################
########## CALCULATE TOTAL PRICE ###############
###################################
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
##########################
###### EMAIL ############
############################
def send_itinerary_email(recipient, itinerary):
    sender = st.secrets["EMAIL_ADDRESS"].strip()
    password = st.secrets["EMAIL_APP_PASSWORD"].replace(" ", "").strip()
    message = EmailMessage()

    message["Subject"] = f"Your {PARK_NAME} Adventure Itinerary"
    message["From"] = sender
    message["To"] = recipient

    lines = [
        f"Welcome to {PARK_NAME}!",
        "",
        "YOUR ADVENTURE ITINERARY",
        "",
        f"Location: {PARK_LOCATION}",
        "",
        "Opening Hours:",
        "\n".join(
            f"{day}: {hours}"
            for day, hours in PARK_HOURS.items()
        ),
        "",
        "Your Selected Attractions:",
    ""
]

    for index, ride in enumerate(itinerary, start=1):
        lines.extend([
            f"{index}. {ride['name']}",
            f"   Ride: {ride['ride_duration']} min",
            ""
        ])

    lines.extend([
        f"Total attractions: {len(itinerary)}",
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


########## EMAIL RECEIPT ################

def send_ticket_receipt(
    recipient,
    visit_date,
    adults,
    children,
    families,
    booking
):

    sender = st.secrets["EMAIL_ADDRESS"].strip()

    password = (
        st.secrets["EMAIL_APP_PASSWORD"]
        .replace(" ", "")
        .strip()
    )

    prices = booking["prices"]

    message = EmailMessage()

    message["Subject"] = "WonderWorld - Booking Receipt"
    message["From"] = sender
    message["To"] = recipient

    receipt = f"""
        WONDERWORLD
        Ticket Booking Receipt
        ========================================

        Thank you for choosing WonderWorld!

        BOOKING INFORMATION

        Visit Date: {visit_date.strftime("%d %B %Y")}
        Admission Type: {booking['day_type']}

        ----------------------------------------
        TICKET DETAILS
        ----------------------------------------

        Adult Tickets:
        {adults} x S${prices['adult']:.2f}
        Subtotal: S${booking['adult_total']:.2f}

        Child Tickets:
        {children} x S${prices['child']:.2f}
        Subtotal: S${booking['child_total']:.2f}

        Family Bundles:
        {families} x S${prices['family']:.2f}
        Subtotal: S${booking['family_total']:.2f}

        ----------------------------------------

        Total Adults: {booking['total_adults']}
        Total Children: {booking['total_children']}
        Total Ticketed Visitors: {booking['total_visitors']}

        Family Bundle Savings: S${booking['family_savings']:.2f}

        TOTAL AMOUNT: S${booking['total']:.2f}

        ========================================

        PARK INFORMATION

        Location: {PARK_LOCATION}
        Opening Hours: {PARK_HOURS}

        We look forward to welcoming you
        to a magical day at {PARK_NAME}!

        """

    message.set_content(receipt)

    context = ssl.create_default_context()

    with smtplib.SMTP(
        "smtp.gmail.com",
        587,
        timeout=30
    ) as smtp:

        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()

        smtp.login(sender, password)
        smtp.send_message(message)

# ###############################################################
# ###################### TICKET PRICING #########################
# ###############################################################

TICKET_PRICES = {
    "Non-Peak": {
        "adult": 60,
        "child": 40,
        "family": 170
    },
    "Peak": {
        "adult": 75,
        "child": 50,
        "family": 210
    }
}


# Determine whether the selected date is a peak day
def get_day_type(visit_date):

    if visit_date.weekday() >= 5:
        return "Peak"

    return "Non-Peak"


# Retrieve ticket prices based on visit date
def get_ticket_prices(visit_date):

    day_type = get_day_type(visit_date)

    return TICKET_PRICES[day_type]


# Calculate ticket prices and booking summary
def calculate_booking(adults, children, families, visit_date):

    prices = get_ticket_prices(visit_date)

    adult_total = adults * prices["adult"]
    child_total = children * prices["child"]
    family_total = families * prices["family"]

    total = adult_total + child_total + family_total

    total_adults = adults + (families * 2)
    total_children = children + (families * 2)

    family_savings = (
        (prices["adult"] * 2)
        + (prices["child"] * 2)
        - prices["family"]
    ) * families

    return {
        "day_type": get_day_type(visit_date),
        "prices": prices,
        "adult_total": adult_total,
        "child_total": child_total,
        "family_total": family_total,
        "total_adults": total_adults,
        "total_children": total_children,
        "total_visitors": total_adults + total_children,
        "family_savings": family_savings,
        "total": total
    }


# Validate email address
def validate_email(email):

    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email.strip()
        )
    )


# Validate ticket booking
def validate_booking(
    adults,
    children,
    families,
    visit_date,
    email
):

    if visit_date < date.today():
        return False, "Please select a valid visit date."

    if not (0 <= adults <= 20
            and 0 <= children <= 20
            and 0 <= families <= 10):
        return False, "Invalid ticket quantity."

    if adults + children + families == 0:
        return False, "Please select at least one ticket."

    total_adults = adults + (families * 2)
    total_children = children + (families * 2)

    if total_children > 0 and total_adults == 0:
        return False, (
            "Children must be accompanied "
            "by at least one adult."
        )

    if not validate_email(email):
        return False, "Please enter a valid email address."

    return True, "Booking is valid."


################# RECOMMENDATION ###################

def get_recommendations(current_name, limit=5):

    all_items = []

    # Retrieve all rides
    for category, rides in attractions.items():

        for ride in rides:

            all_items.append({
                "category": category,
                "classification": "Rides",
                "details": ride
            })

    # Retrieve all shows
    for category, show_list in shows.items():

        for show in show_list:

            all_items.append({
                "category": category,
                "classification": "Shows",
                "details": show
            })

    # Exclude the currently viewed attraction
    available_items = [
        item for item in all_items
        if item["details"]["name"] != current_name
    ]

    # Randomly select up to 5 items
    return random.sample(
        available_items,
        min(limit, len(available_items))
    )
