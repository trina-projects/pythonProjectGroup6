import streamlit as st
from pathlib import Path
import base64
import html
from database.attractions import attractions, shows
from src.init import show_footer

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


# ###############################################################
# ########################## FOOTER #############################
# ###############################################################

show_footer()