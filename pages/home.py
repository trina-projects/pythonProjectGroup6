import streamlit as st
import base64
from pathlib import Path
from database.attractions import attractions, category_descriptions, shows

BASE_DIR = Path(__file__).resolve().parent.parent


#################################################################
######################## HEADER DESIGN ##########################
#################################################################

BASE_DIR = Path(__file__).resolve().parent.parent

image_path = BASE_DIR / "assets/main/themeParkMain.webp"

with open(image_path, "rb") as image:
    encoded_image = base64.b64encode(image.read()).decode()

st.html(f"""
<style>

    .stApp {{
        background-color: #ffffff;
    }}

    .block-container {{
        padding-top: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100%;
    }}

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
##################### ATTRACTIONS DESIGN ########################
#################################################################

st.html("""
<style>

    /* Main attractions section */
    .st-key-attractions_grid {
        max-width: 1000px;
        margin: 0 auto;
        padding: 60px 30px;
        background-color: #ffffff;
    }

    /* Main section heading */
    .section-title {
        color: #142B40;
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Main section subtitle */
    .section-subtitle {
        color: #666666;
        text-align: center;
        font-size: 18px;
        margin-bottom: 40px;
    }

    /* Attraction images */
    .st-key-attractions_grid
    [data-testid="stImage"] img {
        width: 100%;
        aspect-ratio: 4 / 3;
        height: auto;
        object-fit: cover;
        border-radius: 3px;
    }

    /* Category title */
    .category-title {
        color: #142B40;
        font-size: 26px;
        font-weight: 500;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    /* Category description */
    .category-description {
        color: #444444;
        font-size: 17px;
        line-height: 1.8;
        margin-bottom: 15px;
    }

    /* Ride name tags */
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

    /* Space between rows */
    .grid-spacing {
        height: 40px;
    }

    /* Page background */
    .stApp {
        background-color: #ffffff;
    }

    /* Classification buttons */
    [data-testid="stSegmentedControl"] button {
        border-radius: 30px !important;
        padding: 10px 22px !important;
        font-size: 16px !important;
    }

    /* Attraction images */
    [data-testid="stImage"] img {
        width: 80%;
        aspect-ratio: 4 / 3;
        object-fit: cover;
        border-radius: 4px;
    }


</style>
""")
#################################################################
######################## ATTRACTIONS GRID #######################
#################################################################

with st.container(key="attractions_grid"):

    # Section heading
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

    classification = st.segmented_control(
        "Attraction Classification",
        options=[
            "All",
            "Rides",
            "Shows & Entertainment"
        ],
        default="All",
        selection_mode="single",
        label_visibility="collapsed"
    )

    selected_category = "All Rides"

    # Secondary classification for rides
    if classification == "Rides":

        selected_category = st.segmented_control(
            "Ride Categories",
            options=["All Rides"] + list(attractions.keys()),
            default="All Rides",
            selection_mode="single",
            label_visibility="collapsed"
        )

    #############################################################
    # FILTER ATTRACTIONS
    #############################################################

    display_attractions = []

    # Retrieve rides
    if classification in ["All", "Rides"]:

        for category, rides in attractions.items():

            if (
                classification == "All"
                or selected_category == "All Rides"
                or selected_category == category
            ):

                for ride in rides:

                    display_attractions.append({
                        "category": category,
                        "type": "Ride",
                        "details": ride
                    })

    # Retrieve shows
    if classification in ["All", "Shows & Entertainment"]:

        for category, performances in shows.items():

            for show in performances:

                display_attractions.append({
                    "category": category,
                    "type": "Show",
                    "details": show
                })

    #############################################################
    # DISPLAY FILTERED ATTRACTIONS
    #############################################################

    for i in range(0, len(display_attractions), 2):

        columns = st.columns(2, gap="large")

        for col, item in zip(
            columns,
            display_attractions[i:i + 2]
        ):

            with col:

                # Retrieve individual attraction details
                attraction = item["details"]
                category = item["category"]
                attraction_type = item["type"]

                # Display attraction image
                image_path = BASE_DIR / attraction["image"]

                if image_path.exists():

                    st.image(
                        str(image_path),
                        use_container_width=True
                    )

                # Display attraction name
                st.html(f"""
                    <h3 class="category-title">
                        {attraction["name"]}
                    </h3>
                """)

                # Display description
                description = attraction.get(
                    "description",
                    category_descriptions.get(category, "")
                )

                st.html(f"""
                    <p class="category-description">
                        {description}
                    </p>
                """)

                # Display category and duration tags
                st.html(f"""
                    <span class="ride-tag">
                        {category}
                    </span>

                    <span class="ride-tag">
                        {attraction["duration"]} mins
                    </span>
                """)

                # Display show times for entertainment
                if attraction_type == "Show":

                    show_times = ", ".join(
                        attraction["show_times"]
                    )

                    st.html(f"""
                        <p class="category-description">
                            <strong>Show times:</strong>
                            {show_times}
                        </p>
                    """)

        # Add spacing between rows
        st.html('<div class="grid-spacing"></div>')