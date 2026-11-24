
import streamlit as st
from datetime import date

from src.validation import (
    get_day_type,
    get_ticket_prices,
    calculate_booking,
    validate_booking
)

from src.validation import send_ticket_receipt
from src.init import show_footer


# ###############################################################
# ######################## PAGE STYLING #########################
# ###############################################################

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
        margin-bottom: 30px;
    }

    .ticket-info {
        background-color: #E8F3F2;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
        color: #142B40;
    }

    .ticket-price {
        color: #142B40;
        font-size: 24px;
        font-weight: 700;
        margin: 5px 0;
    }

    .ticket-day-peak {
        display: inline-block;
        background-color: #FCE8CD;
        color: #925B13;
        border-radius: 20px;
        padding: 6px 14px;
        font-weight: 600;
    }

    .ticket-day-nonpeak {
        display: inline-block;
        background-color: #DCEFED;
        color: #246B62;
        border-radius: 20px;
        padding: 6px 14px;
        font-weight: 600;
    }
</style>
""")


# ###############################################################
# ######################## PAGE HEADING #########################
# ###############################################################

st.html("""
<h1 class="ticket-heading">
    Tickets & Admission
</h1>

<p class="ticket-subtitle">
    Your adventure starts here!
    Find the perfect ticket for a magical day at WonderWorld.
</p>
""")


# ###############################################################
# ######################## SESSION STATE ########################
# ###############################################################

if "ticket_adults" not in st.session_state:
    st.session_state.ticket_adults = 0

if "ticket_children" not in st.session_state:
    st.session_state.ticket_children = 0

if "ticket_families" not in st.session_state:
    st.session_state.ticket_families = 0


# Callback to preserve quantities when switching ticket types
def update_quantity(widget_key, state_key):
    st.session_state[state_key] = st.session_state[widget_key]


# ###############################################################
# ######################## PAGE LAYOUT ##########################
# ###############################################################

left, right = st.columns([1.6, 1], gap="large")


# ###############################################################
# ######################## TICKET SELECTION #####################
# ###############################################################

with left:

    with st.container(border=True):

        st.subheader("📅 Select Your Visit")

        visit_date = st.date_input(
            "Visit Date",
            value=date.today(),
            min_value=date.today()
        )

        day_type = get_day_type(visit_date)
        prices = get_ticket_prices(visit_date)

        if day_type == "Peak":

            st.html("""
                <span class="ticket-day-peak">
                    Peak Day
                </span>
            """)

            st.caption(
                "Weekend admission rates apply."
            )

        else:

            st.html("""
                <span class="ticket-day-nonpeak">
                    Non-Peak Day
                </span>
            """)

            st.caption(
                "Enjoy our weekday admission rates!"
            )

        with st.expander("View admission prices"):

            st.markdown("""
| Ticket | Non-Peak | Peak |
|---|---:|---:|
| Adult | S$60 | S$75 |
| Child | S$40 | S$50 |
| Family Bundle | S$170 | S$210 |
            """)

            st.caption(
                "Non-Peak: Monday–Friday. "
                "Peak: Saturday–Sunday."
            )

        st.divider()

        st.subheader("🎟️ Select Your Tickets")

        ticket_type = st.radio(
            "Ticket Category",
            ["Standard Admission", "Family Bundle"],
            horizontal=True,
            label_visibility="collapsed"
        )


        # STANDARD ADMISSION
        if ticket_type == "Standard Admission":

            st.html("""
                <div class="ticket-info">
                    <b>Standard One-Day Admission</b>
                    <p>
                        Enjoy a full day of adventure with
                        access to WonderWorld attractions
                        and entertainment.
                    </p>
                </div>
            """)

            # Adult tickets
            adult_col, adult_quantity = st.columns([3, 1.3])

            with adult_col:

                st.markdown("**Adult Ticket**")
                st.caption("Ages 13 and above")

                st.html(
                    f'<div class="ticket-price">'
                    f'S${prices["adult"]:.2f}'
                    f'</div>'
                )

                st.caption("Per person")

            with adult_quantity:

                st.number_input(
                    "Adults",
                    min_value=0,
                    max_value=20,
                    value=st.session_state.ticket_adults,
                    step=1,
                    key="adult_quantity_widget",
                    on_change=update_quantity,
                    args=(
                        "adult_quantity_widget",
                        "ticket_adults"
                    )
                )

            st.divider()

            # Child tickets
            child_col, child_quantity = st.columns([3, 1.3])

            with child_col:

                st.markdown("**Child Ticket**")
                st.caption("Ages 4–12")

                st.html(
                    f'<div class="ticket-price">'
                    f'S${prices["child"]:.2f}'
                    f'</div>'
                )

                st.caption("Per person")

            with child_quantity:

                st.number_input(
                    "Children",
                    min_value=0,
                    max_value=20,
                    value=st.session_state.ticket_children,
                    step=1,
                    key="child_quantity_widget",
                    on_change=update_quantity,
                    args=(
                        "child_quantity_widget",
                        "ticket_children"
                    )
                )


        # FAMILY BUNDLE
        elif ticket_type == "Family Bundle":

            savings = (
                prices["adult"] * 2
                + prices["child"] * 2
                - prices["family"]
            )

            st.html("""
                <div class="ticket-info">
                    <b>Family Adventure Bundle</b>
                    <p>
                        Create unforgettable memories
                        with the entire family!
                    </p>
                    Includes:
                    <ul>
                        <li>2 Adult Tickets</li>
                        <li>2 Child Tickets</li>
                        <li>Full-day park admission</li>
                    </ul>
                </div>
            """)

            family_col, family_quantity = st.columns([3, 1.3])

            with family_col:

                st.markdown("**Family Adventure Bundle**")

                st.html(
                    f'<div class="ticket-price">'
                    f'S${prices["family"]:.2f}'
                    f'</div>'
                )

                st.caption("Per family of four")

                st.success(
                    f"Save S${savings:.2f} per bundle!"
                )

            with family_quantity:

                st.number_input(
                    "Bundles",
                    min_value=0,
                    max_value=10,
                    value=st.session_state.ticket_families,
                    step=1,
                    key="family_quantity_widget",
                    on_change=update_quantity,
                    args=(
                        "family_quantity_widget",
                        "ticket_families"
                    )
                )

        st.divider()

        with st.expander("Terms & Conditions"):

            st.markdown("""
