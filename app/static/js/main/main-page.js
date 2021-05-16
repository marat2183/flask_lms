let slidePosition = 0;
const slides = document.getElementsByClassName('carousel__item');
const buttons = document.getElementsByClassName('carousel__button');
const totalSlides = slides.length;


function moveToFirstSlide() {
    for (let slide of slides) {
        slide.classList.remove('carousel__item--visible');
        slide.classList.add('carousel__item--hidden');
    }
    slides[0].classList.add('carousel__item--visible');

    for (let button of buttons) {
        button.classList.remove('carousel__button--active');
    }
    buttons[0].classList.add('carousel__button--active');
}

function moveToSecondSlide() {
    for (let slide of slides) {
        slide.classList.remove('carousel__item--visible');
        slide.classList.add('carousel__item--hidden');
    }
    slides[1].classList.add('carousel__item--visible');

    for (let button of buttons) {
        button.classList.remove('carousel__button--active');
    }
    buttons[1].classList.add('carousel__button--active');
}

function moveToThirdSlide() {
    for (let slide of slides) {
        slide.classList.remove('carousel__item--visible');
        slide.classList.add('carousel__item--hidden');
    }
    slides[2].classList.add('carousel__item--visible');

    for (let button of buttons) {
        button.classList.remove('carousel__button--active');
    }
    buttons[2].classList.add('carousel__button--active');
}


document.getElementById('carousel__button--fisrt').addEventListener("click", function() {
    moveToFirstSlide();
})

document.getElementById('carousel__button--second').addEventListener("click", function() {
    moveToSecondSlide();
})

document.getElementById('carousel__button--third').addEventListener("click", function() {
    moveToThirdSlide();
})