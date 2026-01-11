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
https://github.com/DanielTomala/tbo-25z-projekt-z1/blob/main/Flask_Book_Library/tests/test_validation.py

## CI/CD


Proces CI/CD jest zrealizowany w GitHub Actions (`.github/workflows/ci-cd.yml`).

- **Triggery:** uruchamiany na `push` do dowolnej gałęzi oraz na `pull_request` do `main`.
- **Tagowanie obrazów:**
  - `main` → budowa/publikacja obrazu z tagiem `:latest`
  np. _ghcr.io/danieltomala/tbo-25z-projekt-z1:latest_
  - pozostałe gałęzie → budowa/publikacja obrazu z tagiem `:<branch>-beta`
  np. _ghcr.io/danieltomala/tbo-25z-projekt-z1:test-branch-beta_
- **Gating przed budową obrazu:** przed `docker build` uruchamiane są:
  - testy jednostkowe (pytest),
  - SAST (Bandit),
  - SCA (OWASP Dependency-Check),
  - DAST (OWASP ZAP baseline).
  Jeśli którykolwiek krok nie przejdzie, pipeline kończy się błędem i obraz nie jest budowany/publikowany.
- **Publikacja obrazu:** obrazy są publikowane do GHCR; dla eventu `pull_request` publikacja jest pomijana.
- **DAST konfiguracja:** ZAP używa pliku `.zap/rules.tsv` do ignorowania wybranych ostrzeżeń baseline, aby utrzymać stabilne wyniki.
- **Ustawienia repozytorium:** gałąź `main` jest chroniona (wymagany PR + status checks), zgodnie z wymaganiami ograniczenia bezpośrednich zmian na gałęzi głównej.

## Podatności

Zadanie 2 zostało zrealizowne na gałęzi 'cicd-verification'.
Wprowadzono 2 celowe podatności, które mogą zostać wykorzystane, dlatego proces CI/CD kończy się niepowodzeniem.

Podatność 1 - Code Injection / Remote Code Execution
  - Endpoint przyjmuje wyrażenie z parametru `expr` i wykonuje je funkcją `eval()`, co umożliwia wykonanie kodu po stronie serwera. 
  - Lokalizacja: tbo-25z-projekt-z1/Flask_Book_Library/app.py
  - Endpoint: GET /debug/unsafe-eval
  - Wykrycie: SAST (Bandit) - reguła B307

Podatność 2 - Command Injection 
  - Endpoint przyjmuje komendę z parametru cmd i wykonuje ją przez `subprocess.check_output(cmd, shell=True, text=True)`, co umożliwia wstrzyknięcie i wykonanie komend systemowych. 
  - Endpoint: GET /debug/unsafe-cmd
  - Wykrycie: SAST (Bandit) - reguły B602/B605 (subprocess z shell=True)
  
Dowód (CI/CD):
  - Link do runa workflow (Zadanie 2):
  https://github.com/DanielTomala/tbo-25z-projekt-z1/actions/runs/20700249578/job/59421417273

