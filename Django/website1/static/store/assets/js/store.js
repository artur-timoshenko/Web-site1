// Get Stripe publishable key
// fetch("/store/stripe/config/")
// .then((result) => { return result.json(); })
// .then((data) => {
//   // Initialize Stripe.js
//   const stripe = Stripe(data.publicKey);
//
//   // new
//   // Event handler
//   document.querySelector("#stripe_checkout").addEventListener("click", () => {
//     // Get Checkout Session ID
//     fetch("/store/stripe/session/")
//     .then((result) => { return result.json(); })
//     .then((data) => {
//       // console.log(data);
//       // Redirect to Stripe Checkout
//       return stripe.redirectToCheckout({sessionId: data.sessionId});
//     })
//     .then((res) => {
//       // console.log(res);
//     });
//   });
// });

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const header = document.getElementById('header');

const scrollUp = () =>{
    const scrollUp = document.getElementById('scroll-up');
    // When the scroll is higher than 350 viewport height, add the show-scroll class to the tag with the scrollup class
    this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
        : scrollUp.classList.remove('show-scroll');
};

window.addEventListener('scroll', scrollUp);

header.addEventListener('click', (event) => {
    // header.classList.toggle('show-menu');
});

document.querySelector('#show-menu').addEventListener('click', (event) => {
    event.preventDefault();
    header.classList.toggle('show-menu');
});
