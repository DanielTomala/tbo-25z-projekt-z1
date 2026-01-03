# TBO Projekt
## Zespół 1
- Zuzanna Damszel
- Iga Mirończuk
- Jakub Szostak
- Daniel Tomala

## Konfiguracja repozytorium
Repozytorium zostało skonfigurowane w taki sposób, aby zapewniać bezpieczne wytwarzanie oprogramowania poprzez ograniczenie uprawnień dla użytkowników oraz zablokowanie dodawania kodu bezpośrednio do głównej gałęzi _main_. Został utworzony odpowiedni "branch protection rule" dla brancha _main_, który wymaga utworzenie pull requesta przed wykonaniem merga, a także jego zatwierdzenia przez "code ownera". Alternatywnie zasady te mogą zostać ominięte przez osoby, którym została przyznana specjalna rola "bypass branch protections". Dodatkowo zostały utworzone zasady, które blokują wykonywanie force pushy do wszystkich gałęzi (z wyjątkiem admina) oraz umożliwiają tworzenie, aktualizowanie i usuwanie branchy (z wyjątkiem _main_) wszystkim użytkownikom z rolą _write_.
 
## Wybrana aplikacja
Aplikacja do zarządzania biblioteką, będąca rozwinięciem aplikacji uzytej w laboratorium nr 1. 
Funkcjonalności:
- CRUD dla książek i klientów.
- Blokowanie ataków XSS (reject_on_xss=True) i rygorystyczna walidacja znaków.

##### Instrukcja uruchomienia
```
cd Python/Flask_Book_Library/
docker build -t projekt-tbo .

# Uruchomienie aplikacji
docker run -p 5000:5000 projekt-tbo

# Uruchomienie testów
docker run --rm -e PYTHONPATH=. projekt-tbo python -m pytest tests/
```

Aplikacja zawiera 19 testów weryfikujących ochronę XSS, walidację danych, logikę API i sanityzację.

## CI/CD

## Podatności
