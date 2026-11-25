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
            "image": "assets/attractions/thrill rides/skyDrop.jpg",

            "description": "Rise high above WonderWorld before experiencing an exhilarating free-fall drop.",
            "type": "Free-fall Drop Tower",
            "location": "Adventure Zone",
            "height_restriction": "Minimum 130 cm",
            "advisory": "Not recommended for pregnant guests or guests with heart, neck or back conditions."
        }
    ],

    "Water Rides": [
        {
            "name": "Rocket Hydro",
            "capacity": 16,
            "duration": 8,
            "image": "assets/attractions/water rides/rocketHydro.jpg",

            "description": "Race through exciting water channels, unexpected twists and refreshing splashes.",
            "type": "Water Coaster",
            "location": "Splash Zone",
            "height_restriction": "Minimum 110 cm",
            "advisory": "Guests may get wet. Secure loose belongings before boarding."
        },
        {
            "name": "Tidal Wave",
            "capacity": 12,
            "duration": 10,
            "image": "assets/attractions/water rides/tidalWave.jpg",

            "description": "Navigate rushing rapids and unpredictable waves on a splashing adventure with friends and family.",
            "type": "River Rapids Ride",
            "location": "Splash Zone",
            "height_restriction": "Minimum 100 cm",
            "advisory": "Guests may get completely soaked. Young children must be accompanied by an adult."
        }
    ],

    "Family Rides": [
        {
            "name": "Magic Carousel",
            "capacity": 30,
            "duration": 5,
            "image": "assets/attractions/family rides/magicCarousel.jpg",

            "description": "Take a magical spin on beautifully decorated carousel horses accompanied by enchanting music.",
            "type": "Traditional Carousel",
            "location": "Fantasy Village",
            "height_restriction": "Guests below 90 cm must be accompanied by an adult",
            "advisory": "Young children must remain supervised throughout the ride."
        },
        {
            "name": "Umbrella Coast",
            "capacity": 40,
            "duration": 12,
            "image": "assets/attractions/family rides/umbrellaCoast.webp",

            "description": "Float beneath colourful umbrellas and enjoy a gentle, whimsical adventure suitable for the whole family.",
            "type": "Family Aerial Ride",
            "location": "Fantasy Village",
            "height_restriction": "Minimum 90 cm",
            "advisory": "Guests sensitive to heights or circular motion should ride with caution."
        }
    ],

    "Scenic Rides": [
        {
            "name": "Alpine Express",
            "capacity": 48,
            "duration": 15,
            "image": "assets/attractions/scenic rides/alpineExpress.jpg",

            "description": "Embark on a relaxing railway journey through picturesque landscapes and scenic mountain surroundings.",
            "type": "Scenic Railway",
            "location": "Alpine Valley",
            "height_restriction": "No minimum height requirement",
            "advisory": "Guests must remain seated throughout the journey."
        },
        {
            "name": "Ancient Cruiser",
            "capacity": 20,
            "duration": 10,
            "image": "assets/attractions/scenic rides/ancientCruiser.webp",

            "description": "Cruise through tranquil waterways and discover mysterious ancient ruins along the way.",
            "type": "Scenic Boat Ride",
            "location": "Ancient Kingdom",
            "height_restriction": "No minimum height requirement",
            "advisory": "Young children must be accompanied by an adult. Remain seated throughout the ride."
        }
    ],

    "Adventure Rides": [
        {
            "name": "Jungle Expedition",
            "capacity": 16,
            "duration": 8,
            "image": "assets/attractions/adventure rides/jungleExpedition.jpg",

            "description": "Journey deep into a mysterious jungle filled with hidden treasures, exotic scenery and unexpected surprises.",
            "type": "Jungle Exploration Ride",
            "location": "Adventure Zone",
            "height_restriction": "Minimum 100 cm",
            "advisory": "Contains sudden movements, loud sounds and dimly lit environments."
        },
        {
            "name": "Mystery Mine",
            "capacity": 24,
            "duration": 6,
            "image": "assets/attractions/adventure rides/mysteryMine.webp",

            "description": "Venture into an abandoned mine and uncover its hidden secrets through dark tunnels and thrilling twists.",
            "type": "Indoor Adventure Coaster",
            "location": "Ancient Kingdom",
            "height_restriction": "Minimum 110 cm",
            "advisory": "Contains dark environments, flashing lights, sudden movements and loud sounds."
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
            "image": "assets/shows/echoesOfTheAncient.jpg",

            "type": "Fireworks & Light Spectacular",
            "location": "Ancient Kingdom",
            "height_restriction": "No minimum height requirement",
            "advisory": "Contains fireworks, flashing lights and loud sounds."
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
            "image": "assets/shows/wingsOfTime.jpg",

            "type": "Live Parade & Musical Performance",
            "location": "WonderWorld Main Street",
            "height_restriction": "No minimum height requirement",
            "advisory": "Guests should remain within designated viewing areas throughout the performance."
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
            "image": "assets/shows/dreamweaversTent.jpg",

            "type": "Live Theatrical Performance",
            "location": "Fantasy Village",
            "height_restriction": "No minimum height requirement",
            "advisory": "Contains theatrical lighting, sound effects and occasional loud music."
        }
    ]
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

