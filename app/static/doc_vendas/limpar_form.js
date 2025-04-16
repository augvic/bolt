// ================================================== \\

// ~~ Elementos.
const form = document.getElementById("add_doc");
const clear_button = document.getElementById("clear_form");

// ~~ Event listener.
clear_button.addEventListener("click", () => {
    form.reset()
});

// ================================================== \\