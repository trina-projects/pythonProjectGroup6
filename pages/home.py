# ====================================
# HOME PAGE
# displays park information, opening hours, park map
# and a filterable preview of rides and shows
# ====================================

#######################################
########## IMPORT FUNCTIONS ###########
#######################################

import streamlit as st
import base64 #encode local image for use in HTML
from pathlib import Path #construct file paths
from database.attractions import attractions, shows
from src.init import show_footer, PARK_NAME, PARK_LOCATION, PARK_HOURS

BASE_DIR = Path(__file__).resolve().parent.parent #retrieves the absolute path of your project's root directory
# Path(__file__) navigates the directory of file 
# .resolve() converts the file into absolute, resolved file and not relative
# parent.parent moves 2 levels up the current directory

# =================================================
# OPENING HOURS MODAL
# =================================================
@st.dialog("WonderWorld Opening Hours")
def show_opening_hours():
    st.write("Plan your adventure with our weekly operating hours!")

    #retrieve day and operating hours from the dictionary
    for day, hours in PARK_HOURS.items():
        st.write(f"{day}: {hours}")

    st.caption("Last admissions are 1 hour before closing time.")

    if st.button("Close", key="close_hours"): #key = .. gives the button a unique ID so it doesnt clash with other "Close" btns
        st.rerun() #rerun the page to close the modal


# =================================================
# PARK MAP MODAL
# =================================================
@st.dialog("WonderWorld Park Map", width="large")
def show_park_map():
    st.write("Explore WonderWorld before your adventure!")

    st.image(
        str(BASE_DIR / "assets/main/parkMap.jpg"),
        use_container_width=True
    )

    if st.button("Close", key="close_map"):
        st.rerun() #rerun the page to close the modal

#################################################################
######################### HEADER DESIGN #########################
#################################################################

image_path = BASE_DIR / "assets/main/themeParkMain.webp"

#read image as bytes and convert to base64 text for CSS background
with open(image_path, "rb") as image:
    encoded_image = base64.b64encode(image.read()).decode()

st.html(f"""
    <style>
        .stApp {{
            background-color: #ffffff;
        }}

        .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
        }}

        /* remove the gap between Streamlit elements */
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {{
            gap: 0 !important;
        }}

        /* full-screen hero with dark overlay for text readability */
        .hero-section {{
            background-image:
                linear-gradient(
                    rgba(0, 0, 0, 0.2),
                    rgba(0, 0, 0, 0.4)
                ),
                url("data:image/webp;base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;

            height: 100vh;

            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            text-align: center;
        }}

        /* animated rainbow gradient applied to title text */
        .rainbow-title {{
            background: linear-gradient(
                90deg,
                #ff5e5e,
                #ffb347,
                #ffff66,
                #66ff99,
                #66eaff,
                #b388ff,
                #ff77ff,
                #ff5e5e
            );

            background-size: 200% auto;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            animation: rainbowFlow 5s linear infinite;

            font-size: 60px;
            font-weight: bold;
            margin-bottom: 10px;
            filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.4))
                    drop-shadow(0 4px 6px rgba(0, 0, 0, 0.6));
        }}

        /* move gradient across the title continuously */
        @keyframes rainbowFlow {{
            from {{
                background-position: 200% center;
            }}
            to {{
                background-position: 0% center;
            }}
        }}

        .hero-subtitle {{
            color: white;
            font-size: 24px;
            margin-top: 10px;
        }}

    </style>

    <div class="hero-section">
        <h1 class="rainbow-title">
            Welcome to WonderWorld!
        </h1>
        <p class="hero-subtitle">
            Your adventure starts here!
        </p>
    </div>
""")

#################################################################
############ GETTING AROUND HERE CONTAINER DESIGN ###############
#################################################################

