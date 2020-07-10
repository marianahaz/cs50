window.addEventListener('load', start);

let toggleMenu = document.querySelector("#toggle");
let overlay = document.querySelector('#overlay');

function start() {

    toggleMenu.addEventListener("click", () => {
        toggleMenu.classList.toggle('active');
        overlay.classList.toggle('overlay');
        document.querySelector('body').classList.toggle('noscroll');
    });

}
