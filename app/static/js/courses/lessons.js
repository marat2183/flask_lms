let burger = document.querySelector(".header_burger");
let menu = document.querySelector(".header_menu");
let body = document.querySelector("body")
burger.addEventListener('click', () => {
    menu.classList.toggle("active");
    burger.classList.toggle("active");
    body.classList.toggle("lock");
})