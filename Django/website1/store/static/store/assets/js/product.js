document.querySelectorAll('.product button').forEach(function(filter) {
    filter.addEventListener('click', (event) => {
        event.stopPropagation();
        let productId = event.target.getAttribute('productId');
        let proudctQuantity = document.getElementById('select').value;

        fetch("/store/cart/add/", {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                productId: productId,
                productQuantity: proudctQuantity,
            })
        })
        .then((result) => { return result.json(); })
        .then((data) => {
            // window.location = `/store/catalog/#item${productId}`;
            // location.reload();
            htmx.trigger(event.target, "changed");
        }).catch((response) => {
            location.replace('/store/sign-in/');
        });
    });
});