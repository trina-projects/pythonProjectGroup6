# ====================================
# BACKEND FUNCTIONS
# This file contains all backend logic for the website

# Responsibilities:
# 1. Calculate ticket prices.
# 2. Generate and send itinerary emails.
# 3. Generate and send ticket booking receipts.
# 4. Determine peak and non-peak admission prices.
# 5. Validate user inputs and ticket bookings.
# 6. Generate random attraction recommendations.

# =====================================


#######################################
########## IMPORT FUNCTIONS ###########
#######################################
import math
from email.message import EmailMessage
import ssl #encrypted connections for sending email
import smtplib #connect to email server
import streamlit as st
import re #regular expressions to check email format
from datetime import date
import random
from database.attractions import attractions, shows, ticket_prices as TICKET_PRICES
from src.init import (
    PARK_NAME,
    PARK_LOCATION,
    PARK_HOURS
)

#create a secure SSL context for encrypted email connections.
context = ssl.create_default_context()

# =================================================
# SEND ITINERARY EMAIL USED IN 2_Park_Planner.py
# ================================================
def send_itinerary_email(recipient, itinerary):
    #retrieve from secrets.toml
    sender = st.secrets["EMAIL_ADDRESS"].strip() 
    password = st.secrets["EMAIL_APP_PASSWORD"].replace(" ", "").strip() #remove any spaces
    
    #create new email message object
    message = EmailMessage()

    #email configuration
    message["Subject"] = f"Your {PARK_NAME} Adventure Itinerary"
    message["From"] = sender
    message["To"] = recipient

    #email body
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
    index = 1
    for ride in itinerary: #loop through each selected attraction
        lines.append(f"{index}. {ride['name']}") #add the attraction number and name
        lines.append(f"   Ride: {ride['ride_duration']} min") #add the ride duration
        lines.append("")  #add a blank line for spacing
        index += 1  #increase attraction number by 1

    #add email footer
    lines.append(f"Total attractions: {len(itinerary)}")
    lines.append("")
    lines.append("Have a wonderful adventure!")
    lines.append(f"The {PARK_NAME} Team")

    message.set_content("\n".join(lines)) #combine every line into one complete email message

    #connect to gmail and send to email
    # SMTP stands for Simple Mail Transfer Protocol.
    # It allows the application to send emails through an external email provider.
    #
    # smtp.gmail.com is Gmail's SMTP server.
    # Port 587 supports email submission using STARTTLS.
    # timeout=30 prevents the connection from waiting indefinitely if the server cannot be reached.
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
        smtp.ehlo() #start connection with echo location
        smtp.starttls(context=context) #upgrade to encrypted connection
        smtp.ehlo() #start again after introducing encrypted connection 

        smtp.login(sender, password) #login through your provided email

        print("Gmail authentication successful!") 

        smtp.send_message(message) #finally send message

        print("Email accepted by Gmail!")
# =================================================
# END OF SEND ITINERARY EMAIL 
# ================================================


# =================================================
# SEND TICKET BOOKING RECEIPT USED IN 3_Tickets.py
# ================================================

#generates and emails a ticket booking receipt.
#Parameters:
#  recipient (str): Visitor's email address.
#  visit_date (date): Selected date of visit.
#  adults (int): Number of individual adult tickets.
#  children (int): Number of individual child tickets.
#  families (int): Number of family bundles.
#  booking (dict): Calculated booking information.

