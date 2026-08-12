# Kopie zapasowe i odtwarzanie

## Wymagany standard produkcyjny

- Codzienny zaszyfrowany eksport PostgreSQL do oddzielnej usługi przechowywania.
- Retencja minimum: 7 kopii dziennych, 4 tygodniowe i 12 miesięcznych.
- Dostęp do kopii tylko dla wyznaczonych administratorów; sekrety przechowywane jako zmienne typu Seal.
- Test odtworzenia do odizolowanej bazy co najmniej raz na kwartał oraz po każdej istotnej zmianie bazy.

## Test odtworzenia

1. Utwórz odizolowaną, pustą bazę testową.
2. Odtwórz najnowszy backup bez zmieniania produkcyjnej bazy.
3. Sprawdź liczbę kont, klientów, projektów i dokumentów oraz możliwość zalogowania w środowisku testowym.
4. Zapisz datę, osobę wykonującą, wersję backupu, wynik oraz potrzebne działania naprawcze.

Nie uruchamiaj testu odtwarzania na produkcyjnej bazie. Railway może zapewniać kopie usługi, ale przed zaakceptowaniem ich jako jedynej kopii zapasowej trzeba zweryfikować częstotliwość, retencję i możliwość odzyskania danych.