st.html("""
    <style>
        .getting-around {
            max-width: 1200px;
            margin: 0 auto;
            padding: 75px 35px;
            color: #142B40;
        }

        .getting-title {
            font-size: 42px;
            font-weight: 500;
            margin-bottom: 12px;
            color: #8B3030;
        }

        .getting-subtitle {
            font-size: 18px;
            color: #666666;
            margin-bottom: 45px;
        }

        .getting-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
        }

        .getting-item {
            padding: 10px 0;
        }

        .getting-icon {
            font-size: 28px;
            margin-bottom: 15px;
        }

        .getting-item h3 {
            font-size: 21px;
            font-weight: 500;
            margin-bottom: 12px;
            color: #142B40;
        }

        .getting-item p {
            font-size: 16px;
            line-height: 1.8;
            color: #555555;
        }

        .getting-link {
            color: #a67c52;
            font-size: 15px;
            font-weight: 500;
            text-decoration: underline;
            text-underline-offset: 4px;
        }

        .getting-link:hover {
            color: #8b3030;
        }
        
        /* responsive layout for smaller screens */
        @media (max-width: 800px) {
            .getting-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 480px) {
            .getting-grid {
                grid-template-columns: 1fr;
            }
        }
        .getting-heading {
            max-width: 1200px;
            margin: 0 auto;
            padding: 65px 35px 35px;
        }

        .getting-heading h2 {
            color: #8B3030;
            font-size: 42px;
            margin-bottom: 12px;
        }

        .getting-heading p {
            color: #666666;
            font-size: 18px;
        }

        .st-key-getting_links {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 35px 65px;
        }

        /* modal buttons */
        .st-key-getting_links [data-testid="stButton"] button {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            min-height: 0 !important;

            color: #0066CC !important;
            font-size: 15px !important;
            font-weight: 400 !important;
            text-decoration: underline !important;
            text-underline-offset: 3px;
        }

        /* page navigation links */
        .st-key-getting_links [data-testid="stPageLink"] a {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            min-height: 0 !important;

            color: #0066CC !important;
            font-size: 15px !important;
            font-weight: 400 !important;
            text-decoration: underline !important;
            text-underline-offset: 3px;
        }

        /* ensure nested link text inherits the blue colour */
        .st-key-getting_links [data-testid="stPageLink"] a * {
            color: inherit !important;
        }

        /* hover effect */
        .st-key-getting_links [data-testid="stButton"] button:hover,
        .st-key-getting_links [data-testid="stPageLink"] a:hover {
            color: #004499 !important;
            background: transparent !important;
            border: none !important;
        }

        /* pointer cursor */
        .st-key-getting_links [data-testid="stButton"] button,
        .st-key-getting_links [data-testid="stPageLink"] a {
            cursor: pointer !important;
        }
    </style>

    <div class="getting-heading">
        <h2>Getting Around Here</h2>
        <p>Everything you need to know before your adventure begins.</p>
    </div>
""")

###################################################
# VIEW OPENING HOURS
# TICKETS & ADMISSIONS
# EXPLORE THE PARK
# PLAN MY VISIT 
# DISPLAY AND CONTROLS
###################################################

#container key allows CSS to target only these buttons and links
with st.container(key="getting_links"):

    col1, col2, col3, col4 = st.columns(4, gap="large") #4 information columns

    with col1:
        st.html("""
            <div class="getting-item">
                <div class="getting-icon">🕓</div>
                <h3>Opening Hours</h3>
                <p>
                    Plan ahead for your adventure.
                    Check our park's operating hours
                    before your visit.
                </p>
            </div>
        """)

        #open the operating hours modal when clicked
        if st.button("View Opening Hours", key="view_hours"):
            show_opening_hours()

    with col2:
        st.html("""
            <div class="getting-item">
                <div class="getting-icon">🎟️</div>
                <h3>Tickets & Admission</h3>
                <p>
                    Discover our ticket options
                    and get ready for an unforgettable
                    day at WonderWorld.
                </p>
            </div>
        """)

        st.page_link(
            "pages/3_Tickets.py",
            label="View Tickets & Admission"
        )

    with col3:
        st.html("""
            <div class="getting-item">
                <div class="getting-icon">🗺️</div>
                <h3>Explore the Park Map</h3>
                <p>
                    Chart your route to the thrills. 
                    Browse our interactive park map to plan your must-ride attractions.   
                </p>
            </div>
        """)

        #open the park map modal when clicked
        if st.button("View Park Map", key="view_map"):
            show_park_map()

    with col4:
        st.html("""
            <div class="getting-item">
                <div class="getting-icon">🗓️</div>
                <h3>Plan My Visit</h3>
                <p>
                    Create a personalised itinerary
                    based on your adventure vibe
                    and visiting preferences.
                </p>
            </div>
        """)

        st.page_link(
            "pages/2_Park_Planner.py",
            label="Start Planning"
        )
###########################################################
####### END OF 4 COL DISPLAY AND CONTROLS #################
###########################################################

