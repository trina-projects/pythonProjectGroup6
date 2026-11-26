# =================================================
# PARK PLANNER PAGE
# select rides, arrange visit order and generate an itinerary
# =================================================
import streamlit as st
from pathlib import Path
from database.attractions import attractions
from src.init import (
    show_footer,
    PARK_LOCATION,
    PARK_HOURS
)

import html
from src.validation import send_itinerary_email, validate_email
#retrieve the absolute path of the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# =================================================
# ATTRACTION CARD DESIGN
# =================================================
st.html("""
<style>
    /* only target planner cards */
    .st-key-planner_cards [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        overflow: hidden;
    }

    /* standardise image dimensions */
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

    /* consistent description height keeps cards aligned */
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
# =================================================
# SESSION STATE
# =================================================

#initialise only once so selections persist across reruns
if "planner_selected" not in st.session_state:
    st.session_state.planner_selected = [] #stores selected ride names

if "planner_generated" not in st.session_state:
    st.session_state.planner_generated = False #controls whether the itinerary opens


# =================================================
# REORDER SELECTED ATTRACTIONS
# =================================================
def move_attraction(index, direction):
    selected = st.session_state.planner_selected

    new_index = index + direction #move up (-1) or down (+1)

    #validate that it is within the list, so no index of -1 or 4
    if new_index >= 0 and new_index < len(selected):
        #swap the two rides using a temporary variable
        temp = selected[index]
        selected[index] = selected[new_index]
        selected[new_index] = temp

        #reset itinerary after reordering
        st.session_state.planner_generated = False

# =================================================
# PAGE HEADING
# =================================================

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


# =================================================
# ATTRACTION DATA
# =================================================

def get_all_rides():
    items = []

    #key = category, value = list of rides
    for category, rides in attractions.items():
        for ride in rides:
            items.append({
                "category": category,
                "details": ride
            })

    return items


all_rides = get_all_rides() #retrieve all rides before filtering


# =================================================
# FILTERS
# =================================================

st.subheader("Explore Attractions")

st.write(
    "Select the rides you'd like to experience "
    "during your visit."
)

#retrieve category names from the database
category_filter = st.selectbox(
    "Filter by category",
    ["All Attractions"] + list(attractions.keys())
)

if category_filter == "All Attractions":
    filtered_rides = all_rides
else:
    filtered_rides = []
    for item in all_rides:
        if item["category"] == category_filter:
            filtered_rides.append(item)

# =================================================
# ATTRACTION CARDS
# =================================================
with st.container(key="planner_cards"):

    index = 0
    for item in filtered_rides:
        if index == 0: #create a new row of 3 columns
            columns = st.columns(3, gap="large")

        with columns[index]:
            ride = item["details"]
            name = ride["name"]

            with st.container(border=True):

                image_path = BASE_DIR / ride["image"]

                if image_path.is_file(): #validate image existence
                    st.image(
                        str(image_path),
                        use_container_width=True
                    )

                st.markdown(f"### {name}")

                st.caption(item["category"])

                #default description if key is missing
                description = ride.get("description", "Discover an unforgettable adventure!")

                st.html(f"""
                    <div class="planner-description">
                        {html.escape(description)}
                    </div>
                """)

                st.write(
                    f"🎢 Ride duration: {ride['duration']} min"
                )

                selected = name in st.session_state.planner_selected #check if ride is already selected

                #toggle between adding and removing a ride
                if selected:
                    if st.button("✔ Remove from Plan", key=f"remove_{name}", use_container_width=True):
                        st.session_state.planner_selected.remove(name)
                        st.session_state.planner_generated = False
                        st.rerun()

                else:
                    if st.button(
                        "+ Add to Plan",
                        key=f"add_{name}",
                        use_container_width=True,
                        type="primary"
                    ):
                        st.session_state.planner_selected.append(name)
                        st.session_state.planner_generated = False
                        st.rerun()
        index += 1 #move to the next column
        if index == 3:
            index = 0 #reset after filling all 3 columns

# =================================================
# ITINERARY SUMMARY
# =================================================
st.divider()

st.subheader("Your Adventure Plan")

selected_names = st.session_state.planner_selected #saved list in visit order

st.write(f"**{len(selected_names)} attractions selected**")

if len(selected_names) == 0: #nothing selected yet
    st.info("Your adventure starts here! Select some attractions to begin planning.")

else:
    st.caption("Use the arrows to rearrange the order of your attractions.")

    index = 0 #keep track of the current ride's position
    for name in selected_names:
        with st.container(border=True):
            name_col, up_col, down_col = st.columns([6, 1, 1], vertical_alignment="center")

            with name_col:
                st.write(f"**{index + 1}. {name}**")

            with up_col:
                if st.button(
                    "↑",
                    key=f"up_{name}",
                    disabled=(index == 0) #first ride cannot move up
                ):
                    move_attraction(index, -1)
                    st.rerun()

            with down_col:
                if st.button(
                    "↓",
                    key=f"down_{name}",
                    disabled=(index == len(selected_names) - 1) #last ride cannot move down
                ):
                    move_attraction(index, 1)
                    st.rerun()

        index += 1 #increment index for the next ride

    if st.button("Generate My Itinerary", type="primary", use_container_width=True):
        st.session_state.planner_generated = True #request to open itinerary dialog
        st.session_state.itinerary_index = 0 #start carousel from first ride

    if st.button("Clear Selection"): #reset the entire plan
        st.session_state.planner_selected = [] #empty selected rides list
        st.session_state.planner_generated = False #reset generation flag
        st.rerun()
# =================================================
# END OF ITINERARY SUMMARY
# =================================================

# =================================================
# GENERATE ITINERARY
# =================================================
#display itinerary in a pop-up window
@st.dialog("Your Adventure Itinerary", width="large")
def show_itinerary(itinerary): #parameter itinerary returns list of dictionaries
    count = len(itinerary)
    if count == 0:
        return #exit funcion if there is 0 items in itinerary

    if "itinerary_index" not in st.session_state: 
        st.session_state.itinerary_index = 0 #initialise carousel index

    index = st.session_state.itinerary_index

    #validation check to prevent IndexError
    if index < 0 or index >= count:
        index = 0
        st.session_state.itinerary_index = index

    ride = itinerary[index] #currently visible ride , returns dictionary

    st.html("""
        <div style="background:#DCEFED; padding:20px; border-radius:12px; text-align:center; color:#142B40;">
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

    #key = day, value = opening hours
    for day, hours in PARK_HOURS.items():
        st.write(f"{day}: {hours}")
    st.caption(f"Attraction {index + 1} of {count}") #e.g. "Attraction 1 of 3"

    # CAROUSEL NAVIGATION
    def navigate(new_index):
        if new_index >= count: #return to first ride
            new_index = 0
        elif new_index < 0: #return to last ride
            new_index = count - 1

        st.session_state.itinerary_index = new_index

    #narrow arrow columns on either side of the itinerary card
    previous, center, following = st.columns(
        [1, 8, 1], vertical_alignment="center"
    )
    # LEFT ARROW
    with previous:
        st.button("◀", key="itinerary_prev", disabled=count == 1, #disable navigation if only 1 ride
                    on_click=navigate, args=(index - 1,)) #onclick call nnavigation function, pass prev index into function

    # ITINERARY CARD
    with center:
        with st.container(key="itinerary_card", border=True):
            image_path = BASE_DIR / ride["image"]
            if image_path.is_file():
                st.image(str(image_path), use_container_width=True)
            else:
                st.caption("Attraction image unavailable")

            st.markdown(f"### {index + 1}. {ride['name']}")
            st.caption(ride["category"])
            st.write(f"🎢 Ride duration: {ride['ride_duration']} min")

    # RIGHT ARROW
    with following:
        st.button("▶︎", key="itinerary_next", disabled=count == 1, on_click=navigate, args=(index + 1,))

    # PAGINATION DOTS
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

        #dynamically generate collumn based on attraction no., with width of 2 on each side 
        dot_widths = [2]
        for i in range(count):
            dot_widths.append(1)
        dot_widths.append(2)
        dots = st.columns(dot_widths)
        for i in range(count):
            with dots[i + 1]: #i+1 because first and last column is empty space
                if i == index:
                    dot = "●" #active position
                else:
                    dot = "○"
                st.button(dot,key=f"itinerary_dot_{i}",on_click=navigate, args=(i,),use_container_width=True)

    st.caption(f"{count} attractions in your adventure plan")
    st.divider()
    # EMAIL ITINERARY
    st.markdown("#### 📧 Email Your Itinerary")
    st.write("Want to keep a copy of your adventure plan?")

    email_address = st.text_input("Email address", placeholder="you@example.com", key="planner_email")
    if st.button("Send My Itinerary", type="primary", use_container_width=True):
        if not validate_email(email_address): #validate before sending
            st.warning("Please enter a valid email address.")
        else:
            try:
                with st.spinner("Sending your itinerary..."):
                    send_itinerary_email(recipient=email_address.strip(),itinerary=itinerary)
                st.success("Your itinerary has been emailed!")
            except Exception as e: #display error if email fails
                st.error(f"Failed to send email: {type(e).__name__}")

    if st.button("Close", key="close_itinerary", use_container_width=True):
        st.session_state.planner_generated = False
        st.rerun()
# =================================================
# END OF GENERATE ITINERARY
# =================================================

# =================================================
# RETRIEVE SELECTED ITINERARY AND OPEN DIALOG
# =================================================
if st.session_state.planner_generated and selected_names:
    #store a dictionary of ride names 
    rides_by_name = {} 
    for item in all_rides:
        name = item["details"]["name"]
        rides_by_name[name] = item
    itinerary_details = []

    #preserve the order chosen by visitor
    for name in selected_names:
        if name not in rides_by_name:
            continue #skip rides that no longer exist
        item = rides_by_name[name] #get key
        ride = item["details"] #get key[value]
        itinerary_details.append({
            "name": name,
            "category": item["category"],
            "image": ride["image"],
            "ride_duration": ride["duration"]
        })

    #reset open request so closing the dialog does not reopen it
    st.session_state.planner_generated = False
    if len(itinerary_details) > 0: 
        show_itinerary(itinerary_details) #trigger show itinerary func

# =================================================
# FOOTER
# =================================================

#shared footer imported from src/init.py
show_footer()
