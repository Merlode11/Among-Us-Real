let modalBtns = [...document.getElementsByClassName("ask")];
modalBtns.forEach(function (btn) {
    btn.onclick = function () {
        let modal = btn.getAttribute("data-modal");
        document.getElementById(modal).style.display = "block";
    };
    btn.onkeydown = function (e) {
        if (e.keyCode === 13) {
            let modal = btn.getAttribute("data-modal");
            document.getElementById(modal).style.display = "block";
        }
    };
});
let closeBtns = [...document.getElementsByClassName("close")];
console.log(closeBtns);
closeBtns.forEach(function (btn) {
    btn.onclick = function () {
        let modal = btn.closest(".modal");
        modal.style.display = "none";
    };
    btn.onkeydown = function (e) {
        if (e.keyCode === 13) {
            let modal = btn.closest(".modal");
            modal.style.display = "none";
        }
    };
});
window.onclick = function (event) {
    if (event.target.className === "modal") {
        event.target.style.display = "none";
    }
};
