import random
attractions = {
    "Thrill Rides": [
        {
            "name": "Mega Coaster",
            "capacity": 24,
            "duration": 5,
            "image": "assets/attractions/thrill rides/megaCoaster.jpg",

            "description": "Experience high-speed turns and thrilling drops.",
            "type": "High-speed Roller Coaster",
            "location": "Adventure Zone",
            "height_restriction": "Minimum 120 cm",
            "advisory": "Not recommended for guests with certain medical conditions."
        },
        {
            "name": "Sky Drop",
            "capacity": 20,
            "duration": 3,
            "image": "assets/attractions/thrill rides/skyDrop.jpg"
        }
    ],

    "Water Rides": [
        {
            "name": "Rocket Hydro",
            "capacity": 16,
            "duration": 8,
            "image": "assets/attractions/water rides/rocketHydro.jpg"
        },
        {
            "name": "Tidal Wave",
            "capacity": 12,
            "duration": 10,
            "image": "assets/attractions/water rides/tidalWave.jpg"
        }
    ],

    "Family Rides": [
        {
            "name": "Magic Carousel",
            "capacity": 30,
            "duration": 5,
            "image": "assets/attractions/family rides/magicCarousel.jpg"
        },
        {
            "name": "Umbrella Coast",
            "capacity": 40,
            "duration": 12,
            "image": "assets/attractions/family rides/umbrellaCoast.webp"
        }
    ],

    "Scenic Rides": [
        {
            "name": "Alpine Express",
            "capacity": 48,
            "duration": 15,
            "image": "assets/attractions/scenic rides/alpineExpress.jpg"
        },
        {
            "name": "Ancient Cruiser",
            "capacity": 20,
            "duration": 10,
            "image": "assets/attractions/scenic rides/ancientCruiser.webp"
        }
    ],

    "Adventure Rides": [
        {
            "name": "Jungle Expedition",
            "capacity": 16,
            "duration": 8,
            "image": "assets/attractions/adventure rides/jungleExpedition.jpg"
        },
        {
            "name": "Mystery Mine",
            "capacity": 24,
            "duration": 6,
            "image": "assets/attractions/adventure rides/mysteryMine.webp"
        }
    ]
}

shows = {
    "Shows & Entertainment": [
        {
            "name": "Echoes of the Ancients",
            "description": (
                "End your adventure with breathtaking "
                "fireworks, dazzling lights and magical music."
            ),
            "capacity": 500,
            "duration": 20,
            "show_times": ["19:30"],
            "image": "assets/shows/echoesOfTheAncient.jpg"
        },
        {
            "name": "Wings of Time",
            "description": (
                "Celebrate with colourful floats, lively "
                "performers and enchanting music."
            ),
            "capacity": 300,
            "duration": 30,
            "show_times": ["14:00", "17:00"],
            "image": "assets/shows/wingsOfTime.jpg"
        },
        {
            "name": "The Dreamweaver’s Tent",
            "description": (
                "Step into a magical world of storytelling, "
                "music and spectacular live performances."
            ),
            "capacity": 200,
            "duration": 25,
            "show_times": ["11:00", "15:30"],
            "image": "assets/shows/dreamweaversTent.jpg"
        }
    ]
}

category_descriptions = {
    "Thrill Rides": (
        "Get your adrenaline pumping with exhilarating "
        "drops, high-speed turns and unforgettable adventures."
    ),

    "Water Rides": (
        "Dive into refreshing adventures and make a "
        "splash with our exciting water attractions."
    ),

    "Family Rides": (
        "Create magical memories together with delightful "
        "attractions for the whole family."
    ),

    "Scenic Rides": (
        "Take a moment to unwind and enjoy breathtaking "
        "views as you journey through WonderWorld."
    ),

    "Adventure Rides": (
        "Embark on exciting expeditions and discover "
        "hidden wonders around every corner."
    )
}

vibe_categories = {
    "Chill & Relaxing": [
        "Scenic Rides",
        "Family Rides"
    ],

    "Thrill Seeker": [
        "Thrill Rides",
        "Adventure Rides"
    ],

    "Fun & Playful": [
        "Family Rides",
        "Water Rides"
    ],

    "A Bit of Everything": random.sample(list(attractions.keys()),5)
}

ticket_prices = {
    "Non-Peak": {
        "adult": 60,
        "child": 40,
        "family": 170
    },
    "Peak": {
        "adult": 75,
        "child": 50,
        "family": 210
    }
}

