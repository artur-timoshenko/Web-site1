const price_gt = document.getElementById("id_price__gte");
const price_lt = document.getElementById("id_price__lte");
const price_0 = document.getElementById("id_price_0");
const price_1 = document.getElementById("id_price_1");

price_gt.value = price_0.value;
price_lt.value = price_1.value;

price_gt.addEventListener('input', (event) => {
    price_0.value = event.target.value;
});

price_lt.addEventListener('input', (event) => {
    price_1.value = event.target.value;
});

price_0.addEventListener('input', (event) => {
    price_gt.value = event.target.value;
});

price_1.addEventListener('input', (event) => {
    price_lt.value = event.target.value;
});

document.querySelectorAll('#filter input').forEach(function(filter) {
    filter.addEventListener('focus', (event) => {
        event.target.value = '';
    });
});

document.querySelectorAll('.items button').forEach(function(filter) {
    filter.addEventListener('click', (event) => {
        event.stopPropagation();
        let productId = event.target.getAttribute('productId');
        fetch("/store/cart/add/", {
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
            htmx.trigger(event.target, "changed");
        }).catch((response) => {
            document.location.href = '/store/sign-in/';
        });
    });
});

document.querySelectorAll('.items ul li').forEach(function(filter) {
    filter.addEventListener('click', (event) => {
        let productId = event.target.getAttribute('productId');
        document.location.href = `/store/product/${productId}`;
    });
});

function addUrlParameter(name, value) {
    let searchParams = new URLSearchParams(window.location.search);
    searchParams.set(name, value);

    return Object.fromEntries(searchParams);
}

function changeUrlParameter(name, value) {
    let searchParams = new URLSearchParams(window.location.search);
    searchParams.set(name, value);

    window.location.search = searchParams.toString();
}
