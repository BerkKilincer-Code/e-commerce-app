from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Session için gerekli

# Ürünler listesi
products = [
    {'id': 1, 'name': 'Telefon', 'price': 1000},
    {'id': 2, 'name': 'Laptop', 'price': 5000}
]

# Sepet (oturum tabanlı)
def get_cart():
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = get_cart()
        # Aynı ürünün tekrar eklenmesini kontrol et
        for item in cart:
            if item['id'] == product_id:
                return f"{product['name']} zaten sepette!"
        cart.append(product)
        session['cart'] = cart  # Session'ı güncelle
        return f"{product['name']} sepete eklendi!"
    return "Ürün bulunamadı."

@app.route('/cart')
def view_cart():
    cart = get_cart()
    return render_template('cart.html', cart=cart)  # Sepet için bir şablon render et

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)