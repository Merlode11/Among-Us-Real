window.setInterval( function() {
    const is_started = fetch("/api/infos")
        .then(response => response.json())
        .then(data => { 
            console.log(data)
            if (!data.meeting) {
                window.location.href = "/joueur";
            }
        })
}, 300);