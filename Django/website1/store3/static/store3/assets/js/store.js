const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const header = document.getElementById('header');
let lastKnownScrollPosition = 0;

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

document.querySelector('#cartMenu').addEventListener('click', (event) => {
    document.querySelector('#cart').showModal();
    document.body.classList.add("modal-open");
});

document.querySelector('#cart').addEventListener('click', (event) => {
  if (event.target === event.currentTarget) {
    event.target.close();
  }
});

document.querySelector('#cart').addEventListener('close', (event) => {
    document.body.classList.remove("modal-open");
});

document.addEventListener("scroll", (event) => {
  let ScrollPosition = window.scrollY || document.documentElement.scrollTop;
  let scrollValue = 100;

  if (ScrollPosition > lastKnownScrollPosition) {
    // downscroll code
    if ((ScrollPosition - lastKnownScrollPosition) > scrollValue) {
      header.classList.remove('showHeader');
      lastKnownScrollPosition = ScrollPosition <= 0 ? 0 : ScrollPosition;
    }
   } else if (ScrollPosition < lastKnownScrollPosition) {
    // upscroll code
    if ((ScrollPosition - lastKnownScrollPosition) < -scrollValue) {
      header.classList.add('showHeader');
      lastKnownScrollPosition = ScrollPosition <= 0 ? 0 : ScrollPosition;
    }
   } // else was horizontal scroll
});

document.addEventListener('htmx:afterSwap', function () {
    initEventListeners();
});

initEventListeners();

function initEventListeners() {
    document.querySelectorAll(".cart .products .product .details .quantity input").forEach(function (element) {
        element.addEventListener("change", function (event) {
            // console.log( +event.target.value > +event.target.dataset.lastValue ? 'increased' : 'decreased');
            //
            // element.dataset.lastValue = element.value;
            // return

            event.target.disabled = true;

            fetch("/store3/cart/change/", {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                body: JSON.stringify({
                    productId: event.target.getAttribute('productId'),
                    value: event.target.value,
                })
            }).then((result) => {
                return result.json();
            }).then((data) => {
                htmx.trigger(event.target, "changed");
            });
        });

        // element.dataset.lastValue = element.value;
    });

    document.querySelectorAll('.remove-button').forEach(function (element) {
        element.addEventListener('click', (event) => {
            fetch("/store3/cart/remove/", {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                body: JSON.stringify({
                    productId: event.target.getAttribute('productId'),
                })
            }).then((result) => {
                return result.json();
            }).then((data) => {
                htmx.trigger(event.target, "changed");
                // location.reload();
            });
        });
    });

    document.querySelector('#checkout')?.addEventListener('click', (event) => {
        fetch("/store3/stripe/checkout/", {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
        }).then((result) => {
            return result.json();
        }).then((data) => {
            location.href = data.checkoutSessionURL;
        });
    });
}

document.querySelectorAll('.parallaxSection .products .product img').forEach(function(element) {
    element.addEventListener('click', (event) => {
        // event.preventDefault();
        let productId = event.target.getAttribute('productId');
        fetch("/store3/cart/add/", {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                productId: productId,
                productQuantity: 1,
            })
        })
        .then((result) => { return result.json(); })
        .then((data) => {
            htmx.trigger(event.target, "changed");
            document.querySelector('#cart').showModal();
            document.body.classList.add("modal-open");
        }).catch((response) => {
            document.location.href = '/store3/sign-in/';
        });
    });
});

const scrollUp = () =>{
    const scrollUp = document.getElementById('scroll-up');
    // When the scroll is higher than 350 viewport height, add the show-scroll class to the tag with the scrollup class
    this.scrollY >= 350 ? scrollUp.classList.add('show-scroll') : scrollUp.classList.remove('show-scroll');
};

window.addEventListener('scroll', scrollUp);

// init controller
let controller = new ScrollMagic.Controller();

// build scenes
new ScrollMagic.Scene({triggerElement: "#parallax1", triggerHook: "onEnter", duration: "200%"})
    .setTween("#parallax1 > div", {y: "80%", ease: Linear.easeNone})
    // .addIndicators()
    .addTo(controller);

new ScrollMagic.Scene({triggerElement: "#parallax2", triggerHook: "onEnter", duration: "200%"})
    .setTween("#parallax2 > div", {y: "80%", ease: Linear.easeNone})
    // .addIndicators()
    .addTo(controller);