- Tickets are valid for the selected visit date.
- Children aged 4–12 require a child ticket.
- Children below 4 enjoy complimentary admission.
- Children must be accompanied by an adult.
- Family bundles include 2 adults and 2 children.
- All bookings are simulated for demonstration purposes.
            """)


# ###############################################################
# ######################## BOOKING SUMMARY ######################
# ###############################################################

adults = st.session_state.ticket_adults
children = st.session_state.ticket_children
families = st.session_state.ticket_families

booking = calculate_booking(
    adults,
    children,
    families,
    visit_date
)


with right:

    with st.container(border=True):

        st.subheader("Booking Summary")

        st.markdown("**Visit Date**")
        st.write(visit_date.strftime("%d %B %Y"))

        st.caption(f"{booking['day_type']} Admission")

        st.divider()

        # Adult ticket subtotal
        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(f"Adult Tickets × {adults}")

        with col2:
            st.write(f"S${booking['adult_total']:.2f}")


        # Child ticket subtotal
        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(f"Child Tickets × {children}")

        with col2:
            st.write(f"S${booking['child_total']:.2f}")


        # Family bundle subtotal
        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(f"Family Bundles × {families}")

        with col2:
            st.write(f"S${booking['family_total']:.2f}")


        st.divider()

        st.write(
            f"**Total Ticketed Visitors:** "
            f"{booking['total_visitors']}"
        )

        st.caption(
            f"{booking['total_adults']} adults · "
            f"{booking['total_children']} children"
        )

        if booking["family_savings"] > 0:

            st.success(
                f"You're saving "
                f"S${booking['family_savings']:.2f}!"
            )

        st.markdown("### Total Amount")

        st.title(f"S${booking['total']:.2f}")

        st.divider()

        st.markdown("#### 📧 Email Your Receipt")

        receipt_email = st.text_input(
            "Email Address",
            placeholder="you@example.com",
            key="ticket_receipt_email"
        )

        if st.button(
            "Confirm Booking",
            type="primary",
            use_container_width=True
        ):

            valid, message = validate_booking(
                adults,
                children,
                families,
                visit_date,
                receipt_email
            )

            if not valid:

                st.warning(message)

            else:

                try:

                    with st.spinner("Sending your receipt..."):

                        send_ticket_receipt(
                            recipient=receipt_email.strip(),
                            visit_date=visit_date,
                            adults=adults,
                            children=children,
                            families=families,
                            booking=booking
                        )

                    st.success(
                        "Booking receipt emailed successfully!"
                    )

                except Exception:

                    st.error(
                        "Unable to send your receipt. "
                        "Please try again."
                    )

        if st.button(
            "Clear Selection",
            use_container_width=True
        ):

            st.session_state.ticket_adults = 0
            st.session_state.ticket_children = 0
            st.session_state.ticket_families = 0

            for key in [
                "adult_quantity_widget",
                "child_quantity_widget",
                "family_quantity_widget"
            ]:
                st.session_state.pop(key, None)

            st.rerun()


# ###############################################################
# ########################## FOOTER #############################
# ###############################################################

show_footer()
