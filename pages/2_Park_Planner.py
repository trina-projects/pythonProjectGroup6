import streamlit as st
from datetime import date
from database.attractions import attractions, shows, vibe_categories
from src.validation import generate_itinerary

st.title("Your Adventure, Your Way")

st.write(
    "Let us help you plan your perfect day "
    "at WonderWorld!"
)

# Initialise session state
if "step" not in st.session_state:
    st.session_state.step = 1

if "visit_date" not in st.session_state:
    st.session_state.visit_date = date.today()

if "preferences" not in st.session_state:
    st.session_state.preferences = []

if "vibe" not in st.session_state:
    st.session_state.vibe = None

# Initialise session state
if "adults" not in st.session_state:
    st.session_state.adults = 1

if "children" not in st.session_state:
    st.session_state.children = 0

# Centre the form
left, middle, right = st.columns([1, 2, 1])

with middle:

    with st.container(border=True):

        # Progress indicator
        st.progress(
            st.session_state.step / 4
        )

        st.caption(
            f"Step {st.session_state.step} of 4"
        )

        # STEP 1
        if st.session_state.step == 1:

            st.subheader("When are you visiting?")

            visiting_date = st.date_input(
                "Select your visiting date",
                value=st.session_state.visit_date,
                min_value=date.today()
            )

            if st.button("Next"):

                st.session_state.visit_date = visiting_date

                st.session_state.step = 2

                st.rerun()

        # STEP 2
        elif st.session_state.step == 2:

            st.subheader("What's your adventure vibe?")

            st.write(
                "Tell us what kind of experience you're looking for!"
            )
            vibes = list(vibe_categories.keys())

            saved_vibe = st.session_state.vibe
            selected_vibe = st.radio(
                "Choose your adventure vibe",
                options=vibes,
                index=vibes.index(saved_vibe) if saved_vibe in vibes else None,
                key="vibe_selection"
            )

            back, next_button = st.columns(2)

            with back:
                if st.button("Back", key="back_step2"):
                    st.session_state.step = 1
                    st.rerun()

            with next_button:
                if st.button("Next", key="next_step2"):

                    if selected_vibe is None:
                        st.warning("Please select your adventure vibe!")

                    else:
                        st.session_state.vibe = selected_vibe
                        st.session_state.step = 3
                        st.rerun()

        # STEP 3 (Select number of people)
        elif st.session_state.step == 3:

            st.subheader("Who are you visiting with?")

            st.write(
                "Let us know how many people are joining your adventure!"
            )

            adults = st.number_input(
                "Number of adults",
                min_value=0,
                max_value=20,
                value=st.session_state.adults,
                step=1
            )

            children = st.number_input(
                "Number of children",
                min_value=0,
                max_value=20,
                value=st.session_state.children,
                step=1
            )

            back, next_button = st.columns(2)

            with back:
                if st.button("Back", key="back_step3"):
                    st.session_state.adults = adults
                    st.session_state.children = children
                    st.session_state.step = 2
                    st.rerun()

            with next_button:
                if st.button("Next", key="next_step3"):

                    if adults + children == 0:
                        st.warning(
                            "Please enter at least one visitor!"
                        )

                    else:
                        st.session_state.adults = adults
                        st.session_state.children = children
                        st.session_state.step = 4
                        st.rerun()
                
        # STEP 4 (Review your itinerary)
        # STEP 4 (Review Your Itinerary)
        elif st.session_state.step == 4:

            st.subheader("Your Personalised Itinerary 🎢")

            st.write(
                "We've put together an adventure "
                "based on your preferences!"
            )

            # Retrieve saved visitor information
            visit_date = st.session_state.visit_date
            selected_vibe = st.session_state.vibe
            adults = st.session_state.adults
            children = st.session_state.children

            # Generate itinerary
            itinerary = generate_itinerary(
                attractions,
                vibe_categories,
                selected_vibe
            )

            # Calculate total estimated duration
            total_duration = 0

            for ride in itinerary:
                total_duration += ride["total_time"]

            # Display visitor summary
            st.markdown("### Your Visit Details")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"📅 **Date:** {visit_date}")
                st.write(f"🌿 **Adventure Vibe:** {selected_vibe}")

            with col2:
                st.write(f"👥 **Adults:** {adults}")
                st.write(f"🧒 **Children:** {children}")

            st.divider()

            # Display itinerary statistics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Attractions",
                    len(itinerary)
                )

            with col2:
                st.metric(
                    "Estimated Duration",
                    f"{total_duration} min"
                )

            with col3:
                st.metric(
                    "Visitors",
                    adults + children
                )

            st.divider()

            st.markdown("### Your Recommended Attractions")

            if not itinerary:
                st.warning(
                    "No matching attractions were found. "
                    "Try choosing another adventure vibe."
                )

            else:
                for index, ride in enumerate(itinerary):

                    with st.container(border=True):

                        st.markdown(
                            f"### {index + 1}. {ride['name']}"
                        )

                        st.caption(ride["category"])

                        col1, col2 = st.columns(2)

                        with col1:
                            st.write(
                                f"🎢 Ride Duration: "
                                f"{ride['duration']} min"
                            )

                        with col2:
                            st.write(
                                f"⏳ Estimated Wait: "
                                f"{ride['waiting_time']} min"
                            )

            st.caption(
                "Waiting times are estimates based on "
                "sample queue data and may vary."
            )

            # Navigation buttons
            back, restart = st.columns(2)

            with back:
                if st.button("Back", key="back_step4"):
                    st.session_state.step = 3
                    st.rerun()

            with restart:
                if st.button("Start Over", key="restart_planner"):
                    st.session_state.step = 1
                    st.session_state.vibe = None
                    st.session_state.preferences = []
                    st.session_state.adults = 1
                    st.session_state.children = 0
                    st.session_state.visit_date = date.today()
                    st.rerun()