new ScrollMagic.Scene({triggerElement: "#parallax3", triggerHook: "onEnter", duration: "200%"})
    .setTween("#parallax3 > div", {y: "80%", ease: Linear.easeNone})
    // .addIndicators()
    .addTo(controller);

new ScrollMagic.Scene({triggerElement: '.company', triggerHook: "onCenter"})
    .setTween('.company img', 1, {opacity: 1, ease: Linear.easeNone})
    .addTo(controller);

new ScrollMagic.Scene({triggerElement: '.company', triggerHook: "onEnter", duration: "200%", tweenChanges: true, reverse: true})
    .setTween('.company img', 10, {scale: 1, ease: Linear.easeNone})
    .addTo(controller);

// let timeline = TimelineMax();
// let tween = TweenMax.to('.container .title', 1, {x: "5%", y: "5%", opacity: 1, delay: 1});
// timeline.add(tween);

// var timeline = new TimelineMax();
// var tween1 = TweenMax.from("obj1", 1, {x: 100});
// var tween2 = TweenMax.to("obj2", 1, {y: 100});
// timeline
//     .add(tween1)
//     .add(tween2);

new ScrollMagic.Scene({triggerElement: '.company', triggerHook: "onCenter", duration: '75%', tweenChanges: true, reverse: true})
    .setTween('.company .bigTitle', 1, {x: "5%", y: "75%", opacity: 1, delay: 1, ease: Linear.easeNone})
    .addTo(controller);

document.querySelectorAll(".main > .parallaxSection").forEach(function (self) {
    new ScrollMagic.Scene({triggerElement: self ,triggerHook: "onEnter", duration: '50%', tweenChanges: true, reverse: false})
        .setTween(self.children[0], 1, {x: "5%", y: "25%", opacity: 1, delay: 0, ease: Linear.easeNone})
        .addTo(controller);
});

new ScrollMagic.Scene({triggerElement: '.sign-form', triggerHook: "onEnter"})
    .setTween('.sign-form form', .25, {opacity: 1, ease: Linear.easeNone})
    .addTo(controller);

var swiperParameters = {
    // wrapperClass: 'swiper-wrapper',
    // slideClass: 'swiper-slide',
    // touchEventsTarget: 'swiper-wrapper',
    spaceBetween: 40,
    grabCursor: true,
    freeMode: true,
    // freeModeMomentum: false,
    // freeModeMomentumBounce: false,
    // direction: 'horizontal',
    speed: 11000,
    loop: true,
    slidesPerView: "auto",
    autoplay: {
        delay: 1,
        disableOnInteraction: false,
        // reverseDirection: true,
        // waitForTransition: false,
    },
    breakpoints: {
        0: { /* when window >=0px - webflow mobile landscape/portriat */
            spaceBetween: 30,
        },
        480: { /* when window >=0px - webflow mobile landscape/portriat */
            spaceBetween: 30,
        },
        767: { /* when window >= 767px - webflow tablet */
            spaceBetween: 40,
        },
        992: { /* when window >= 988px - webflow desktop */
            spaceBetween: 40,
        }
    },
};

var swiper = new Swiper('#normalSwiper', swiperParameters);

swiperParameters.autoplay = {
    delay: 1,
    disableOnInteraction: false,
    reverseDirection: true,
};

var reverseSwiper = new Swiper('#reverseSwiper', swiperParameters);

// This is your test publishable API key.
// fetch("/store3/stripe/config/")
// .then((result) => { return result.json(); })
// .then((data) => {
//     const stripe = Stripe(data.publicKey, {locale: 'en'});
//
//     document
//     .querySelector("#checkout-button")
//     .addEventListener("click", function (event) {
//         event.preventDefault();
//         initialize().then(r => {
//         // document.querySelector('#submit').toggleAttribute('disabled');
//         });
//     }, {once: false});
//
//     // Create a Checkout Session
//     async function initialize() {
//         const fetchClientSecret = async () => {
//             const response = await fetch("/store3/stripe/checkout/", {
//                 method: "POST",
//                 headers: {'X-CSRFToken': csrftoken},
//             });
//             const {clientSecret} = await response.json();
//             return clientSecret;
//         };
//
//         const elements = stripe.elements();
//         elements.update({locale: 'fr'});
//
//         const onComplete = async () => {
//           checkout.destroy();
//         };
//
//         const checkout = await stripe.initEmbeddedCheckout({
//             fetchClientSecret, onComplete
//         });
//
//         // Mount Checkout
//         checkout.mount('#checkout');
//     }
// });
