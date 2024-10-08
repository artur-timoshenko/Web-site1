const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const header = document.getElementById('header');
let lastKnownScrollPosition = 0;

const inViewport = (entries, obServer) => {
    entries.forEach(entry => {
        // // ⚠️ Feature detection
        // if (typeof entry.isVisible === 'undefined') {
        //   // The browser doesn't support Intersection Observer v2, falling back to v1 behavior.
        //     entry.isVisible = true;
        // }
        //
        // console.log(entry.target, entry.isIntersecting, entry.isVisible);
        //
        // if (entry.isIntersecting && entry.isVisible) {
        //   // visibleSince = change.time;
        //     entry.target.classList.toggle("is-inViewport", true);
        // } else {
        //   // visibleSince = 0;
        //     entry.target.classList.toggle("is-inViewport", false);
        // }

        entry.target.classList.toggle("is-inViewport", entry.isIntersecting);
    });
};

const obsOptions = {
    // root: document.querySelector(".main"),
    threshold: [0.01],
    // trackVisibility: true,
    // delay: 100,
}; //See: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API#Intersection_observer_options

const Obs = new IntersectionObserver(inViewport, obsOptions);

// Attach observer to every [data-inviewport] element:
document.querySelectorAll('[data-inviewport]').forEach(el => {
    Obs.observe(el, obsOptions);
});

document.querySelector('#showMenu').addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();

    // if (box.classList.contains('hidden')) {
    //     box.classList.remove('hidden');
    //
    //     setTimeout(function () {
    //         box.classList.remove('visuallyhidden');
    //     }, 20);
    // } else {
    //     box.classList.add('visuallyhidden');
    //
    //     box.addEventListener('transitionend', function(e) {
    //         box.classList.add('hidden');
    //     }, { capture: false, once: true, passive: false});
    // }

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

    // if (ScrollPosition === 0) {
    //     header.classList.remove('showHeader');
    //     header.classList.remove('show-menu');
    //
    //     return;
    // }

    if (ScrollPosition > lastKnownScrollPosition) {
        // downscroll code
        if ((ScrollPosition - lastKnownScrollPosition) > scrollValue) {
            header.classList.remove('showHeader');
            header.classList.remove('show-menu');
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

            fetch("/store4/cart/change/", {
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
            fetch("/store4/cart/remove/", {
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
        fetch("/store4/stripe/checkout/", {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
        }).then((result) => {
            return result.json();
        }).then((data) => {
            location.href = data.checkoutSessionURL;
        });
    });
}

document.querySelectorAll('.productsSection .products .product').forEach(function(element) {
    element.addEventListener('click', (event) => {
        // event.preventDefault();
        let productId = event.target.getAttribute('productId');
        fetch("/store4/cart/add/", {
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
            document.location.href = '/store4/sign-in/';
        });
    });
});

document.querySelector('#subscribe')?.addEventListener('submit', (event) => {
    event.preventDefault();
    event.target.elements.email.value = '';
});

const scrollUp = () =>{
    const scrollUp = document.getElementById('scroll-up');
    // When the scroll is higher than 350 viewport height, add the show-scroll class to the tag with the scrollup class
    this.scrollY >= 350 ? scrollUp.classList.add('show-scroll') : scrollUp.classList.remove('show-scroll');
};

window.addEventListener('scroll', scrollUp);

// init controller
let controller = new ScrollMagic.Controller();

new ScrollMagic.Scene({triggerElement: '.sign-form', triggerHook: "onEnter"})
    .setTween('.sign-form form', .25, {opacity: 1, ease: Linear.easeNone})
    .addTo(controller);

document.querySelectorAll(".pin").forEach(function (self) {
    new ScrollMagic.Scene({triggerElement: self, triggerHook: 0, duration: "100%", reverse: true})
        .setPin(self, {pushFollowers: self.hasAttribute('pushFollowers')})
        .addTo(controller);

    var timeline = new TimelineMax();
    var tween1 = TweenMax.from(self, 1, {opacity: 0, rotation: -10, x: "-100%", ease: Linear.easeNone});
    var tween2 = TweenMax.to(self, 1, {opacity: 1, rotation: 0, x: 0, ease: Linear.easeNone});
    var tween3 = TweenMax.to(self, 1, {opacity: 0, rotation: 10, x: 100,  ease: Linear.easeNone});
    timeline
        .add(tween1)
        .add(tween2)
        .add(tween3);

    new ScrollMagic.Scene({triggerElement: self, triggerHook: 0, duration: "150%", reverse: true})
        // .setTween(self, 1, {opacity: 1, ease: Linear.easeNone})
        .setTween(timeline)
        .addTo(controller);
});

new ScrollMagic.Scene({triggerElement: '.cover', triggerHook: "onEnter", duration: "200%", tweenChanges: true, reverse: true})
    .setTween('.cover img', 10, {scale: 1, ease: Linear.easeNone})
    .addTo(controller);

new ScrollMagic.Scene({triggerElement: '.cover', triggerHook: "onEnter", duration: "50%", tweenChanges: true})
    .setTween('.cover img', 1, {opacity: 1, ease: Linear.easeNone})
    .addTo(controller);

new ScrollMagic.Scene({triggerElement: '.cover', triggerHook: "onLeave", duration: "100%", tweenChanges: true, reverse: true})
    .setTween('.sectionImage', 1, {opacity: 1, ease: Linear.easeNone})
    .addTo(controller);

new ScrollMagic.Scene({triggerElement: '.main > .title', triggerHook: "onEnter", duration: "50%", tweenChanges: true, reverse: true})
    .setTween('.main > .title', 1, {opacity: 1, ease: Linear.easeNone})
    .addTo(controller);
