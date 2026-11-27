# =================================================
# ATTRACTIONS PAGE
# displays the attractions directory, individual details and recommendations
# =================================================
import streamlit as st
from pathlib import Path
import base64
import html
from database.attractions import attractions, shows
from src.init import show_footer
from src.validation import get_recommendations
from html import escape

#retrieve the absolute path of the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# =================================================
# ATTRACTIONS AND CAROUSEL DESIGN
# =================================================
st.html("""
<style>
    /* directory card image dimensions */
    .st-key-attractions_grid .attraction-card-image {
        width: 100%;
        height: 280px;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        border-radius: 10px;
    }
    /* recommendation heading and subtitle */
    .recommendation-heading {
        text-align: center;
        color: #142B40;
        font-size: 32px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 5px;
    }

    .recommendation-subtitle {
        text-align: center;
        color: #777777;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* standardise image dimensions */
    .st-key-recommendation_cards [data-testid="stImage"],
    .st-key-recommendation_cards [data-testid="stImage"] > div {
        width: 100% !important;
    }

    .st-key-recommendation_cards [data-testid="stImage"] img {
        width: 100% !important;
        height: 190px !important;
        object-fit: cover !important;
        object-position: center !important;
        border-radius: 10px !important;
    }

    /* consistent title height keeps cards aligned */
    .recommendation-name {
        color: #142B40;
        font-size: 19px;
        font-weight: 700;
        min-height: 48px;
        margin-top: 8px;
    }

    .recommendation-category {
        color: #777777;
        font-size: 14px;
        min-height: 25px;
    }

    /* left and right carousel arrows */
    .st-key-carousel_previous button,
    .st-key-carousel_next button {
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        min-height: 44px !important;
        padding: 0 !important;
        font-size: 22px !important;
        background-color: white !important;
        color: #142B40 !important;
        border: 1px solid #D0D5DA !important;
    }

    .st-key-carousel_previous button:hover,
    .st-key-carousel_next button:hover {
        background-color: #91C3C2 !important;
        border-color: #91C3C2 !important;
    }

    /* pagination dots */
    .st-key-carousel_dots button {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
        min-height: 28px !important;
        color: #B8C4C8 !important;
        font-size: 18px !important;
    }

    .st-key-carousel_dots button:hover {
        color: #91C3C2 !important;
    }

    .st-key-carousel_dots button[kind="primary"] {
        color: #142B40 !important;
        background: transparent !important;
    }
</style>
""")

# =================================================
# SESSION STATE
# =================================================
#st.session_state: store and remember variables even when the Python script reruns
#initialise only once
if "selected_attraction" not in st.session_state:
    st.session_state.selected_attraction = None

# =================================================
# VIDEO FILE PATH
# =================================================
def get_video_path(name):
    #use the attraction name as the video filename
    filename = name
    return BASE_DIR / "assets" / "videos" / (filename + ".mp4")


# =================================================
# GET ALL RIDES AND SHOWS
# =================================================
def get_all_attractions():
    items = []

    #key = category, value = list of rides
    for category, rides in attractions.items():
        for ride in rides:
            items.append({
                "category": category,
                "classification": "Rides",
                "details": ride
            })

    #retrieve shows using the same structure as rides
    for category, performances in shows.items():
        for show in performances:
            items.append({
                "category": category,
                "classification": "Shows & Entertainment",
                "details": show
            })

    return items

# =================================================
# SELECT ATTRACTION
# =================================================
def explore_attraction(item):

    #store the entire selected item, including its details
    st.session_state.selected_attraction = item

    #reset the recommendation carousel when opening another attraction
    st.session_state.recommendation_source = None
    st.session_state.recommendation_index = 0

