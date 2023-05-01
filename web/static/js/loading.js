window.setInterval(function () {
    const wait = document.getElementById("dots");
    if (wait.innerHTML.length > 2)
        wait.innerHTML = "";
    else
        wait.innerHTML += ".";

    const is_started = fetch("/api/game_is_started")
        .then(response => response.json())
        .then(data => {
            if (data.started) {
                window.location.href = "/player";
            }
        })
}, 300);