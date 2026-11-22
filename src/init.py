#################################################################
############################ FOOTER #############################
#################################################################
import streamlit as st

def show_footer():
    st.html("""
        <style>
            .wonder-footer {
                background-color: #142B40;
                color: #ffffff;

                /* Full-width footer */
                width: 100vw;
                max-width: 100vw;
                position: relative;
                left: 50%;
                transform: translateX(-50%);

                /* Spacing */
                padding: 65px 40px 25px;
                margin-top: 60px;
                margin-bottom: 0;

                box-sizing: border-box;
            }

            .footer-content {
                max-width: 1200px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: 2fr 1fr 1fr;
                gap: 50px;
            }

            .footer-brand {
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 15px;
            }

            .footer-heading {
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 18px;
            }

            .wonder-footer p {
                color: #cccccc;
                line-height: 1.8;
            }

            .footer-links a {
                display: block;
                color: #cccccc;
                text-decoration: none;
                margin-bottom: 12px;
            }

            .footer-links a:hover {
                color: #ffffff;
                text-decoration: underline;
            }

            .footer-bottom {
                max-width: 1200px;
                margin: 45px auto 0;
                padding-top: 20px;
                border-top: 1px solid #526273;
                text-align: center;
                color: #bbbbbb;
                font-size: 14px;
            }

            @media (max-width: 700px) {
                .footer-content {
                    grid-template-columns: 1fr;
                    gap: 25px;
                }
            }
            /* Remove extra bottom padding from Streamlit's page container */
            [data-testid="stMainBlockContainer"] {
                padding-bottom: 0 !important;
            }

            /* Prevent horizontal overflow from full-width sections */
            [data-testid="stMain"] {
                overflow-x: clip;
            }
        </style>

        <footer class="wonder-footer">

            <div class="footer-content">

                <div>
                    <h2 class="footer-brand">🎡 WonderWorld</h2>
                    <p>
                        Where every adventure begins!
                        Discover thrilling rides, magical
                        experiences and unforgettable memories.
                    </p>
                </div>

                <div class="footer-links">
                    <h3 class="footer-heading">Explore</h3>
                    <a href="/">Home</a>
                    <a href="/Attractions">Attractions</a>
                    <a href="/Park_Planner">Plan My Visit</a>
                </div>

                <div>
                    <h3 class="footer-heading">Visitor Information</h3>
                    <p>Opening Hours</p>
                    <p>Tickets & Admission</p>
                    <p>Park Information</p>
                </div>

            </div>

            <div class="footer-bottom">
                © 2026 WonderWorld. All rights reserved.
                <p>Theme park · Programming Group 6</p>
            </div>

        </footer>
    """)
