import streamlit as st
from pathlib import Path
from database.attractions import attractions
from src.init import (
    show_footer,
    PARK_NAME,
    PARK_LOCATION,
    PARK_HOURS,
    PARK_TAGLINE
)

import html
from src.validation import send_itinerary_email, validate_email
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
        st.session_state.itinerary_index = 0

    if st.button("Clear Selection"):
        st.session_state.planner_selected = []
        st.session_state.planner_generated = False
        st.rerun()

# -------------------------------------------------
# GENERATED ITINERARY
# -------------------------------------------------


@st.dialog("Your Adventure Itinerary", width="large")
def show_itinerary(itinerary):
    count = len(itinerary)
    index = st.session_state.get("itinerary_index", 0) % count
    ride = itinerary[index]

    st.html("""
        <div style="background:#DCEFED; padding:20px;
                    border-radius:12px; text-align:center; color:#142B40;">
            <small>W O N D E R W O R L D</small>
            <h2>Your Adventure Itinerary 🎡</h2>
            <p>Your day, your way.</p>
        </div>
        <style>
            .st-key-itinerary_card [data-testid="stImage"] img {
                width: 100% !important;
                height: 260px !important;
                object-fit: cover !important;
                border-radius: 10px !important;
            }
        </style>
    """)
    st.write(f"📍 **Location:** {PARK_LOCATION}")
    st.write("🕙 **Opening Hours:**")

    for day, hours in PARK_HOURS.items():
        st.write(f"{day}: {hours}")
    st.caption(f"Attraction {index + 1} of {count}")

    def navigate(new_index):
        st.session_state.itinerary_index = new_index % count

    previous, center, following = st.columns(
        [1, 8, 1], vertical_alignment="center"
    )
    with previous:
        st.button("◀", key="itinerary_prev", disabled=count == 1,
                    on_click=navigate, args=(index - 1,))

    with center:
        with st.container(key="itinerary_card", border=True):
            image_path = BASE_DIR / ride["image"]
            if image_path.is_file():
                st.image(str(image_path), use_container_width=True)
            else:
                st.caption("Attraction image unavailable")

            st.markdown(f"### {index + 1:02d}. {ride['name']}")
            st.caption(ride["category"])
            st.write(f"🎢 Ride duration: {ride['ride_duration']} min")

    with following:
        st.button("▶︎", key="itinerary_next", disabled=count == 1,
                    on_click=navigate, args=(index + 1,))

    # Clickable pagination dots
    with st.container(key="itinerary_dots"):
        st.html("""
            <style>
                .st-key-itinerary_dots button {
                    border: none !important;
                    background: transparent !important;
                    padding: 0 !important;
                    min-height: 30px !important;
                    color: #426E70 !important;
                }
            </style>
        """)
        dots = st.columns([2] + [1] * count + [2])
        for i in range(count):
            with dots[i + 1]:
                st.button("●" if i == index else "○",
                            key=f"itinerary_dot_{i}",
                            on_click=navigate, args=(i,),
                            use_container_width=True)

    st.caption(f"{count} attractions in your adventure plan")
    st.divider()
    st.markdown("#### 📧 Email Your Itinerary")
    st.write("Want to keep a copy of your adventure plan?")

    email_address = st.text_input(
        "Email address", placeholder="you@example.com", key="planner_email"
    )
    if st.button("Send My Itinerary", type="primary", use_container_width=True):
        if not validate_email(email_address):
            st.warning("Please enter a valid email address.")
        else:
            try:
                with st.spinner("Sending your itinerary..."):
                    send_itinerary_email(
                        recipient=email_address.strip(),
                        itinerary=itinerary_details
                    )
                st.success("Your itinerary has been emailed!")
            except Exception as e:
                st.error(f"Failed to send email: {type(e).__name__}")

    if st.button("Close", key="close_itinerary", use_container_width=True):
        st.session_state.planner_generated = False
        st.rerun()


if st.session_state.planner_generated and selected_names:
    # Preserve the order chosen by the visitor.
    rides_by_name = {item["details"]["name"]: item for item in all_rides}
    itinerary_details = []

    for name in selected_names:
        if name not in rides_by_name:
            continue
        item = rides_by_name[name]
        ride = item["details"]
        itinerary_details.append({
            "name": name,
            "category": item["category"],
            "image": ride["image"],
            "ride_duration": ride["duration"]
        })

    # Consume the open request so dismissing the modal does not reopen it.
    st.session_state.planner_generated = False
    if itinerary_details:
        show_itinerary(itinerary_details)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

show_footer()
