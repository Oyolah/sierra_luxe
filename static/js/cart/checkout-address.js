document.addEventListener('DOMContentLoaded', function() {
    // Handle address selection
    const addressRadios = document.querySelectorAll('input[name="selected_address"]');
    const newAddressForm = document.getElementById('new-address-form');
    const addressCards = document.querySelectorAll('.address-card, .address-card-new');
    
    // Make entire card clickable
    addressCards.forEach(function(card) {
        card.addEventListener('click', function(e) {
            const radio = this.querySelector('input[type="radio"]');
            if (radio && e.target !== radio) {
                radio.checked = true;
                // Trigger change event
                radio.dispatchEvent(new Event('change'));
            }
        });
    });
    
    addressRadios.forEach(function(radio) {
        radio.addEventListener('change', function() {
            // Update card styles
            addressCards.forEach(function(card) {
                card.style.borderColor = '#dee2e6';
                card.style.background = '#fff';
            });
            
            const selectedCard = this.closest('.address-card, .address-card-new');
            if (selectedCard) {
                selectedCard.style.borderColor = '#0d6efd';
                selectedCard.style.background = '#f8f9ff';
            }
            
            if (this.value === '') {
                // "Ship to a different address" selected
                newAddressForm.style.display = 'block';
                // Make new address fields required
                newAddressForm.querySelectorAll('input, select').forEach(function(field) {
                    field.required = true;
                });
            } else {
                // Saved address selected
                newAddressForm.style.display = 'none';
                // Make new address fields not required
                newAddressForm.querySelectorAll('input, select').forEach(function(field) {
                    field.required = false;
                });
            }
        });
    });
    
    // Initialize with default address selected
    const defaultRadio = document.querySelector('input[name="selected_address"]:checked');
    if (defaultRadio) {
        const defaultCard = defaultRadio.closest('.address-card, .address-card-new');
        if (defaultCard) {
            defaultCard.style.borderColor = '#0d6efd';
            defaultCard.style.background = '#f8f9ff';
        }
    }
});
