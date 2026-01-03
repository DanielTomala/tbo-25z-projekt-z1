# TBO Projekt
## Zespół 1
- Zuzanna Damszel
- Iga Mirończuk
- Jakub Szostak
- Daniel Tomala

## Konfiguracja repozytorium
Repozytorium zostało skonfigurowane w taki sposób, aby zapewniać bezpieczne wytwarzanie oprogramowania poprzez ograniczenie uprawnień dla użytkowników oraz zablokowanie dodawania kodu bezpośrednio do głównej gałęzi _main_. Został utworzony odpowiedni "branch protection rule", dla brancha _main_, który wymaga utworzenie pull requesta przed wykonaniem merga, a także jego zatwierdzenia przez "code ownera". Ponadto branch _main_ została przełączona w tryb "read-only", aby uniemożliwić jego nieautoryzowaną zmianę. Powyższa zasada może, zostać ominieta przez administratora repozytorium oraz osoby, którym zostały przyznane specjalne role "bypass branch protections". Dodatkowo zostały utworzone zasady, które blokują wykonywanie force pushy do wszystkich gałęzi (z wyjątkiem admina) oraz umożliwiają na tworzenie, aktualizowanie i usuwanie branchy (z wyjątkiem _main_) wszystkim użytkowniką z rolą _write_.
 
## Wybrana aplikacja

## CI/CD

## Podatności