#################################################################
##################### EXPLORE WONDERWORLD DESIGN ################
#################################################################
st.html("""
    <style>

        /* main attractions section */
        .st-key-home_attractions_grid {
            width: 100%;
            max-width: 1400px;
            margin-left: auto;
            margin-right: auto;
            padding: 60px 30px;
            box-sizing: border-box;
            background-color: #ffffff;
        }

        /* main section heading */
        .section-title {
            color: #142B40;
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        /* main section subtitle */
        .section-subtitle {
            color: #666666;
            text-align: center;
            font-size: 18px;
            margin-bottom: 40px;
        }

        /* attraction image container */
        .st-key-home_attractions_grid [data-testid="stImage"] {
            width: 100%;
        }

        /* attraction image */
        .st-key-home_attractions_grid [data-testid="stImage"] img {
            width: 100%;
            height: 280px; /* consistent attraction image height */
            object-fit: cover; /* crop image without stretching */
            border-radius: 8px;
        }

        /* category title */
        .category-title {
            color: #142B40;
            font-size: 26px;
            font-weight: 500;
            margin-top: 8px;
            margin-bottom: 8px;
        }

        /* category description */
        .category-description {
            color: #444444;
            font-size: 17px;
            line-height: 1.8;
            margin-bottom: 15px;
        }

        /* ride name tags */
        .ride-tag {
            display: inline-block;
            background-color: #f4f4f4;
            color: #333333;
            border: 1px solid #e5e5e5;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 13px;
            margin-right: 6px;
            margin-bottom: 8px;
        }

        /* space between rows */
        .grid-spacing {
            height: 40px;
        }

        /* page background */
        .stApp {
            background-color: #ffffff;
        }

        /* classification buttons */
        [data-testid="stSegmentedControl"] button {
            border-radius: 30px !important;
            padding: 10px 22px !important;
            font-size: 16px !important;
        }

    </style>
""")
#################################################################
######################## ATTRACTIONS GRID #######################
#################################################################

with st.container(key="home_attractions_grid"):

    #section heading
    st.html("""
        <h2 class="section-title">
            Explore WonderWorld
        </h2>

        <p class="section-subtitle">
            Discover thrilling rides, magical performances
            and unforgettable experiences at WonderWorld.
        </p>
    """)


#############################################################
# CLASSIFICATION BAR
#############################################################

    #main filter, only one option can be selected at a time
    classification = st.segmented_control( #creates horizontal bar of connected buttons
        "Attraction Classification",
        options=[ 
            "All",
            "Rides",
            "Shows & Entertainment"
        ],
        default="All",
        selection_mode="single",
        label_visibility="collapsed" #hides attraction classification label
    )

    selected_category = "All Rides"

    #secondary classification for rides
    if classification == "Rides":

        selected_category = st.segmented_control(
            "Ride Categories",
            options=["All Rides"] + list(attractions.keys()), #retrieve category names from database
            default="All Rides",
            selection_mode="single",
            label_visibility="collapsed"
        )

#############################################################
# FILTER ATTRACTIONS
#############################################################

    display_attractions = [] #store rides and shows matching the selected filters

    #retrieve rides
    if classification in ["All", "Rides"]:

        for category, rides in attractions.items(): #key = category, value = list of rides

            #include all rides or only rides from the selected category
            if (classification == "All" or selected_category == "All Rides" or selected_category == category):
                #store each ride using the same structure as the shows below
                for ride in rides:

                    display_attractions.append({
                        "category": category,
                        "type": "Ride",
                        "details": ride
                    })

    #retrieve shows
    if classification in ["All", "Shows & Entertainment"]:

        for category, performances in shows.items():

            for show in performances:

                display_attractions.append({
                    "category": category,
                    "type": "Show",
                    "details": show
                })

    print(display_attractions)

    print("\nTotal attractions:", len(display_attractions))

#############################################################
# DISPLAY FILTERED ATTRACTIONS
#############################################################

    #display 3 attractions per row
    for i in range(0, len(display_attractions), 3):

        columns = st.columns(3, gap="large")

        #zip() pairs each column with one attraction
        #display_attractions[i:i + 3] retrieves up to 3 items for the current row
        for col, item in zip(columns, display_attractions[i:i + 3]):
            with col:
                #retrieve individual attraction details
                attraction = item["details"]
                category = item["category"]
                attraction_type = item["type"]

                #display attraction image
                image_path = BASE_DIR / attraction["image"]

                if image_path.exists(): 

                    st.image(
                        str(image_path),
                        use_container_width=True
                    )

                #display attraction name
                st.html(f"""
                    <h3 class="category-title">
                        {attraction["name"]}
                    </h3>
                """)

                #retrieve attraction description, default = "No description available"
                description = attraction.get("description", "No description available")

                st.html(f"""
                    <p class="category-description">
                        {description}
                    </p>
                """)

                #display category and duration tags
                st.html(f"""
                    <span class="ride-tag">
                        {category}
                    </span>

                    <span class="ride-tag">
                        {attraction["duration"]} mins
                    </span>
                """)

                #display show times for entertainment
                if attraction_type == "Show":

                    #combine show times into a comma-separated string
                    show_times = ", ".join(
                        attraction["show_times"]
                    )

                    st.html(f"""
                        <p class="category-description">
                            <strong>Show times:</strong>
                            {show_times}
                        </p>
                    """)

        #add spacing between rows
        st.html('<div class="grid-spacing"></div>')

# ###############################################################
# ########################## FOOTER #############################
# ###############################################################

show_footer() #shared footer imported from src/init.py