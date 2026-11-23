import streamlit as st
from pathlib import Path
from database.attractions import attractions
from src.validation import calculate_ride_time
from src.init import show_footer
import html
import re
from src.validation import send_itinerary_email

BASE_DIR = Path(__file__).resolve().parent.parent

st.html("""
<style>
    /* Only target the Park Planner's attraction cards */
    .st-key-planner_cards [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        overflow: hidden;
    }

    /* Equal-sized images */
    .st-key-planner_cards [data-testid="stImage"] {
        width: 100% !important;
    }

    .st-key-planner_cards [data-testid="stImage"] img {
        width: 100% !important;
        height: 220px !important;
        object-fit: cover !important;
        object-position: center !important;
        border-radius: 10px !important;
    }

    /* Consistent description height */
    .st-key-planner_cards .planner-description {
        height: 72px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        line-height: 24px;
        color: #64748B;
        font-size: 15px;
    }
</style>
""")
# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "planner_selected" not in st.session_state:
    st.session_state.planner_selected = []

if "planner_generated" not in st.session_state:
    st.session_state.planner_generated = False


def move_attraction(index, direction):
    selected = st.session_state.planner_selected

    new_index = index + direction

    # Prevent moving beyond the list boundaries
    if 0 <= new_index < len(selected):

        selected[index], selected[new_index] = (
            selected[new_index],
            selected[index]
        )

        # Regenerate itinerary after reordering
        st.session_state.planner_generated = False

# -------------------------------------------------
# PAGE HEADING
# -------------------------------------------------

st.html("""
<style>
    .planner-heading {
        text-align: center;
        padding: 25px 15px 40px;
    }

    .planner-heading h1 {
        color: #142B40;
        font-size: clamp(36px, 4vw, 56px);
        font-weight: 750;
        margin-bottom: 15px;
    }

    .planner-heading p {
        color: #64748B;
        font-size: 18px;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }
</style>

<div class="planner-heading">
    <h1>Plan Your Perfect Adventure 🎡</h1>
    <p>
        Explore attractions, choose your favourites,
        and create your very own WonderWorld itinerary.
    </p>
</div>
""")


# -------------------------------------------------
# ATTRACTION DATA
# -------------------------------------------------

def get_all_rides():
    items = []

    for category, rides in attractions.items():
        for ride in rides:
            items.append({
                "category": category,
                "details": ride
            })

    return items


all_rides = get_all_rides()


# -------------------------------------------------
# FILTERS
# -------------------------------------------------

st.subheader("Explore Attractions")

st.write(
    "Select the rides you'd like to experience "
    "during your visit."
)

category_filter = st.selectbox(
    "Filter by category",
    ["All Attractions"] + list(attractions.keys())
)

if category_filter == "All Attractions":
    filtered_rides = all_rides
else:
    filtered_rides = [
        item for item in all_rides
        if item["category"] == category_filter
    ]

# -------------------------------------------------
# ATTRACTION CARDS
# -------------------------------------------------
with st.container(key="planner_cards"):

    for i in range(0, len(filtered_rides), 3):

        columns = st.columns(3, gap="large")

        for col, item in zip(columns, filtered_rides[i:i + 3]):

            with col:
                ride = item["details"]
                name = ride["name"]

                with st.container(border=True):

                    image_path = BASE_DIR / ride["image"]

                    if image_path.is_file():
                        st.image(
                            str(image_path),
                            use_container_width=True
                        )

                    st.markdown(f"### {name}")

                    st.caption(item["category"])

                    # Fixed-height description
                    description = ride.get(
                        "description",
                        "Discover an unforgettable adventure!"
                    )

                    st.html(f"""
                        <div class="planner-description">
                            {html.escape(description)}
                        </div>
                    """)

                    st.write(
                        f"🎢 Ride duration: {ride['duration']} min"
                    )

                    selected = (
                        name in st.session_state.planner_selected
                    )

                    if selected:
                        if st.button(
                            "✓ Remove from Plan",
                            key=f"remove_{name}",
                            use_container_width=True
                        ):
                            st.session_state.planner_selected.remove(name)
                            st.session_state.planner_generated = False
                            st.rerun()

                    else:
                        if st.button(
                            "＋ Add to Plan",
                            key=f"add_{name}",
                            use_container_width=True,
                            type="primary"
                        ):
                            st.session_state.planner_selected.append(name)
                            st.session_state.planner_generated = False
                            st.rerun()
# -------------------------------------------------
# ITINERARY SUMMARY
# -------------------------------------------------
st.divider()

st.subheader("Your Adventure Plan")

selected_names = st.session_state.planner_selected

st.write(f"**{len(selected_names)} attractions selected**")

