document.addEventListener('alpine:init', () => {
    Alpine.store('cart', {
        items: JSON.parse(localStorage.getItem('scentpro_cart') || '[]'),

        get count() {
            return this.items.reduce((sum, item) => sum + item.quantity, 0);
        },

        get total() {
            return this.items.reduce((sum, item) => {
                const price = parseFloat(item.price.replace('$', '').replace(',', ''));
                return sum + (price * item.quantity);
            }, 0);
        },

        addItem(product) {
            const existing = this.items.find(i => i.id === product.id);
            if (existing) {
                existing.quantity++;
            } else {
                this.items.push({
                    id: product.id,
                    name: product.name,
                    price: product.price,
                    icon: product.icon,
                    img: product.img,
                    quantity: 1
                });
            }
            this.save();

            // Dispatch event for UI feedback
            window.dispatchEvent(new CustomEvent('cart-updated', { detail: { name: product.name } }));
        },

        removeItem(id) {
            this.items = this.items.filter(i => i.id !== id);
            this.save();
        },

        updateQuantity(id, delta) {
            const item = this.items.find(i => i.id === id);
            if (item) {
                item.quantity += delta;
                if (item.quantity <= 0) {
                    this.removeItem(id);
                } else {
                    this.save();
                }
            }
        },

        clear() {
            this.items = [];
            this.save();
        },

        save() {
            localStorage.setItem('scentpro_cart', JSON.stringify(this.items));
        }
    });
});
