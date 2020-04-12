window.addEventListener('load', () => {

    preventSubmit();


    var inputName = null;
    var name = null;

    const submitHello = document.querySelector("#submit");
    submitHello.addEventListener('click', () => {

        inputName = document.querySelector("#name");
        name = inputName.value;
        const result = document.querySelector('#result');

        result.textContent = "The mountains are beautiful, "+name+", be more like the mountains";

        clearInput();

    })



    function preventSubmit() {

        function handleSubmit(event) {
            event.preventDefault();
        }

        let form = document.querySelector("form");
        form.addEventListener('submit', handleSubmit);

    }


    function clearInput() {
        inputName.value = '';
        inputName.focus();
    }

});
