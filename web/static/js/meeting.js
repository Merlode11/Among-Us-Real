let lastData = {};
let errors = 0;

const seePassword = document.getElementById("see-password");

const radios = document.querySelectorAll('input[type=radio][name="vote"]');
const voteButton = document.querySelector("#submit-button");

const modalPopup = document.querySelector("#popup");
const modalPopupTitle = document.getElementById("popup-title");
const modalPopupContent = document.getElementById("popup-content");

let interval = window.setInterval( function() {
    fetch("/api/infos")
        .then(response => response.json())
        .then(data => {
            if (!data.meeting) {
                window.location.href = "/player";
            }
            else if (data.end) {
                window.location.href = "/end"
            }
            else if (data.meeting && data.meeting !== lastData.meeting) {
                if (data.meeting === "vote" && !data.has_vote && !data.dead) {
                    radios.forEach(radio => {
                        if (radio.getAttribute("data-player-dead") !== "True") {
                            radio.checked = false;
                            radio.disabled = false;
                        } else {
                            radio.checked = false;
                            radio.disabled = true;
                        }
                    });
                    voteButton.disabled = false;
                } else if (data.meeting === "discussion") {
                    seePassword.style.display = "none";
                } else {
                    radios.forEach(radio => {
                        radio.checked = false;
                        radio.disabled = true;
                    });
                    voteButton.disabled = true;
                }
            }
            else if (data.popup && data.popup !== lastData.popup && data.popup.message) {
                modalPopup.style.display = "block";
                modalPopupTitle.innerHTML = data.popup.title;
                modalPopupContent.innerHTML = data.popup.message;
            }

            lastData = data;
        }).catch(error => {
            console.log(error);
            errors++;
            if (errors >= 10) {
                window.clearInterval(interval);
            }
        })
}, 300);