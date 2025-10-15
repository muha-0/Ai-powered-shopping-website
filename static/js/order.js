document.addEventListener('DOMContentLoaded', () => {
    const productSelect = document.getElementById('product');
    const quantitySection = document.getElementById('quantity-section');
    const quantityInput = document.getElementById('quantity');
    const totalCostDisplay = document.getElementById('total-cost');
    const prefillButton = document.getElementById('prefill');
    const dateInput = document.getElementById('date');


    const now = new Date();
    //reference: https://www.w3schools.com/jsref/jsref_slice_string.asp
    const formattedDate = now.toISOString().slice(0, 19);
    console.log(formattedDate);
    dateInput.value = formattedDate;


    const prices = {
        apples: 2.5,
        eggs: 3.0,
        milk: 4.0
    };


    productSelect.addEventListener('change', () => {
        const product = productSelect.value;
        if (product) {
            quantitySection.style.display = 'block';
            updateTotalCost();
        } else {
            quantitySection.style.display = 'none';
            totalCostDisplay.textContent = '$0.00';
        }
    });


    quantityInput.addEventListener('input', updateTotalCost);

    function updateTotalCost() {
        const product = productSelect.value;
        const quantity = parseInt(quantityInput.value) || 0;
        if (product && prices[product]) {
            const total = prices[product] * quantity;
            totalCostDisplay.textContent = `$${total.toFixed(2)}`;
        }
    }


    prefillButton.addEventListener('click', () => {
        document.getElementById('buyer').value = "Sonic";
        document.getElementById('address').value = "123 Main St\nMinneapolis, MN 55401";
        productSelect.value = "milk";
        quantityInput.value = 2;
        document.getElementById('ground').checked = true;
        quantitySection.style.display = 'block';
        updateTotalCost();
    });
});