# =================================================
# RECOMMENDATION CAROUSEL
# =================================================
def show_recommendations(current_name):

    st.divider() #horizontal line

    st.html("""
        <h2 class="recommendation-heading">
            Discover More Adventures
        </h2>

        <p class="recommendation-subtitle">
            There's always more magic waiting
            for you at WonderWorld.
        </p>
    """)

    #generate new recommendations only when the selected attraction changes
    if ("recommendation_source" not in st.session_state or st.session_state.recommendation_source != current_name):

        #retrieve up to 5 random attractions excluding the current one
        st.session_state.recommended_items = (
            get_recommendations(current_name, limit=5)
        )

        st.session_state.recommendation_source = current_name
        st.session_state.recommendation_index = 0

    #reuse saved recommendations when the page reruns
    recommendations = st.session_state.recommended_items

    total_items = len(recommendations)

    #stop if there are no recommendations
    # if total_items == 0:
    #     st.info("No other attractions available.")
    #     return

    #display up to 4 cards at a time
    visible_count = min(4, total_items)

    #index of the first visible card
    start = st.session_state.recommendation_index

    # ###########################################################
    # CAROUSEL NAVIGATION FUNCTIONS
    # ###########################################################

    #############################################################
    # CAROUSEL NAVIGATION FUNCTIONS
    #############################################################

    def move_carousel(direction):
        index = st.session_state.recommendation_index
        index = index + direction #move left (-1) or right (+1)

        if index >= total_items: #return to first attraction if past the last attraction
            index = 0
        elif index < 0: #return to last attraction if before the first attraction
            index = total_items - 1

        st.session_state.recommendation_index = index #save the updated index

    def jump_to_slide(index):

        #jump directly to the selected pagination dot
        st.session_state.recommendation_index = index


    #############################################################
    # INFINITE LOOP LOGIC
    #############################################################

    visible_items = []

    index = start

    for i in range(visible_count):
        #return to first attraction if past the last attraction
        if index >= total_items:
            index = 0

        visible_items.append(recommendations[index]) #add attraction to the visible list
        index += 1 #move to the next attraction

    # ###########################################################
    # CAROUSEL LAYOUT
    # ###########################################################

    #0.5/13 size width for arrow columns on either side of the wider card area
    previous_col, cards_col, next_col = st.columns(
        [0.5, 12, 0.5],
        vertical_alignment="center",
        gap="small"
    )

    # LEFT ARROW
    with previous_col:

        #on click calls the function with -1 to move backwards
        st.button(
            "◀",
            key="carousel_previous",
            on_click=move_carousel,
            args=(-1,),
            disabled=total_items <= 1 #backup incase there's nth to scroll through
        )


    # RECOMMENDATION CARDS
    with cards_col:
        with st.container(key="recommendation_cards"):
            columns = st.columns(visible_count)
            index = 0 #start from the first column

            for item in visible_items:
                details = item["details"]
                name = details["name"]
                category = item["category"]

                #display attraction in its corresponding column
                with columns[index]:
                    with st.container(border=True):
                        st.image(
                            str(BASE_DIR / details["image"]),
                            use_container_width=True
                        )

                        #escape() prevents special characters from being interpreted as HTML
                        st.html(f"""
                            <div class="recommendation-name">
                                {escape(name)}
                            </div>

                            <div class="recommendation-category">
                                {escape(category)}
                            </div>
                        """)

                        #pass selected attraction to the callback function
                        st.button(
                            "Explore →",
                            key=f"recommendation_{name}",
                            use_container_width=True,
                            on_click=explore_attraction,
                            args=(item,)
                        )

                index += 1 #move to the next column

                
        # RIGHT ARROW
        with next_col:
            #pass 1 to move forwards
            st.button(
                "▶",
                key="carousel_next",
                on_click=move_carousel,
                args=(1,),
                disabled=total_items <= 1
            )

        # ###########################################################
        # PAGINATION DOTS
        # ###########################################################

        with st.container(key="carousel_dots"):
            left_space, dots_col, right_space = st.columns([4, 2, 4])

            with dots_col:
                dot_columns = st.columns(total_items, gap="small")

                #create one dot for each possible starting position
                for index in range(total_items):
                    with dot_columns[index]:
                        #check whether this dot matches the current carousel index
                        is_active = (index == st.session_state.recommendation_index)

                        #use a filled dot and primary style for the active position
                        st.button(
                            "•" if is_active else "⚬",
                            key=f"carousel_dot_{index}",
                            type="primary" if is_active else "secondary",
                            on_click=jump_to_slide,
                            args=(index,),
                            help=f"Go to position {index + 1}"
                        )
# =================================================
# END OF RECOMMENDATION CAROUSEL
# =================================================


# =================================================
# ATTRACTION BANNER PICTURE
# =================================================
def show_attraction_banner(item):
    #retrieve the original attraction dictionary
    details = item["details"]

    image_path = BASE_DIR / details["image"]

    #skip the banner if the image file is missing
    if not image_path.is_file():
        return

    #read image bytes and encode as base64 text for CSS
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    #retrieve the file extension without the dot
    image_format = image_path.suffix.lower().replace(".", "")

    if image_format == "jpg":
        image_format = "jpeg"

    #escape text before inserting it into HTML
    title = html.escape(details["name"])
    description = html.escape(details.get("description", ""))

    st.html(f"""
        <style>
            /* full-width banner with dark overlay for text readability */
            .attraction-hero {{
                width: 100vw;
                height: 65vh;

                /* centre banner across the full viewport */
                position: relative;
                left: 50%;
                transform: translateX(-50%);

                background-image:
                    linear-gradient(
                        rgba(0, 0, 0, 0.25),
                        rgba(0, 0, 0, 0.50)
                    ),
                    url("data:image/{image_format};base64,{encoded_image}");

                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;

                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;

                text-align: center;
                padding: 30px;
                box-sizing: border-box;
            }}

            .attraction-hero-title {{
                font-size: clamp(40px, 5vw, 72px);
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 15px;
                line-height: 1.2;
            }}

            .attraction-hero-description {{
                font-size: clamp(16px, 2vw, 24px);
                color: #ffffff;
                max-width: 900px;
                line-height: 1.6;
                margin: 0;
            }}
        </style>

        <section class="attraction-hero">
            <h1 class="attraction-hero-title">
                {title}
            </h1>

            <p class="attraction-hero-description">
                {description}
            </p>
        </section>
    """)
