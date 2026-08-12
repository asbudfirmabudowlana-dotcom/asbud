# Procedura RODO i bezpieczeństwa — BuildSmart AI

Ten dokument jest operacyjną procedurą dla administratora platformy. Nie zastępuje umowy powierzenia, regulaminu ani porady prawnej.

## 1. Role i rejestr przetwarzania

- Operator BuildSmart AI jest administratorem danych kont, rozliczeń i obsługi platformy.
- Firma korzystająca z platformy jest administratorem danych swoich klientów, pracowników i projektów.
- Operator zawiera z taką firmą umowę powierzenia przed udostępnieniem produkcyjnej usługi.
- Utrzymuj rejestr czynności przetwarzania, wykaz dostawców i umów powierzenia.

## 2. Obsługa żądań osób, których dane dotyczą

1. Potwierdź tożsamość osoby zgłaszającej żądanie.
2. Zarejestruj żądanie, zakres danych, właściciela i termin odpowiedzi.
3. Odpowiedz bez zbędnej zwłoki, co do zasady w ciągu miesiąca.
4. Gdy zgłoszenie dotyczy danych klienta firmy korzystającej z platformy, przekaż je tej firmie i współpracuj w realizacji żądania.

## 3. Incydenty bezpieczeństwa

1. Natychmiast ogranicz dostęp: unieważnij sesje, klucze lub hasła, których dotyczy incydent.
2. Zachowaj logi i sporządź chronologię zdarzenia.
3. Oceń zakres danych, osoby objęte incydentem i ryzyko naruszenia praw oraz wolności.
4. Jeżeli wymagają tego przepisy, zgłoś naruszenie do PUODO w ciągu 72 godzin od stwierdzenia oraz powiadom osoby, których dane dotyczą.
5. Udokumentuj decyzję także wtedy, gdy zgłoszenie nie było konieczne; wykonaj działania naprawcze.

## 4. Retencja i usuwanie

- Konta i dane robocze: usuwaj lub anonimizuj zgodnie z umową po zamknięciu konta.
- Dane księgowe: przechowuj przez okres wymagany przepisami podatkowymi i rachunkowymi.
- Logi bezpieczeństwa: ogranicz do metadanych, dostęp tylko dla upoważnionych osób, okres retencji ustalony w polityce bezpieczeństwa.
- Kopie zapasowe: szyfruj, ogranicz dostęp i ustal termin automatycznego wygasania.

## 5. Minimum kontrolne przed udostępnieniem klientom

- [ ] Uzupełniono dane operatora i kontakt do spraw prywatności w polityce prywatności.
- [ ] Podpisano umowy powierzenia z dostawcami hostingu, poczty, płatności i AI.
- [ ] Ustawiono produkcyjne sekrety Railway jako Seal oraz rotację kluczy.
- [ ] Skonfigurowano SMTP, szyfrowanie sekretu 2FA i skaner załączników.
- [ ] Włączono zaszyfrowane kopie PostgreSQL oraz wykonano udany test odtworzenia.
- [ ] Sprawdzono role użytkowników, 2FA i rejestr audytowy.
