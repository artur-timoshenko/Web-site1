const scrollReveal = ScrollReveal();

scrollReveal.reveal('.main > img', { duration: 500, scale: 0.9, opacity: 0 });
scrollReveal.reveal('.swiper', { delay: 0, duration: 500, opacity: 0, scale: 0.75 });

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
    // autoplay: {
    //   // delay: 5000,
    //   disableOnInteraction: true,
    // },
    grabCursor: true,
    pagination: {
    el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true,
    },
    centeredSlides: true,
    slidesPerView: 1,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    loop: true,
    effect: 'coverflow',
    coverflowEffect: {
        rotate: 50,
        stretch: 0,
        depth: 100,
        modifier: 1,
        slideShadows: false,
    },
    breakpoints: {
        1024: {
            slidesPerView: 3,
        }
    }
});

document.querySelectorAll('.product button').forEach(function(filter) {
    filter.addEventListener('click', (event) => {
        event.stopPropagation();
        let productId = event.target.getAttribute('productId');
        fetch("/store2/cart/add/", {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                productId: productId,
                productQuantity: 1,
            })
        })
        .then((result) => { return result.json(); })
        .then((data) => {
            // window.location = `/store/catalog/#item${productId}`;
            // location.reload();
        }).catch((response) => {
            document.location.href = '/store2/sign-in/';
        });
    });
});
