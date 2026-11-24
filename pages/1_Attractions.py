import streamlit as st
from pathlib import Path
import base64
import html
from database.attractions import attractions, shows
from src.init import show_footer
from src.validation import get_recommendations
from html import escape

BASE_DIR = Path(__file__).resolve().parent.parent

st.html("""
<style>
    .st-key-attractions_grid .attraction-card-image {
        width: 100%;
        height: 280px;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        border-radius: 10px;
    }
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

    /* Standardise image dimensions */
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

    /* Left and right carousel arrows */
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

    /* Pagination dots */
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

# Store which attraction is currently selected
if "selected_attraction" not in st.session_state:
    st.session_state.selected_attraction = None

# Convert ride names into filenames:
# "Mega Coaster" -> "megaCoaster.mp4"
def get_video_path(name):
    filename = name
    return BASE_DIR / "assets" / "videos" / (filename + ".mp4")


# Combine rides and shows into one list
def get_all_attractions():
    items = []

    for category, rides in attractions.items():
        for ride in rides:
            items.append({
                "category": category,
                "classification": "Rides",
                "details": ride
            })

    for category, performances in shows.items():
        for show in performances:
            items.append({
                "category": category,
                "classification": "Shows & Entertainment",
                "details": show
            })

    return items

def explore_attraction(item):

    st.session_state.selected_attraction = item

    # Reset the recommendation carousel
    st.session_state.recommendation_source = None
    st.session_state.recommendation_index = 0

def show_recommendations(current_name):

    st.divider()

    st.html("""
        <h2 class="recommendation-heading">
            Discover More Adventures
        </h2>

        <p class="recommendation-subtitle">
            There's always more magic waiting
            for you at WonderWorld.
        </p>
    """)

    # ###########################################################
    # GENERATE RANDOM RECOMMENDATIONS
    # ###########################################################

    if (
        "recommendation_source" not in st.session_state
        or st.session_state.recommendation_source != current_name
    ):

        st.session_state.recommended_items = (
            get_recommendations(current_name, limit=5)
        )

        st.session_state.recommendation_source = current_name
        st.session_state.recommendation_index = 0

    recommendations = st.session_state.recommended_items

    total_items = len(recommendations)

    if total_items == 0:
        st.info("No other attractions available.")
        return

    visible_count = min(4, total_items)

    start = st.session_state.recommendation_index


    # ###########################################################
    # CAROUSEL NAVIGATION FUNCTIONS
    # ###########################################################

    def move_carousel(direction):

        st.session_state.recommendation_index = (
            st.session_state.recommendation_index + direction
        ) % total_items


    def jump_to_slide(index):

        st.session_state.recommendation_index = index


    # ###########################################################
    # INFINITE LOOP LOGIC
    # ###########################################################

    visible_items = [
        recommendations[(start + i) % total_items]
        for i in range(visible_count)
    ]


    # ###########################################################
    # CAROUSEL LAYOUT
    # ###########################################################

    previous_col, cards_col, next_col = st.columns(
        [0.5, 12, 0.5],
        vertical_alignment="center",
        gap="small"
    )


    # LEFT ARROW
    with previous_col:

        st.button(
            "❮",
            key="carousel_previous",
            on_click=move_carousel,
            args=(-1,),
            disabled=total_items <= 1
        )


    # RECOMMENDATION CARDS
    with cards_col:

        with st.container(key="recommendation_cards"):

            columns = st.columns(visible_count)

            for index, item in enumerate(visible_items):

                details = item["details"]
                name = details["name"]
                category = item["category"]

                with columns[index]:

                    with st.container(border=True):

                        st.image(
                            str(BASE_DIR / details["image"]),
                            use_container_width=True
                        )

                        st.html(f"""
                            <div class="recommendation-name">
                                {escape(name)}
                            </div>

                            <div class="recommendation-category">
                                {escape(category)}
                            </div>
                        """)

                        st.button(
                            "Explore →",
                            key=f"recommendation_{name}",
                            use_container_width=True,
                            on_click=explore_attraction,
                            args=(item,)
                        )

    # RIGHT ARROW
    with next_col:

        st.button(
            "❯",
            key="carousel_next",
            on_click=move_carousel,
            args=(1,),
            disabled=total_items <= 1
        )


    # ###########################################################
    # PAGINATION DOTS
    # ###########################################################

    with st.container(key="carousel_dots"):

        left_space, dots_col, right_space = st.columns(
            [4, 1.5, 4]
        )

        with dots_col:

            dot_columns = st.columns(
                total_items,
                gap="small"
            )

            for index in range(total_items):

                with dot_columns[index]:

                    is_active = (
                        index ==
                        st.session_state.recommendation_index
                    )

                    st.button(
                        "●" if is_active else "○",
                        key=f"carousel_dot_{index}",
                        type="primary" if is_active else "secondary",
                        on_click=jump_to_slide,
                        args=(index,),
                        help=f"Go to position {index + 1}"
                    )

def show_attraction_banner(item):
    details = item["details"]

    image_path = BASE_DIR / details["image"]

    if not image_path.is_file():
        return

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    image_format = image_path.suffix.lower().replace(".", "")

    if image_format == "jpg":
        image_format = "jpeg"

    title = html.escape(details["name"])
    description = html.escape(details.get("description", ""))

    st.html(f"""
        <style>
            .attraction-hero {{
                width: 100vw;
                height: 65vh;

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

# Display one attraction's details
def show_attraction_details(item):
    details = item["details"]

    # Full-width attraction banner
    show_attraction_banner(item)

    if st.button("← Back to Attractions"):
        st.session_state.selected_attraction = None
        st.rerun()

    left, right = st.columns([2, 1], gap="large")

    with left:
        st.subheader("Attraction Information")

        st.write("**Category:**", item["category"])

        if item["classification"] == "Rides":
            st.write(
                "**Attraction Type:**",
                details.get("type", item["category"])
            )

            st.write(
                "**Ride Duration:**",
                str(details["duration"]) + " minutes"
            )

            st.write(
                "**Ride Capacity:**",
                str(details["capacity"]) + " guests"
            )

            if "height_restriction" in details:
                st.write(
                    "**Height Restrictions:**",
                    details["height_restriction"]
                )

        else:
            st.write("**Classification:** Shows & Entertainment")

            if "duration" in details:
                st.write(
                    "**Show Duration:**",
                    str(details["duration"]) + " minutes"
                )

        with st.expander("Advisory: Before Visiting"):
            st.write(details.get(
                "advisory",
                "Please follow all attraction safety instructions."
            ))

    with right:
        st.subheader("Experience Preview")

        video_path = get_video_path(details["name"])

        if video_path.is_file():
            st.video(str(video_path))
        else:
            st.info("Preview video coming soon!")

    st.divider()


# Display the attractions directory
def show_attractions_grid():
    st.title("Our Attractions")

    st.write(
        "Explore exciting rides, spectacular shows "
        "and unforgettable experiences at WonderWorld."
    )

    classification = st.segmented_control(
        "Attraction Classification",
        options=["All", "Rides", "Shows & Entertainment"],
        default="All",
        key="attraction_filter"
    )

    items = get_all_attractions()

    # Filter by classification
    if classification != "All":
        items = [
            item for item in items
            if item["classification"] == classification
        ]

    # Optional ride category filter
    if classification == "Rides":
        category = st.selectbox(
            "Ride Category",
            options=["All Rides"] + list(attractions.keys())
        )

        if category != "All Rides":
            items = [
                item for item in items
                if item["category"] == category
            ]

    st.divider()
    with st.container(key="attractions_grid"):
        # Three columns per row
        for i in range(0, len(items), 3):
            columns = st.columns(3, gap="large")

            for col, item in zip(columns, items[i:i + 3]):
                with col:
                    details = item["details"]

                    image_path = BASE_DIR / details["image"]

                    if image_path.is_file():
                        with open(image_path, "rb") as image_file:
                            encoded_image = base64.b64encode(
                                image_file.read()
                            ).decode("utf-8")

                        image_format = image_path.suffix.lower().replace(".", "")

                        if image_format == "jpg":
                            image_format = "jpeg"

                        st.html(f"""
                            <div class="attraction-card-image"
                                style="
                                    background-image: url('data:image/{image_format};base64,{encoded_image}');
                                ">
                            </div>
                        """)

                    st.subheader(details["name"])

                    st.caption(item["category"])

                    st.write(details.get(
                        "description",
                        "Discover this attraction at WonderWorld!"
                    ))

                    if st.button(
                        "View Details",
                        key="view_" + item["classification"] + "_" + details["name"]
                    ):
                        st.session_state.selected_attraction = item
                        st.rerun()


# Main page controller
if st.session_state.selected_attraction is None:
    show_attractions_grid()
else:
    show_attraction_details(
        st.session_state.selected_attraction
    )
if st.session_state.get("selected_attraction"):
    show_recommendations(
        st.session_state.selected_attraction["details"]["name"]
    )

# ###############################################################
# ########################## FOOTER #############################
# ###############################################################

show_footer()