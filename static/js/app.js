async function api(
    url,
    method = "GET",
    body = null,
    isForm = false
) {

    const options = {
        method: method,
        credentials: "include",
        headers: {}
    };


    if (body !== null) {

        if (isForm) {

            options.body = body;

        } else {

            options.headers[
                "Content-Type"
            ] = "application/json";

            options.body =
                JSON.stringify(body);
        }
    }


    const response =
        await fetch(
            url,
            options
        );


    let data = {};


    try {

        data =
            await response.json();

    } catch (error) {

        data = {};

    }


    return {

        ok:
            response.ok,

        status:
            response.status,

        data:
            data,
    };
}


async function logout() {

    await api(
        "/api/logout",
        "POST"
    );

    window.location.href = "/";
}


function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        function(character) {

            return {

                "&":
                    "&amp;",

                "<":
                    "&lt;",

                ">":
                    "&gt;",

                '"':
                    "&quot;",

                "'":
                    "&#039;",
            }[character];

        }
    );
}


function money(
    value,
    currency = "INR"
) {

    try {

        return new Intl.NumberFormat(
            "en-IN",
            {
                style: "currency",
                currency: currency
            }
        ).format(
            Number(value || 0)
        );

    } catch (error) {

        return (
            currency +
            " " +
            Number(
                value || 0
            ).toLocaleString(
                "en-IN"
            )
        );
    }
}


function renderResult(response) {

    const box =
        document.getElementById(
            "results"
        );


    if (!response.ok) {

        box.innerHTML = `
            <div class="error">

                ${escapeHtml(
                    response.data.detail
                    ||
                    "Could not generate recommendations."
                )}

            </div>
        `;

        return;
    }


    const result =
        response.data.result;


    box.innerHTML = `

        <section class="results">


            <div class="result-summary">

                <span class="eyebrow">

                    AI PLAN

                </span>


                <h2>

                    ${escapeHtml(
                        result.summary
                    )}

                </h2>

            </div>


            <div class="allocation-grid">

                ${
                    (
                        result
                            .budget_allocation
                        || []
                    )
                    .map(
                        function(item) {

                            return `

                                <div class="allocation">

                                    <b>
                                        ${escapeHtml(
                                            item.category
                                        )}
                                    </b>


                                    <strong>

                                        ${money(
                                            item.amount
                                        )}

                                    </strong>


                                    <span>

                                        ${escapeHtml(
                                            item.percentage
                                        )}%

                                    </span>

                                </div>

                            `;

                        }
                    )
                    .join("")
                }

            </div>


            <h3>
                Recommendations
            </h3>


            <div class="recommendation-grid">

                ${
                    (
                        result
                            .recommendations
                        || []
                    )
                    .map(
                        function(item) {

                            return `

                                <article class="card">

                                    <span class="platform">

                                        ${escapeHtml(
                                            item.platform
                                        )}

                                    </span>


                                    <h3>

                                        ${escapeHtml(
                                            item.title
                                        )}

                                    </h3>


                                    <strong>

                                        ${money(
                                            item.estimated_price
                                        )}

                                    </strong>


                                    <p>

                                        ${escapeHtml(
                                            item.description
                                        )}

                                    </p>


                                    <small>

                                        ${escapeHtml(
                                            item.reason
                                        )}

                                    </small>


                                    ${
                                        item.search_url
                                        ?
                                        `

                                        <a
                                            class="button secondary small"
                                            href="${escapeHtml(
                                                item.search_url
                                            )}"
                                            target="_blank"
                                            rel="noopener"
                                        >

                                            Search options ↗

                                        </a>

                                        `
                                        :
                                        ""
                                    }

                                </article>

                            `;

                        }
                    )
                    .join("")
                }

            </div>


            <div class="tips">

                <h3>
                    Savings tips
                </h3>


                <ul>

                    ${
                        (
                            result
                                .savings_tips
                            || []
                        )
                        .map(
                            function(tip) {

                                return `

                                    <li>

                                        ${escapeHtml(
                                            tip
                                        )}

                                    </li>

                                `;

                            }
                        )
                        .join("")
                    }

                </ul>

            </div>


            <p class="muted">

                Saved as history item #

                ${escapeHtml(
                    response.data.history_id
                )}

                .

            </p>


        </section>

    `;
}