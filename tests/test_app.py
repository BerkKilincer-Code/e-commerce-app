import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['cart'] = []  # Her test öncesi sepeti sıfırla
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Telefon' in response.data
    assert b'Laptop' in response.data
    assert b'Sepete Ekle' in response.data

def test_add_to_cart(client):
    response = client.get('/add/1')
    assert response.status_code == 200
    assert b'Telefon sepete eklendi' in response.data

def test_add_to_cart_duplicate(client):
    # İlk ekleme
    client.get('/add/1')
    # Aynı ürünü tekrar ekleme
    response = client.get('/add/1')
    assert response.status_code == 200
    assert b'Telefon zaten sepette' in response.data

def test_add_to_cart_not_found(client):
    response = client.get('/add/999')
    assert response.status_code == 200
    assert b'\xc3\x9cr\xc3\xbcn bulunamad\xc4\xb1' in response.data

def test_view_cart_empty(client):
    response = client.get('/cart')
    assert response.status_code == 200
    assert b'Sepetiniz bo\xc5\x9f' in response.data

def test_view_cart_with_items(client):
    # Sepete bir ürün ekle
    client.get('/add/1')
    response = client.get('/cart')
    assert response.status_code == 200
    assert b'Telefon - 1000 TL' in response.data