# =================================================
# END OF ATTRACTION BANNER PICTURE
# =================================================

# =================================================
# ATTRACTION DETAILS
# =================================================
def show_attraction_details(item):
    details = item["details"]

    # Full-width attraction banner
    show_attraction_banner(item)

    #clear selection and rerun to return to the directory
    if st.button("← Back to Attractions"):
        st.session_state.selected_attraction = None
        st.rerun()

    #left column is twice as wide as the right column
    left, right = st.columns([2, 1], gap="large")

    with left:
        st.subheader("Attraction Information")

        st.write("**Category:**", item["category"])
        #display ride-specific information
        if item["classification"] == "Rides":
            #use the category as a fallback if the type key is missing
            st.write("**Attraction Type:**", details.get("type", item["category"]))
            st.write("**Ride Duration:**", str(details["duration"]) + " minutes")
            st.write("**Ride Capacity:**", str(details["capacity"]) + " guests")
            st.write("**Show Times:**")

            if "height_restriction" in details:
                st.write("**Height Restrictions:**",details["height_restriction"])

        #display show-specific information
        else:
            st.write("**Classification:** Shows & Entertainment")

            if "duration" in details:
                st.write("**Show Duration:**", str(details["duration"]) + " minutes")
            for time in details.get("show_times", []):
                st.write(f"- {time}")

        #use a default safety message if advisory is missing
        with st.expander("Advisory: Before Visiting"):
            st.write(details.get("advisory","Please follow all attraction safety instructions."))

    with right:
        st.subheader("Experience Preview")
        video_path = get_video_path(details["name"])

        #display the preview only if the video file exists
        if video_path.is_file():
            st.video(str(video_path))
        else:
            st.info("Preview video coming soon!")

    st.divider()
# =================================================
# END OF ATTRACTION DETAILS
# =================================================


# =================================================
# ATTRACTIONS DIRECTORY
# =================================================
def show_attractions_grid():

    st.title("Our Attractions")
    st.write("Explore exciting rides, spectacular shows and unforgettable experiences at WonderWorld.")

    classification = st.segmented_control(
        "Attraction Classification",
        options=["All", "Rides", "Shows & Entertainment"],
        default="All",
        key="attraction_filter",
        label_visibility="collapsed"
    )

    #retrieve all attractions before filtering
    items = get_all_attractions()

    # filter by classification
    if classification != "All":
        filtered_items = []
        for item in items:
            if item["classification"] == classification:
                filtered_items.append(item)
        items = filtered_items

    # filter by ride cat.
    if classification == "Rides":
        category = st.selectbox("Ride Category", options=["All Rides"] + list(attractions.keys()))

        if category != "All Rides":
            filtered_items = []
            for item in items:
                if item["category"] == category:
                    filtered_items.append(item)
            items = filtered_items

    st.divider()

    ###########################################################
    # DISPLAY ATTRACTIONS GRID
    ###########################################################
    with st.container(key="attractions_grid"):
        index = 0
        for item in items:
            #create a new row of 3 columns
            if index == 0:
                columns = st.columns(3, gap="large")

            with columns[index]:
                details = item["details"]
                image_path = BASE_DIR / details["image"]
                
                if image_path.is_file(): #validate image existence
                    with open(image_path, "rb") as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
                    
                    #retrieve image format
                    image_format = image_path.suffix.lower().replace(".", "")

                    if image_format == "jpg":
                        image_format = "jpeg"

                    #display image as a CSS background
                    st.html(f"""
                        <div class="attraction-card-image"
                            style="
                                background-image: url('data:image/{image_format};base64,{encoded_image}');
                            ">
                        </div>
                    """)

                st.subheader(details["name"])
                st.caption(item["category"])

                #default description if key is missing
                st.write(details.get("description", "Discover this attraction at WonderWorld!"))

                #unique button key for each attraction e.g. view_Rides_Rocket Hydro
                if st.button("View Details", key="view_" + item["classification"] + "_" + details["name"]):
                    #save selected attraction and rerun page
                    st.session_state.selected_attraction = item
                    st.rerun()

            index += 1 #move to the next column
            if index == 3: #reset index after filling all 3 columns
                index = 0
                
# =================================================
# END OF ATTRACTIONS DIRECTORY
# =================================================

# =================================================
# MAIN PAGE CONTROLLER
# =================================================
#show directory when no attraction is selected
if st.session_state.selected_attraction is None:
    show_attractions_grid()
else:
    show_attraction_details(
        st.session_state.selected_attraction
    )
#show recommendations only on the attraction details page
if st.session_state.get("selected_attraction"):
    show_recommendations(
        st.session_state.selected_attraction["details"]["name"]
    )

# ###############################################################
# ########################## FOOTER #############################
# ###############################################################

#shared footer imported from src/init.py
show_footer()