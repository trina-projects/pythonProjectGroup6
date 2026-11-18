import streamlit as st
from datetime import date
from database.attractions import attractions

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

            st.subheader(
                "What type of attractions "
                "are you looking for?"
            )

            selected = st.multiselect(
                "Select your preferred attractions",
                options=list(attractions.keys()),
                default=st.session_state.preferences
            )

            back, next_button = st.columns(2)

            with back:

                if st.button("Back"):

                    st.session_state.preferences = selected
                    st.session_state.step = 1
                    st.rerun()

            with next_button:

                if st.button("Next"):

                    if len(selected) == 0:

                        st.warning(
                            "Please select at least "
                            "one attraction category."
                        )

                    else:

                        st.session_state.preferences = selected

                        st.session_state.step = 3

                        st.rerun()

        # STEP 3 (Select number of people)
        elif st.session_state.step == 3:

            st.subheader("Who are you visiting with?")

            st.write("Number of adults, num of kids")
        
        # STEP 4 (Review your itinerary)
        elif st.session_state.step == 4:

            st.subheader("Review your itinerary")

            st.write("show itinerary")