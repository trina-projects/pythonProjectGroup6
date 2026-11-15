import streamlit as st
import base64
from pathlib import Path
from database.attractions import attractions, category_descriptions

BASE_DIR = Path(__file__).resolve().parent.parent


#################################################################
######################## HEADER DESIGN ##########################
#################################################################

BASE_DIR = Path(__file__).resolve().parent.parent

image_path = BASE_DIR / "assets/main/themeParkMain.webp"

with open(image_path, "rb") as image:
    encoded_image = base64.b64encode(image.read()).decode()

st.html(f"""
<style>

    .stApp {{
        background-color: #ffffff;
    }}

    .block-container {{
        padding-top: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100%;
    }}

    .hero-section {{
        background-image:
            linear-gradient(
                rgba(0, 0, 0, 0.3),
                rgba(0, 0, 0, 0.5)
            ),
            url("data:image/webp;base64,{encoded_image}");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;

        height: 85vh;

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        text-align: center;
    }}

    .rainbow-title {{
        background: linear-gradient(
            90deg,
            #ff0000,
            #ff9900,
            #ffff00,
            #00ff88,
            #00ccff,
            #aa55ff,
            #ff0000
        );

        background-size: 200% auto;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        animation: rainbowFlow 5s linear infinite;

        font-size: 60px;
        font-weight: bold;
        margin-bottom: 10px;
    }}

    @keyframes rainbowFlow {{
        from {{
            background-position: 200% center;
        }}
        to {{
            background-position: 0% center;
        }}
    }}

    .hero-subtitle {{
        color: white;
        font-size: 24px;
        margin-top: 10px;
    }}

</style>

<div class="hero-section">
    <h1 class="rainbow-title">
        Welcome to WonderWorld!
    </h1>
    <p class="hero-subtitle">
        Your adventure starts here!
    </p>
</div>
""")
#################################################################
##################### ATTRACTIONS DESIGN ########################
#################################################################

st.html("""
<style>

    /* Main attractions section */
    .st-key-attractions_grid {
        max-width: 1200px;
        margin: 0 auto;
        padding: 60px 30px;
        background-color: #ffffff;
    }

    /* Main section heading */
    .section-title {
        color: #142B40;
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Main section subtitle */
    .section-subtitle {
        color: #666666;
        text-align: center;
        font-size: 18px;
        margin-bottom: 40px;
    }

    /* Attraction images */
    .st-key-attractions_grid
    [data-testid="stImage"] img {
        width: 100%;
        aspect-ratio: 4 / 3;
        height: auto;
        object-fit: cover;
        border-radius: 3px;
    }

    /* Category title */
    .category-title {
        color: #142B40;
        font-size: 26px;
        font-weight: 500;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    /* Category description */
    .category-description {
        color: #444444;
        font-size: 17px;
        line-height: 1.8;
        margin-bottom: 15px;
    }

    /* Ride name tags */
    .ride-tag {
        display: inline-block;
        background-color: #f4f4f4;
        color: #333333;
        border: 1px solid #e5e5e5;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 13px;
        margin-right: 6px;
        margin-bottom: 8px;
    }

    /* Space between rows */
    .grid-spacing {
        height: 40px;
    }

</style>
""")
#################################################################
######################## ATTRACTIONS GRID #######################
#################################################################

with st.container(key="attractions_grid"):

    # Section heading
    st.html("""
        <h2 class="section-title">
            Explore WonderWorld
        </h2>

        <p class="section-subtitle">
            Discover an adventure for everyone!
        </p>
    """)

    # Select 5 categories for the 2x2 grid
    categories = list(attractions.keys())[:5]

    for i in range(0, len(categories), 2):

        columns = st.columns(2, gap="large")

        for col, category in zip(
            columns, categories[i:i + 2]
        ):

            with col:

                # Retrieve rides from the database
                rides = attractions[category]

                # Display category cover image
                image_path = rides[0]["image"]

                if image_path:
                    st.image(
                        str(BASE_DIR / image_path),
                        use_container_width=True
                    )

                # Category title
                st.html(f"""
                    <h3 class="category-title">
                        {category}
                    </h3>
                """)

                # Category description
                st.html(f"""
                    <p class="category-description">
                        {category_descriptions[category]}
                    </p>
                """)

                # Create ride name tags
                tags = ""

                for ride in rides:

                    tags += f"""
                        <span class="ride-tag">
                            {ride["name"]}
                        </span>
                    """

                st.html(tags)

                # Link to attractions page
                st.page_link(
                    "pages/1_Attractions.py",
                    label="Explore More"
                )

        # Add spacing between each row
        st.html('<div class="grid-spacing"></div>')