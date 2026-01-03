import pytest
from project.books.models import Book
from project.customers.models import Customer, _sanitize_text
from project import app, db
from datetime import datetime


@pytest.fixture
def client():
    """Konfiguracja klienta testowego Flaska i bazy danych w pamięci (RAM)."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_book_creation_sanitizes_and_validates():
    print("\n[TEST] Próba stworzenia książki z tagami HTML - oczekiwany ValueError.")
    with pytest.raises(ValueError):
        Book(
            name="<b>Clean</b>",
            author="A<script>alert(1)</script> B",
            year_published=2024,
            book_type="novel",
            status="available"
        )

def test_sanitize_text_allowed_special_characters():
    print("\n[TEST] Sprawdzanie czy znaki interpunkcyjne są dozwolone.")
    result = _sanitize_text("Harry Potter: Part 1, (New-Edition).", field="name", maxlen=64)
    assert ":" in result and "(" in result and "-" in result

def test_sanitize_text_whitespace_handling():
    print("\n[TEST] Sprawdzanie usuwania nadmiarowych spacji.")
    result = _sanitize_text("  Władca    Pierścieni  ", field="name", maxlen=64)
    assert result == "Władca Pierścieni"

def test_book_invalid_year_raises():
    print("\n[TEST] Tworzenie książki z błędnym rokiem - oczekiwany ValueError.")
    with pytest.raises(ValueError):
        Book(name="N", author="A", year_published="xxxx", book_type="t")

def test_book_year_range_too_future():
    print("\n[TEST] Rok z przyszłości - oczekiwany błąd walidacji.")
    from datetime import datetime
    future_year = datetime.utcnow().year + 5
    with pytest.raises(ValueError):
        Book(name="Future", author="Someone", year_published=future_year, book_type="novel")

def test_book_field_length_limit():
    print("\n[TEST] Zbyt długa nazwa książki - powinna zostać przycięta.")
    long_name = "X" * 100
    b = Book(name=long_name, author="A", year_published=2020, book_type="t")
    assert len(b.name) <= 64, "Nazwa książki nie została przycięta do 64 znaków"

def test_book_field_update_triggers_validation():
    print("\n[TEST] Edycja pola autora z niedozwolonymi znakami - oczekiwany ValueError.")
    b = Book(name="Good", author="OK", year_published=2020, book_type="test")
    with pytest.raises(ValueError):
        b.author = "<script>evil()</script>"

def test_customer_age_boundaries():
    print("\n[TEST] Wiek 0 i 130 - wartości brzegowe.")
    c1 = Customer(name="Noworodek", city="Gdańsk", age=0)
    c2 = Customer(name="Starzec", city="Kraków", age=130)
    assert c1.age == 0
    assert c2.age == 130

def test_customer_age_out_of_range():
    print("\n[TEST] Wiek 131 - poza zakresem.")
    with pytest.raises(ValueError, match="age is out of allowed range"):
        Customer(name="Wampir", city="Londyn", age=131)

def test_book_year_future_allowed():
    print("\n[TEST] Rok bieżący + 1 (zapowiedzi wydawnicze) - powinno być OK.")
    next_year = datetime.utcnow().year + 1
    b = Book(name="Future Book", author="Author", year_published=next_year, book_type="sci-fi")
    assert b.year_published == next_year

def test_customer_creation_sanitizes_and_validates():
    print("\n[TEST] Próba stworzenia klienta z tagami HTML - oczekiwany ValueError.")
    with pytest.raises(ValueError):
        Customer(name="<i>N</i>", city="Ci<script>ty</script>", age="23")

def test_customer_invalid_age_raises():
    print("\n[TEST] Tworzenie klienta z błędnym wiekiem - oczekiwany ValueError.")
    with pytest.raises(ValueError):
        Customer(name="N", city="C", age="old")

def test_customer_negative_age_raises():
    print("\n[TEST] Wiek ujemny - oczekiwany ValueError.")
    with pytest.raises(ValueError):
        Customer(name="Adam", city="Gdańsk", age=-5)

def test_customer_field_update_triggers_validation():
    print("\n[TEST] Edycja pola city z HTML - oczekiwany ValueError.")
    c = Customer(name="Jan", city="Warszawa", age=30)
    with pytest.raises(ValueError):
        c.city = "<script>evil()</script>"

def test_customer_field_length_limit():
    print("\n[TEST] Zbyt długa nazwa miasta - powinna zostać przycięta.")
    long_city = "X" * 200
    c = Customer(name="Tomek", city=long_city, age=20)
    assert len(c.city) <= 64, "Miasto nie zostało przycięte do 64 znaków"

def test_api_list_customers_empty(client):
    print("\n[TEST GET] Lista klientów powinna być pusta na starcie.")
    response = client.get('/customers/json')
    assert response.status_code == 200
    assert response.json['customers'] == []

def test_api_create_customer_success(client):
    print("\n[TEST POST] Tworzenie klienta przez formularz.")
    response = client.post('/customers/create', data={
        'name': 'Jan Kowalski',
        'city': 'Warszawa',
        'age': '30'
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Customer.query.filter_by(name='Jan Kowalski').first() is not None

def test_api_create_customer_invalid_data(client):
    print("\n[TEST POST] Próba stworzenia klienta z błędnym wiekiem (tekst zamiast liczb).")
    response = client.post('/customers/create', data={
        'name': 'Błąd',
        'city': 'Łódź',
        'age': 'nie-liczba'
    })
    assert response.status_code == 400
    assert b"age must be an integer" in response.data

def test_api_get_non_existent_book(client):
    print("\n[TEST GET] Próba pobrania nieistniejącej książki (404).")
    response = client.get('/books/details/Nieistniejaca')
    assert response.status_code == 404
    assert response.json['error'] == 'Book not found'