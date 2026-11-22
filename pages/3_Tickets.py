import streamlit as st
from datetime import date
from src.validation import calculate_total
from src.init import show_footer

# Page styling
st.html("""
<style>
    .ticket-heading {
        color: #142B40;
        font-size: 46px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .ticket-subtitle {
        color: #666666;
        font-size: 18px;
        margin-bottom: 35px;
    }

    .ticket-section {
        color: #142B40;
        font-size: 23px;
        font-weight: 600;
    }
</style>
""")


# Page heading
st.html("""
<h1 class="ticket-heading">
    Tickets & Admission
</h1>

<p class="ticket-subtitle">
    Your adventure starts here!
    Choose your tickets and get ready
    for a magical day at WonderWorld.
</p>
""")


# Two-column layout
left, right = st.columns([1.6, 1], gap="large")


# LEFT: Ticket selection
with left:

    with st.container(border=True):

        st.subheader("📅 Select Your Visit")

        visit_date = st.date_input(
            "Visit Date",
            value=date.today(),
            min_value=date.today()
        )

        st.divider()

        st.subheader("🎟️ Select Your Tickets")

        adult_col, adult_quantity = st.columns([3, 1])

        with adult_col:
            st.markdown("**Adult Ticket**")
            st.caption("Ages 13 and above")
            st.write("S$60.00")

        with adult_quantity:
            adults = st.number_input(
                "Adults",
                min_value=0,
                max_value=20,
                value=0,
                step=1
            )

        st.divider()

        child_col, child_quantity = st.columns([3, 1])

        with child_col:
            st.markdown("**Child Ticket**")
            st.caption("Ages 4–12")
            st.write("S$40.00")

        with child_quantity:
            children = st.number_input(
                "Children",
                min_value=0,
                max_value=20,
                value=0,
                step=1
            )


# RIGHT: Booking summary
with right:

    with st.container(border=True):

        st.subheader("Booking Summary")

        st.write("**Visit Date**")
        st.write(visit_date.strftime("%d %B %Y"))

        st.divider()

        st.write(
            f"Adult Tickets: {adults} × S$60"
        )

        st.write(
            f"Child Tickets: {children} × S$40"
        )

        total = calculate_total(adults, children)

        st.divider()

        st.markdown("### Total")

        st.title(f"S${total:.2f}")

        if st.button(
            "Confirm Booking",
            type="primary",
            use_container_width=True
        ):

            if adults + children == 0:
                st.warning(
                    "Please select at least one ticket."
                )

            else:
                st.success(
                    "Your booking has been confirmed!"
                )

                st.write(
                    f"Visit Date: {visit_date}"
                )

                st.write(
                    f"Total Tickets: {adults + children}"
                )

                st.write(
                    f"Total Amount: S${total:.2f}"
                )

# ###############################################################
# ########################## FOOTER #############################
# ###############################################################

show_footer()