let lastData = {};
let errors = 0;

const modalPopup = document.querySelector("#popup");
const modalPopupTitle = document.getElementById("popup-title");
const modalPopupContent = document.getElementById("popup-content");

let interval = window.setInterval( function() {
    fetch("/api/infos")
        .then(response => response.json())
        .then(data => {
            errors = 0
            if (data.game_pause) {
                window.location.href = "/paused";
            }
            else if (data.meeting) {
                window.location.href = "/meeting";
            }
            else if (data.end) {
                window.location.href = "/end"
            }
            else if (data.popup && data.popup !== lastData.popup && data.popup.message) {
                modalPopup.style.display = "block";
                modalPopupTitle.innerHTML = data.popup.title;
                modalPopupContent.innerHTML = data.popup.message;
            }
            else if (lastData.dead !== data.dead) {
                if (data.dead) {
                    document.body.classList.add("dead");
                } else {
                    document.body.classList.remove("dead");
                }
            }
        }).catch(error => {
            console.log(error);
            errors++;
            if (errors >= 10) {
                window.clearInterval(interval);
            }
        })
}, 300);
