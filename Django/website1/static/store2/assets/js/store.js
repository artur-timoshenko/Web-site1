const scrollReveal = ScrollReveal();

scrollReveal.reveal('.mySwiper', { duration: 500, scale: 1.1, opacity: 0 });
scrollReveal.reveal('.sign-form form', { duration: 500, scale: 0.75, opacity: 0 });
scrollReveal.reveal('.sign-form img', { duration: 500, scale: 0.9, opacity: 0 });

const progressCircles = document.querySelectorAll(".autoplay-progress svg");
const progressContents = document.querySelectorAll(".autoplay-progress span");

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const header = document.getElementById('header');

document.querySelector('#show-menu').addEventListener('click', (event) => {
  event.preventDefault();
  event.stopPropagation();
  header.classList.toggle('show-menu');
});

header.addEventListener('click', (event) => {
  event.stopPropagation();
});

document.addEventListener('click', (event) => {
  header.classList.remove('show-menu');
});

const swiper = new Swiper(".mySwiper", {
  spaceBetween: 30,
  centeredSlides: true,
  autoplay: {
    // delay: 5000,
    disableOnInteraction: false,
  },
  grabCursor: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
    dynamicBullets: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  loop: true,
  effect: 'coverflow',
  coverflowEffect: {
    rotate: 30,
    slideShadows: true,
  },
  slideShadows: true,
  // on: {
  //   autoplayTimeLeft(s, time, progress) {
  //     progressCircles.forEach(function(progressCircle) {
  //       progressCircle.style.setProperty("--progress", 1 - progress);
  //     });
  //     progressContents.forEach(function(progressContent) {
  //       progressContent.textContent = `${Math.ceil(time / 1000)}s`;
  //     });
  //     // progressCircle.style.setProperty("--progress", 1 - progress);
  //     // progressContent.textContent = `${Math.ceil(time / 1000)}s`;
  //   }
  // }
});
