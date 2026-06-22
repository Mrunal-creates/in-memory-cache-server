const API_KEY = "mysecretkey123";

let hitsMissesChart = null;

async function loadHealth() {

    try {

        const response = await fetch(
            "/health",
            {
                headers: {
                    "x-api-key": API_KEY
                }
            }
        );

        const data = await response.json();

        const status =
            document.getElementById(
                "status"
            );

        status.innerHTML =
        `
        <span class="status-online">
            🟢 ${data.status}
        </span>

        | Database: ${data.database}
        `;

    }

    catch {

        document.getElementById(
            "status"
        ).innerHTML =
        `
        <span class="status-offline">
            🔴 Server Offline
        </span>
        `;
    }
}


async function loadMetrics() {

    try {

        const response = await fetch(
            "/metrics",
            {
                headers: {
                    "x-api-key": API_KEY
                }
            }
        );

        const data = await response.json();

        document.getElementById(
            "hits"
        ).innerText =
            data.hits;

        document.getElementById(
            "misses"
        ).innerText =
            data.misses;

        document.getElementById(
            "hit_ratio"
        ).innerText =
            data.hit_ratio + "%";

        document.getElementById(
            "current_size"
        ).innerText =
            data.current_size;

        document.getElementById(
            "capacity"
        ).innerText =
            data.capacity;

        document.getElementById(
            "uptime"
        ).innerText =
            data.uptime;

        updateChart(
            data.hits,
            data.misses
);

    }

    catch (error) {

        console.error(
            "Metrics Error:",
            error
        );
    }
}


async function setValue() {

    try {

        const key =
            document.getElementById(
                "set_key"
            ).value;

        const value =
            document.getElementById(
                "set_value"
            ).value;

        const ttl =
            document.getElementById(
                "set_ttl"
            ).value;

        const response =
            await fetch(
                "/set",
                {
                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "x-api-key":
                            API_KEY
                    },

                    body: JSON.stringify({

                        key: key,

                        value: value,

                        ttl: ttl
                            ? parseInt(ttl)
                            : null
                    })
                }
            );

        const data =
            await response.json();

        alert(
            "SET Operation: " +
            data.status
        );

        loadMetrics();

    }

    catch (error) {

        console.error(
            "SET Error:",
            error
        );
    }
}


async function getValue() {

    try {

        const key =
            document.getElementById(
                "get_key"
            ).value;

        const response =
            await fetch(
                `/get/${key}`,
                {
                    headers: {
                        "x-api-key":
                            API_KEY
                    }
                }
            );

        const data =
            await response.json();

        document.getElementById(
            "get_result"
        ).innerText =
            `Value: ${data.value}`;

        loadMetrics();

    }

    catch (error) {

        console.error(
            "GET Error:",
            error
        );
    }
}


async function deleteValue() {

    try {

        const key =
            document.getElementById(
                "delete_key"
            ).value;

        const response =
            await fetch(
                `/delete/${key}`,
                {
                    method: "DELETE",

                    headers: {
                        "x-api-key":
                            API_KEY
                    }
                }
            );

        const data =
            await response.json();

        document.getElementById(
            "delete_result"
        ).innerText =
            data.status;

        loadMetrics();

    }

    catch (error) {

        console.error(
            "DELETE Error:",
            error
        );
    }
}


loadHealth();

loadMetrics();


setInterval(
    () => {

        loadHealth();

        loadMetrics();

    },
    3000
);

function updateChart(
    hits,
    misses
) {

    const ctx =
        document
        .getElementById(
            "hitsMissesChart"
        )
        .getContext("2d");

    if (
        hitsMissesChart
    ) {

        hitsMissesChart.destroy();
    }

    hitsMissesChart =
        new Chart(
            ctx,
            {

                type: "bar",

                data: {

                    labels: [
                        "Hits",
                        "Misses"
                    ],

                    datasets: [

                        {

                            label:
                                "Cache Activity",

                            data: [
                                hits,
                                misses
                            ]
                        }
                    ]
                },

                options: {

                    responsive: true,

                    maintainAspectRatio:
                        false
                }
            }
        );
}