if not selected_names:
    st.info(
        "Your adventure starts here! "
        "Select some attractions to begin planning."
    )

else:
    st.caption(
        "Use the arrows to rearrange the order "
        "of your attractions."
    )

    for index, name in enumerate(selected_names):

        with st.container(border=True):

            name_col, up_col, down_col = st.columns(
                [6, 1, 1],
                vertical_alignment="center"
            )

            with name_col:
                st.write(f"**{index + 1}. {name}**")

            with up_col:
                if st.button(
                    "↑",
                    key=f"up_{name}",
                    disabled=(index == 0)
                ):
                    move_attraction(index, -1)
                    st.rerun()

            with down_col:
                if st.button(
                    "↓",
                    key=f"down_{name}",
                    disabled=(index == len(selected_names) - 1)
                ):
                    move_attraction(index, 1)
                    st.rerun()

    if st.button(
        "Generate My Itinerary",
        type="primary",
        use_container_width=True
    ):
        st.session_state.planner_generated = True

    if st.button("Clear Selection"):
        st.session_state.planner_selected = []
        st.session_state.planner_generated = False
        st.rerun()

# -------------------------------------------------
# GENERATED ITINERARY
# -------------------------------------------------

PARK_NAME = "WonderWorld"
PARK_LOCATION = "Sentosa Island, Singapore (fictional park)"
PARK_HOURS = "10:00 AM - 8:00 PM"

if st.session_state.planner_generated and selected_names:

    st.divider()

    # Restrict the width of the itinerary card
    left_space, card_col, right_space = st.columns([1, 2, 1])

    with card_col:

        with st.container(border=True):

            st.html("""
                <div style="
                    background: #DCEFED;
                    padding: 24px 12px;
                    border-radius: 12px;
                    text-align: center;
                    margin-bottom: 18px;
                ">
                    <div style="
                        font-size: 13px;
                        letter-spacing: 2px;
                        color: #426E70;
                    ">WONDERWORLD</div>

                    <h2 style="
                        color: #17384A;
                        margin: 10px 0;
                    ">Your Adventure Itinerary 🎡</h2>

                    <p style="color: #426E70; margin: 0;">
                        Your day, your way.
                    </p>
                </div>
            """)

            st.write(f"📍 **Location:** {PARK_LOCATION}")
            st.write(f"🕙 **Opening Hours:** {PARK_HOURS}")

            st.divider()

            total_duration = 0
            itinerary_details = []

            for index, name in enumerate(selected_names, start=1):

                ride = None

                for item in all_rides:
                    if item["details"]["name"] == name:
                        ride = item["details"]
                        break

                if ride is None:
                    continue

                timing = calculate_ride_time(ride)

                if timing is None:
                    st.warning(f"Cannot estimate time for {name}.")
                    continue

                total_duration += timing["total_time"]

                itinerary_details.append({
                    "name": name,
                    "ride_duration": timing["ride_duration"],
                    "waiting_time": timing["waiting_time"],
                    "total_time": timing["total_time"]
                })

                st.markdown(f"#### {index:02d}. {name}")

                st.caption(
                    f"🎢 Ride: {timing['ride_duration']} min  |  "
                    f"⏳ Wait: {timing['waiting_time']} min"
                )

                st.write(
                    f"**Estimated stop: {timing['total_time']} min**"
                )

                if index < len(selected_names):
                    st.divider()

            st.divider()

            st.metric(
                "Total Estimated Duration",
                f"{total_duration} minutes"
            )

            st.caption(
                "Waiting times are estimates based on sample "
                "queue data. Walking, breaks and loading times "
                "are not included."
            )

            st.divider()

            st.markdown("#### 📧 Email Your Itinerary")

            st.write(
                "Want to keep a copy of your adventure plan? "
                "Enter your email address below."
            )

            email_address = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="planner_email"
            )

            if st.button(
                "Send My Itinerary",
                type="primary",
                use_container_width=True
            ):

                if not re.fullmatch(
                    r"[^@\s]+@[^@\s]+\.[^@\s]+",
                    email_address.strip()
                ):
                    st.warning("Please enter a valid email address.")

                else:
                    try:
                        with st.spinner("Sending your itinerary..."):

                            send_itinerary_email(
                                recipient=email_address.strip(),
                                itinerary=itinerary_details,
                                total_duration=total_duration,
                                park_name=PARK_NAME,
                                park_location=PARK_LOCATION,
                                park_hours=PARK_HOURS
                            )

                        st.success("Your itinerary has been emailed!")

                    except Exception as e:
                        st.error(f"Failed to send email: {type(e).__name__}")
                        st.write(str(e))

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

show_footer()
