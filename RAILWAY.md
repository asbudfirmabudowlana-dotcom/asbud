# Wdrożenie BuildSmart AI na Railway

1. Utwórz konto na [Railway](https://railway.app/) i połącz je z kontem GitHub.
2. Utwórz nowy projekt, wybierz **Deploy from GitHub Repo** i wskaż repozytorium z tym projektem.
3. Po utworzeniu usługi aplikacji kliknij **New** → **Database** → **Add PostgreSQL**.
4. Otwórz usługę aplikacji → **Variables** i dodaj:

   ```text
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   JWT_SECRET=własny-długi-losowy-tekst
   CORS_ORIGINS=https://asbud-production.up.railway.app
   OPENAI_API_KEY=klucz-z-platform.openai.com
   ```

   Jeśli baza w Railway ma inną nazwę niż `Postgres`, wybierz jej `DATABASE_URL` z podpowiedzi w polu wartości zamiast przepisywać przykład.
   `OPENAI_MODEL` nie jest wymagany — aplikacja domyślnie korzysta z `gpt-5.6-terra`.

5. W **Settings** → **Networking** kliknij **Generate Domain**.
6. Otwórz wygenerowany adres. Po pierwszym uruchomieniu utwórz konto firmy na ekranie rejestracji.

## Bezpieczeństwo

- Klucza `OPENAI_API_KEY` nie umieszczaj w GitHubie ani w kodzie.
- W Railway oznacz `OPENAI_API_KEY` i `JWT_SECRET` jako **Seal** po ich zapisaniu.
- Baza jest wymagana: nie używaj lokalnego pliku SQLite w produkcji.
- Ustaw regularne kopie zapasowe PostgreSQL oraz sprawdź, czy można je odtworzyć.
- Klucze lub hasła wpisane przypadkowo na czacie traktuj jako ujawnione: unieważnij je i wygeneruj nowe.

## Płatności Stripe

1. W panelu Stripe utwórz dwa produkty: **BuildSmart AI Basic** oraz **BuildSmart AI Professional**. Dla każdego produktu utwórz dwie ceny cykliczne w PLN:

   - Basic miesięcznie: **49,00 zł**, odnawianie co miesiąc;
   - Basic rocznie: **529,20 zł**, odnawianie co rok (12 miesięcy z rabatem 10%);
   - Professional miesięcznie: **149,00 zł**, odnawianie co miesiąc;
   - Professional rocznie: **1 609,20 zł**, odnawianie co rok (12 miesięcy z rabatem 10%).
2. W usłudze aplikacji `asbud` w Railway dodaj zmienne:

   ```text
   STRIPE_SECRET_KEY=sekretny-klucz-z-trybu-testowego-Stripe
   STRIPE_PRICE_BASIC_MONTHLY=id-ceny-Basic-miesięcznej-zaczynające-się-od-price_
   STRIPE_PRICE_BASIC_YEARLY=id-ceny-Basic-rocznej-zaczynające-się-od-price_
   STRIPE_PRICE_PROFESSIONAL_MONTHLY=id-ceny-Professional-miesięcznej-zaczynające-się-od-price_
   STRIPE_PRICE_PROFESSIONAL_YEARLY=id-ceny-Professional-rocznej-zaczynające-się-od-price_
   APP_BASE_URL=https://asbud-production.up.railway.app
   ```

   Oznacz `STRIPE_SECRET_KEY` jako **Seal**. Nie wpisuj tego klucza do GitHuba ani na czacie.
3. W Stripe utwórz webhook dla adresu `https://asbud-production.up.railway.app/api/v1/billing/webhook` i wybierz zdarzenia `checkout.session.completed`, `customer.subscription.updated` oraz `customer.subscription.deleted`.
4. Skopiuj sekret webhooka do zmiennej `STRIPE_WEBHOOK_SECRET` w Railway i oznacz go jako **Seal**.
5. Na początek użyj trybu testowego Stripe. Dopiero po pomyślnym teście zamień wszystkie klucze, ceny i webhook na dane z trybu produkcyjnego.

## Firmy i NIP

W formularzu klienta wybierz **Firma**, a następnie wpisz ręcznie nazwę, NIP oraz dane kontaktowe. Aplikacja nie łączy się obecnie z bazą GUS.
