window.addEventListener('load', () => {

    const body = document.querySelector('body');
    var bg = null;


    function updateColor() {

        let color = this.id;
        let bg = null;

        switch (color) {
            case 'gray':
                bg = '#303030';
                break;
            case 'navy':
                bg = '#0a0a54';
                break;
            case 'blood':
                bg = '#701208';
                break;
        }

        body.style.backgroundColor = bg;


        backToBlack(3000);



    }

    var bgColor = document.querySelectorAll('button');

    bgColor.forEach(item => {
        item.addEventListener('click', updateColor);
    });

    function backToBlack(time) {
        setTimeout( () => {
            body.style.backgroundColor = '#000';
        }, time);
    }

});
