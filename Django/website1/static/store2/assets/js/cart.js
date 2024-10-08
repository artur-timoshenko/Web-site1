scrollReveal.reveal('.cart', { delay: 0, duration: 500, scale: 0.75, opacity: 0 });
scrollReveal.reveal('.main > img', { duration: 500, scale: 0.9, opacity: 0 });
scrollReveal.reveal('.main > .procced', { duration: 500, opacity: 0 });

document.addEventListener('htmx:afterSwap', function () {
    initEventListeners();
    scrollReveal.sync();
});

initEventListeners();

function initEventListeners() {
    document.querySelectorAll('.remove-button').forEach(function (filter) {
        filter.addEventListener('click', (event) => {
            fetch("/store2/cart/remove/", {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                body: JSON.stringify({
                    productId: event.target.getAttribute('productId'),
                })
            })
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    htmx.trigger(event.target, "changed");
                    // location.reload();
                });
        });
    });

    document.querySelectorAll('.increase-button').forEach(function (filter) {
        filter.addEventListener('click', (event) => {
            fetch("/store2/cart/change/", {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                body: JSON.stringify({
                    productId: event.target.getAttribute('productId'),
                    value: 'increase',
                })
            })
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    htmx.trigger(event.target, "changed");
                    // if (data.status === 'success') {
                    //
                    // }
                    // console.log(data);
                    // location.reload();
                });
        });
    });

    document.querySelectorAll('.decrease-button').forEach(function (filter) {
        filter.addEventListener('click', (event) => {
            fetch("/store2/cart/change/", {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                body: JSON.stringify({
                    productId: event.target.getAttribute('productId'),
                    value: 'decrease',
                })
            })
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    htmx.trigger(event.target, "changed");
                    // location.reload();
                });
        });
    });

    document.querySelector("#procced")?.addEventListener("click", function () {
      document.querySelector('.checkout').style.display = 'grid';
      document.querySelector('.cart').style.display = 'none';
      document.querySelector('.procced').style.display = 'none';
      initStripe();
    }, {once: true});
};

function initStripe() {
  // This is your test publishable API key.
  fetch("/store2/stripe/config/")
      .then((result) => {
        return result.json();
      })
      .then((data) => {
        const stripe = Stripe(data.publicKey, {locale: 'en'});

        // The items the customer wants to buy
        // const items = [{ id: "xl-tshirt", amount: 1000 }, { id: "xl-tshirt", amount: 1500 }];

        let elements;

        document.querySelector("#email").addEventListener("click", function () {
          initialize().then(r => {
            document.querySelector('#submit').toggleAttribute('disabled');
          });
        }, {once: true});
        // initialize();

        document.querySelector("#payment-form").addEventListener("submit", handleSubmit);

        // Fetches a payment intent and captures the client secret
        async function initialize() {
          const response = await fetch("/store2/stripe/payment/", {
            method: "POST",
            headers: {'X-CSRFToken': csrftoken},
            // headers: { "Content-Type": "application/json" },
            // body: JSON.stringify({ items }),
          });

          const {clientSecret, dpmCheckerLink} = await response.json();

          const appearance = {
            theme: 'stripe',
            variables: {
              colorPrimary: '#000000',
              colorText: '#000000',
            },
          };

          elements = stripe.elements({appearance, clientSecret});

          const paymentElementOptions = {
            layout: "tabs",
          };

          const paymentElement = elements.create("payment", paymentElementOptions);
          paymentElement.mount("#payment-element");

          // [DEV] For demo purposes only
          // setDpmCheckerLink(dpmCheckerLink);
        }

        async function handleSubmit(e) {
          e.preventDefault();
          setLoading(true);

          const {error} = await stripe.confirmPayment({
            elements,
            confirmParams: {
              // Make sure to change this to your payment completion page
              return_url: "http://localhost:8000/store2/stripe/complete/",
              receipt_email: document.getElementById("email").value,
            },
          });

          // This point will only be reached if there is an immediate error when
          // confirming the payment. Otherwise, your customer will be redirected to
          // your `return_url`. For some payment methods like iDEAL, your customer will
          // be redirected to an intermediate site first to authorize the payment, then
          // redirected to the `return_url`.
          if (error.type === "card_error" || error.type === "validation_error") {
            showMessage(error.message);
          } else {
            showMessage("An unexpected error occurred.");
          }

          setLoading(false);
        }

        // ------- UI helpers -------

        function showMessage(messageText) {
          const messageContainer = document.querySelector("#payment-message");

          messageContainer.classList.remove("hidden");
          messageContainer.textContent = messageText;

          setTimeout(function () {
            messageContainer.classList.add("hidden");
            messageContainer.textContent = "";
          }, 4000);
        }

        // Show a spinner on payment submission
        function setLoading(isLoading) {
          if (isLoading) {
            // Disable the button and show a spinner
            document.querySelector("#submit").disabled = true;
            document.querySelector("#spinner").classList.remove("hidden");
            document.querySelector("#button-text").classList.add("hidden");
          } else {
            document.querySelector("#submit").disabled = false;
            document.querySelector("#spinner").classList.add("hidden");
            document.querySelector("#button-text").classList.remove("hidden");
          }
        }

        function setDpmCheckerLink(url) {
          document.querySelector("#dpm-integration-checker").href = url;
        }
      });
}