def send_ticket_receipt(recipient, visit_date, adults, children, families, booking):

    #retrieve credentials
    sender = st.secrets["EMAIL_ADDRESS"].strip() 

    password = (
        st.secrets["EMAIL_APP_PASSWORD"]
        .replace(" ", "")
        .strip()
    )

    prices = booking["prices"]

    #create new email object
    message = EmailMessage()

    #construct email
    message["Subject"] = f"{PARK_NAME} - Booking Receipt"
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
        Opening Hours: {PARK_HOURS[visit_date.strftime("%A")]}

        We look forward to welcoming you
        to a magical day at {PARK_NAME}!

        """

    #assign completed receipt as the email content
    message.set_content(receipt)

    #connect and send to email
    context = ssl.create_default_context() #create a secure SSL context for email encryption

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()

        smtp.login(sender, password)
        smtp.send_message(message)

# ===============================================================
# TICKET PRICING CONFIGURATION
# ===============================================================

#determine whether the selected date is a peak day or not
def get_day_type(visit_date):

    if visit_date.weekday() >= 5: #python's weekday function, index 0 = Monday, 6 = Sunday
        return "Peak"

    return "Non-Peak"


#retrieve ticket prices based on visit date
def get_ticket_prices(visit_date):

    day_type = get_day_type(visit_date)

    return TICKET_PRICES[day_type]


#calc ticket prices and booking summary
def calculate_booking(adults, children, families, visit_date):

    prices = get_ticket_prices(visit_date)

    #multiply tix quantity by their respective prices
    adult_total = adults * prices["adult"]
    child_total = children * prices["child"]
    family_total = families * prices["family"]

    #sum total
    total = adult_total + child_total + family_total

    #calc total no. of visitors
    total_adults = adults + (families * 2)
    total_children = children + (families * 2)

    #calculate how much two adult tickets and two child tickets would cost if purchased alone
    #subtract the family bundle price to determine the savings per bundle.
    #multiply by the number of family bundles purchased.
    family_savings = ( (prices["adult"] * 2) + (prices["child"] * 2) - prices["family"]) * families

    #return complete booking information so that tix booking page 
    # and email receipt function can access it without having to recalculate
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
# ===============================================================
# END OF TICKET PRICING CONFIGURATION
# ===============================================================


# ===============================================================
# VALIDATE EMAIL ADDRESS
# ===============================================================
# re.fullmatch() checks whether the entire email address
# matches the specified regular expression pattern.
#
# [^@\s]+ represents one or more characters that
# are not an @ symbol or whitespace.
#
# @ represents the required email separator.
#
# \. represents a literal full stop.
#
# Example of an accepted format:
# visitor@gmail.com
#
# strip() removes unnecessary surrounding whitespace.
#
# bool() converts the matching result into True or False.
def validate_email(email):

    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email.strip()
        )
    )


# ===============================================================
# VALIDATE TICKET BOOKING IN 3_Park_Planner.py
# ===============================================================
def validate_booking(adults,children,families,visit_date,email):

    if visit_date < date.today():
        return False, "Please select a valid visit date."

    if not (0 <= adults <= 20 and 0 <= children <= 20 and 0 <= families <= 10):
        return False, "Invalid ticket quantity."
    # note:
    # if the maximum ticket quantities are changed here,
    # the input limits in 3_Tickets.py should also be updated.

    if adults + children + families == 0:
        return False, "Please select at least one ticket."

    #include visitors from both individual tix and family bundles
    total_adults = adults + (families * 2)
    total_children = children + (families * 2)

    #reject bookings if only children and no adult
    if total_children > 0 and total_adults == 0:
        return False, (
            "Children must be accompanied "
            "by at least one adult."
        )

    if not validate_email(email):
        return False, "Please enter a valid email address."

    return True, "Booking is valid."


# ===============================================================
# RECOMMENDATION CAROUSEL MODAL USED IN 1_Attractions.py
# ===============================================================

#generates up to 5 random attraction recommendation
def get_recommendations(current_name, limit=5):

    #store the 5 random items in this list
    all_items = []

    #retrieve all rides
    for category, rides in attractions.items(): #.item() is python function, returns dictionary key-value pair

        for ride in rides:

            all_items.append({
                "category": category,
                "classification": "Rides",
                "details": ride
            })

    #retrieve all show
    for category, show_list in shows.items():

        for show in show_list:

            all_items.append({
                "category": category,
                "classification": "Shows",
                "details": show
            })

    #empty list to store filted attrations
    available_items = []

    #loop through all rides and shows
    for item in all_items:
        attraction_name = item["details"]["name"]
        if attraction_name != current_name: #check if attraction is different from current attraction
            available_items.append(item) #add to list

    #randomly select up to 5 items
    return random.sample(available_items, min(limit, len(available_items)))
