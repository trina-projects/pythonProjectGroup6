import random

attractions = {
    "Thrill Rides": [
        {
            "name": "Mega Coaster",
            "capacity": 24,
            "duration": 5,
            "queue_length": 120,
            "image": "assets/attractions/thrill rides/megaCoaster.jpg",
            "description": (
                "Experience high-speed turns, thrilling drops and "
                "heart-pounding excitement on WonderWorld's "
                "ultimate roller coaster adventure."
            ),
            "type": "High-speed Roller Coaster",
            "location": "Adventure Zone",
            "height_restriction": "Minimum 120 cm",
            "advisory": (
                "Not recommended for guests with heart conditions, "
                "back or neck problems, or motion sickness. "
                "Secure all loose belongings before boarding."
            )
        },
        {
            "name": "Sky Drop",
            "capacity": 20,
            "duration": 3,
            "queue_length": 80,
            "image": "assets/attractions/thrill rides/skyDrop.jpg",
            "description": (
                "Rise high above WonderWorld before experiencing "
                "a breathtaking free-fall that will leave your "
                "heart racing and your adrenaline soaring."
            ),
            "type": "Drop Tower",
            "location": "Adventure Zone",
            "height_restriction": "Minimum 130 cm",
            "advisory": (
                "This attraction features sudden vertical drops "
                "and intense movements. Not recommended for "
                "guests with heart conditions, back problems "
                "or a fear of heights."
            )
        }
    ],

    "Water Rides": [
        {
            "name": "Rocket Hydro",
            "capacity": 16,
            "duration": 8,
            "queue_length": 64,
            "image": "assets/attractions/water rides/rocketHydro.jpg",
            "description": (
                "Blast through rushing rapids, sharp turns and "
                "unexpected splashes as you race along an "
                "action-packed water adventure."
            ),
            "type": "High-speed Water Ride",
            "location": "Splash Bay",
            "height_restriction": "Minimum 110 cm",
            "advisory": (
                "Guests may get wet during this attraction. "
                "Waterproof bags are recommended for personal "
                "belongings. Guests with back or neck conditions "
                "should avoid this ride."
            )
        },
        {
            "name": "Tidal Wave",
            "capacity": 12,
            "duration": 10,
            "queue_length": 48,
            "image": "assets/attractions/water rides/tidalWave.jpg",
            "description": (
                "Prepare for an unforgettable splash as you "
                "navigate winding waterways, climb to exciting "
                "heights and plunge into a giant wave."
            ),
            "type": "Water Flume Ride",
            "location": "Splash Bay",
            "height_restriction": (
                "Minimum 100 cm. Children under 120 cm "
                "must be accompanied by an adult."
            ),
            "advisory": (
                "Expect large splashes and wet seating areas. "
                "Keep electronic devices protected and "
                "follow all safety instructions."
            )
        }
    ],

    "Family Rides": [
        {
            "name": "Magic Carousel",
            "capacity": 30,
            "duration": 5,
            "queue_length": 45,
            "image": "assets/attractions/family rides/magicCarousel.jpg",
            "description": (
                "Step into a world of wonder aboard our "
                "beautifully decorated carousel, where "
                "enchanting music and magical creatures "
                "bring timeless childhood memories to life."
            ),
            "type": "Classic Merry-Go-Round",
            "location": "Fantasy Gardens",
            "height_restriction": (
                "No minimum height. Young children "
                "must be accompanied by an adult."
            ),
            "advisory": (
                "Suitable for families and younger guests. "
                "Children must remain seated throughout "
                "the ride and follow staff instructions."
            )
        },
        {
            "name": "Umbrella Coast",
            "capacity": 40,
            "duration": 12,
            "queue_length": 60,
            "image": "assets/attractions/family rides/umbrellaCoast.webp",
            "description": (
                "Float gently through a colourful world of "
                "spinning umbrellas and whimsical scenery "
                "as you enjoy a delightful journey with "
                "family and friends."
            ),
            "type": "Gentle Rotating Ride",
            "location": "Fantasy Gardens",
            "height_restriction": (
                "Minimum 90 cm. Children under 120 cm "
                "must be accompanied by an adult."
            ),
            "advisory": (
                "This attraction features gentle spinning "
                "movements. Guests who are sensitive to "
                "motion should exercise caution."
            )
        }
    ],

    "Scenic Rides": [
        {
            "name": "Alpine Express",
            "capacity": 48,
            "duration": 15,
            "queue_length": 72,
            "image": "assets/attractions/scenic rides/alpineExpress.jpg",
            "description": (
                "Embark on a peaceful train journey through "
                "picturesque mountains, lush forests and "
                "charming villages while discovering the "
                "natural beauty of WonderWorld."
            ),
            "type": "Scenic Railway",
            "location": "Alpine Valley",
            "height_restriction": (
                "No minimum height. Young children "
                "must be accompanied by an adult."
            ),
            "advisory": (
                "A relaxing experience suitable for guests "
                "of all ages. Remain seated while the train "
                "is moving and keep hands inside the carriage."
            )
        },
        {
            "name": "Ancient Cruiser",
            "capacity": 20,
            "duration": 10,
            "queue_length": 40,
            "image": "assets/attractions/scenic rides/ancientCruiser.webp",
            "description": (
                "Sail along tranquil waterways surrounded "
                "by ancient ruins, mysterious temples and "
                "breathtaking landscapes on a relaxing "
                "voyage through forgotten civilizations."
            ),
            "type": "Scenic Boat Ride",
            "location": "Ancient Kingdom",
            "height_restriction": (
                "No minimum height. Children under 120 cm "
                "must be accompanied by an adult."
            ),
            "advisory": (
                "This attraction features slow boat movements "
                "and occasional gentle rocking. Guests must "
                "remain seated and avoid leaning over the boat."
            )
        }
    ],

    "Adventure Rides": [
        {
            "name": "Jungle Expedition",
            "capacity": 16,
            "duration": 8,
            "queue_length": 32,
            "image": "assets/attractions/adventure rides/jungleExpedition.jpg",
            "description": (
                "Venture deep into an untamed jungle filled "
                "with hidden ruins, mysterious wildlife and "
                "unexpected surprises as you embark on an "
                "exciting expedition."
            ),
            "type": "Jungle Adventure Ride",
            "location": "Lost Jungle",
            "height_restriction": (
                "Minimum 100 cm. Children under 120 cm "
                "must be accompanied by an adult."
            ),
            "advisory": (
                "Features sudden movements, loud sound effects "
                "and dimly lit environments. Younger guests "
                "may find some scenes frightening."
            )
        },
        {
            "name": "Mystery Mine",
            "capacity": 24,
            "duration": 6,
            "queue_length": 96,
            "image": "assets/attractions/adventure rides/mysteryMine.webp",
            "description": (
                "Journey into the depths of an abandoned "
                "mine where glowing crystals, hidden tunnels "
                "and mysterious discoveries await around "
                "every corner."
            ),
            "type": "Indoor Mine Train Ride",
            "location": "Lost Jungle",
            "height_restriction": "Minimum 110 cm",
            "advisory": (
                "This attraction includes dark tunnels, "
                "flashing lights, sudden turns and loud "
                "sound effects. Not recommended for guests "
                "sensitive to flashing lights or sudden motion."
            )
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
            "name": "The Dreamweavers Tent",
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

