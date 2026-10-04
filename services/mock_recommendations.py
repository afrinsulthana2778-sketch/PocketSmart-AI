from urllib.parse import quote_plus


def search_url(
    platform: str,
    query: str,
) -> str:

    platforms = {

        "Amazon":
            "https://www.amazon.in/s?k=",

        "Flipkart":
            "https://www.flipkart.com/search?q=",

        "IKEA":
            "https://www.ikea.com/in/en/search/?q=",

        "Swiggy":
            "https://www.swiggy.com/search?query=",

        "Zomato":
            "https://www.zomato.com/search?q=",

        "OYO":
            "https://www.oyorooms.com/search?location=",
    }

    base_url = platforms.get(
        platform,
        "https://www.google.com/search?q=",
    )

    return base_url + quote_plus(query)


def home_mock(data):

    budget = data["budget"]

    items = [

        (
            "Ambient lighting set",
            min(budget * 0.08, 7000),
            "Amazon",
            "Warm, low-glare lighting for the main living area.",
        ),

        (
            "Ceiling fan",
            min(budget * 0.12, 6500),
            "IKEA",
            "Choose an energy-efficient model sized for the room.",
        ),

        (
            "Compact storage unit",
            min(budget * 0.22, 12000),
            "IKEA",
            "Useful for keeping frequently used items organized.",
        ),

        (
            "Accent decor bundle",
            min(budget * 0.10, 5500),
            "Amazon",
            "A small group of decor pieces rather than many separate purchases.",
        ),
    ]

    return {

        "summary":
            f"A balanced home setup for "
            f"{data['currency']} "
            f"{budget:,.0f}.",

        "budget_allocation": [

            {
                "category":
                    "Furniture & storage",

                "amount":
                    round(budget * 0.40, 2),

                "percentage":
                    40,
            },

            {
                "category":
                    "Lighting & fans",

                "amount":
                    round(budget * 0.25, 2),

                "percentage":
                    25,
            },

            {
                "category":
                    "Decor",

                "amount":
                    round(budget * 0.20, 2),

                "percentage":
                    20,
            },

            {
                "category":
                    "Contingency",

                "amount":
                    round(budget * 0.15, 2),

                "percentage":
                    15,
            },
        ],

        "recommendations": [

            {
                "title": title,

                "estimated_price":
                    round(price, 2),

                "platform": platform,

                "description": description,

                "search_url":
                    search_url(platform, title),

                "reason":
                    "Fits the requested budget and style.",
            }

            for title, price, platform, description
            in items
        ],

        "savings_tips": [

            "Buy large furniture first and compare dimensions before ordering.",

            "Keep a contingency amount for delivery or installation.",

            "Compare the same specification across at least two sellers before purchase.",
        ],
    }


def party_mock(data):

    budget = data["budget"]

    items = [

        (
            "Vegetarian catering package",
            budget * 0.35,
            "Swiggy",
            "Search for local catering or restaurant packages.",
        ),

        (
            "Venue shortlist",
            budget * 0.30,
            "OYO",
            "Use the platform to compare nearby stay/event options where available.",
        ),

        (
            "Decoration package",
            budget * 0.15,
            "Amazon",
            "Simple reusable decorations can reduce repeat costs.",
        ),

        (
            "Dessert and snacks",
            budget * 0.10,
            "Zomato",
            "Compare nearby restaurant and bakery options.",
        ),
    ]

    return {

        "summary":
            f"A practical "
            f"{data['event_type']} "
            f"plan for "
            f"{data['guest_count']} guests.",

        "budget_allocation": [

            {
                "category":
                    "Food & catering",

                "amount":
                    round(budget * 0.35, 2),

                "percentage":
                    35,
            },

            {
                "category":
                    "Venue",

                "amount":
                    round(budget * 0.30, 2),

                "percentage":
                    30,
            },

            {
                "category":
                    "Decoration",

                "amount":
                    round(budget * 0.15, 2),

                "percentage":
                    15,
            },

            {
                "category":
                    "Entertainment",

                "amount":
                    round(budget * 0.10, 2),

                "percentage":
                    10,
            },

            {
                "category":
                    "Contingency",

                "amount":
                    round(budget * 0.10, 2),

                "percentage":
                    10,
            },
        ],

        "recommendations": [

            {
                "title": title,

                "estimated_price":
                    round(price, 2),

                "platform": platform,

                "description": description,

                "search_url":
                    search_url(platform, title),

                "reason":
                    "A starting point for comparing options within the planned allocation.",
            }

            for title, price, platform, description
            in items
        ],

        "savings_tips": [

            "Ask vendors for a per-person quote before committing.",

            "Keep decoration reusable where possible.",

            "Reserve a contingency amount for last-minute guest changes.",
        ],
    }


def jewelry_mock(data):

    budget = data["budget"]

    items = [

        (
            "Minimal necklace",
            budget * 0.30,
            "Amazon",
            "A versatile option for an elegant occasion.",
        ),

        (
            "Matching earrings",
            budget * 0.20,
            "Flipkart",
            "Coordinates naturally with a simple necklace.",
        ),

        (
            "Bracelet",
            budget * 0.18,
            "Amazon",
            "Adds a subtle finishing detail.",
        ),

        (
            "Statement earrings alternative",
            budget * 0.28,
            "Flipkart",
            "Alternative if you prefer skipping a necklace.",
        ),
    ]

    return {

        "summary":
            f"Jewelry ideas for a "
            f"{data['occasion']} "
            f"with a "
            f"{data['style']} "
            f"preference.",

        "budget_allocation": [

            {
                "category":
                    "Primary jewelry",

                "amount":
                    round(budget * 0.45, 2),

                "percentage":
                    45,
            },

            {
                "category":
                    "Matching pieces",

                "amount":
                    round(budget * 0.30, 2),

                "percentage":
                    30,
            },

            {
                "category":
                    "Alternative piece",

                "amount":
                    round(budget * 0.15, 2),

                "percentage":
                    15,
            },

            {
                "category":
                    "Contingency",

                "amount":
                    round(budget * 0.10, 2),

                "percentage":
                    10,
            },
        ],

        "recommendations": [

            {
                "title": title,

                "estimated_price":
                    round(price, 2),

                "platform": platform,

                "description": description,

                "search_url":
                    search_url(platform, title),

                "reason":
                    "Selected as a style-compatible starting point within budget.",
            }

            for title, price, platform, description
            in items
        ],

        "savings_tips": [

            "Choose one focal piece and keep supporting pieces simpler.",

            "Check material, dimensions and seller reviews before buying.",

            "Use the outfit image as a color reference rather than assuming exact color matching.",
        ],
    } 