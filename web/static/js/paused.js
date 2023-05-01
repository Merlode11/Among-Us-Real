window.setInterval( function() {
    fetch("/api/infos")
        .then(response => response.json())
        .then(data => {
            if (!data.game_pause) {
                window.location.href = "/joueur";
            }
        })
}, 300);