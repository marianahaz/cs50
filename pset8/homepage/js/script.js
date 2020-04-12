window.addEventListener('load', () => {



    function blink() {
        let blinkingPrompt = document.querySelector('span');
        blinkingPrompt.classList.toggle('hidden');
    }

    window.setInterval(blink, 400);



});
