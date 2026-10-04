def register_and_login(client):

    response = client.post(
        "/api/register",
        json={
            "email":
                "test@example.com",

            "password":
                "password123",

            "full_name":
                "Test User",
        },
    )

    assert response.status_code in (
        200,
        409,
    )

    return client


def test_health(client):

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_register_login_and_session(
    client
):

    register_and_login(client)

    response = client.get(
        "/api/session-info"
    )

    assert response.status_code == 200

    assert (
        response.json()["authenticated"]
        is True
    )


def test_home_planner(client):

    register_and_login(client)

    payload = {

        "budget":
            50000,

        "currency":
            "INR",

        "rooms": [

            {

                "room_type":
                    "Living Room",

                "quantity":
                    1,

                "style":
                    "Modern",
            }

        ],

        "requirements": [

            "lights",

            "storage",
        ],

        "location":
            "Coimbatore",
    }


    response = client.post(
        "/api/generate-home",
        json=payload,
    )


    assert response.status_code == 200


    body =
        response.json()


    assert (
        body["planner_type"]
        == "home"
    )


    assert (
        body["history_id"]
        > 0
    )


    assert len(
        body[
            "result"
        ][
            "recommendations"
        ]
    ) > 0


def test_party_planner(client):

    register_and_login(client)


    payload = {

        "budget":
            30000,

        "currency":
            "INR",

        "guest_count":
            30,

        "event_type":
            "Birthday",

        "venue":
            "Hall",

        "location":
            "Coimbatore",

        "preferences": [

            "vegetarian"
        ],
    }


    response = client.post(
        "/api/generate-party",
        json=payload,
    )


    assert response.status_code == 200


    assert (
        response.json()["planner_type"]
        == "party"
    )


def test_history(client):

    register_and_login(client)


    response = client.get(
        "/api/history"
    )


    assert response.status_code == 200


    assert isinstance(
        response.json()["history"],
        list,
    )


def test_protected_route_rejects_anonymous(
    client
):

    client.post(
        "/api/logout"
    )


    response = client.get(
        "/api/history"
    )


    assert response.status_code == 401