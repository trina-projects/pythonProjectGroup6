
import streamlit as st
from pathlib import Path
from database.attractions import attractions, shows

BASE_DIR = Path(__file__).resolve().parent.parent

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


# Display one attraction's details
def show_attraction_details(item):
    details = item["details"]

    if st.button("← Back to Attractions"):
        st.session_state.selected_attraction = None
        st.rerun()

    st.title(details["name"])

    st.write(details.get(
        "description",
        "Discover an unforgettable experience at WonderWorld!"
    ))

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

    # Three columns per row
    for i in range(0, len(items), 3):
        columns = st.columns(3, gap="large")

        for col, item in zip(columns, items[i:i + 3]):
            with col:
                details = item["details"]

                image_path = BASE_DIR / details["image"]

                if image_path.is_file():
                    st.image(
                        str(image_path),
                        use_container_width=True
                    )

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
