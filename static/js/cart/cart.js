document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const currencySymbol = document.querySelector('[data-currency-symbol]')?.dataset.currencySymbol || '';
    
    // Quantity buttons
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const action = this.dataset.action;
            const input = document.querySelector(`#qty-${itemId}`);
            let quantity = parseInt(input.value);
            
            if (action === 'increase') {
                quantity++;
            } else if (action === 'decrease' && quantity > 1) {
                quantity--;
            }
            
            input.value = quantity;
            updateCartItem(itemId, quantity);
        });
    });
    
    // Remove cart items
    document.querySelectorAll('[data-action="remove-cart"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            confirmRemove(itemId);
        });
    });
    
    // Save for later
    document.querySelectorAll('[data-action="save-for-later"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            saveForLater(itemId);
        });
    });
    
    // Remove saved items
    document.querySelectorAll('[data-action="remove-saved"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            confirmRemoveSaved(itemId);
        });
    });
    
    // Move to cart
    document.querySelectorAll('.move-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            moveToCart(itemId);
        });
    });
    
    function updateCartItem(itemId, quantity) {
        fetch(`/cart/update/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `quantity=${quantity}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.querySelector(`#item-subtotal-${itemId}`).textContent = `${currencySymbol}${data.subtotal.toFixed(2)}`;
                document.querySelector('#subtotal-amount').textContent = `${currencySymbol}${data.cart_total.toFixed(2)}`;
                document.querySelector('#total-amount').textContent = `${currencySymbol}${data.total.toFixed(2)}`;
                updateCartCount(data.cart_count);
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    window.confirmRemove = function(itemId) {
        showModal(
            'confirmModal',
            'Remove Item',
            'Remove this item from cart?',
            function() {
                removeCartItem(itemId);
            }
        );
    };
    
    function removeCartItem(itemId) {
        fetch(`/cart/remove/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const itemElement = document.querySelector(`#cart-item-${itemId}`);
                itemElement.remove();
                
                document.querySelector('#subtotal-amount').textContent = `${currencySymbol}${data.cart_total.toFixed(2)}`;
                document.querySelector('#total-amount').textContent = `${currencySymbol}${data.total.toFixed(2)}`;
                
                updateCartCount(data.cart_count);
                
                if (data.cart_count === 0) {
                    location.reload();
                }
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    window.saveForLater = function(itemId) {
        showModal(
            'confirmModal',
            'Save for Later',
            'Save this item for later? It will be removed from your active cart.',
            function() {
                moveToSavedForLater(itemId);
            }
        );
    };
    
    function moveToSavedForLater(itemId) {
        fetch(`/cart/save-for-later/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    window.moveToCart = function(itemId) {
        fetch(`/cart/move-to-cart/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
        return false;
    };
    
    window.confirmRemoveSaved = function(itemId) {
        showModal(
            'confirmModal',
            'Remove Saved Item',
            'Remove this item from saved for later?',
            function() {
                removeSavedItem(itemId);
            }
        );
        return false;
    };
    
    function removeSavedItem(itemId) {
        fetch(`/cart/remove-saved/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const itemElement = document.querySelector(`#saved-item-${itemId}`);
                itemElement.remove();
                
                updateCartCount(data.cart_count);
                
                if (data.saved_count === 0) {
                    location.reload();
                }
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    function updateCartCount(count) {
        let cartBadge = document.querySelector('.cart-count');
        const cartDropdown = document.querySelector('#cartDropdown');
        
        if (!cartBadge && cartDropdown && count > 0) {
            // Create badge if it doesn't exist
            cartBadge = document.createElement('span');
            cartBadge.className = 'position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger cart-count';
            cartDropdown.appendChild(cartBadge);
        }
        
        if (cartBadge) {
            cartBadge.textContent = count;
            if (count === 0) {
                cartBadge.classList.add('d-none');
            } else {
                cartBadge.classList.remove('d-none');
            }
        }
        
        // Reload cart dropdown preview if function exists
        if (typeof loadCartPreview === 'function') {
            loadCartPreview();
        }
    }
});
