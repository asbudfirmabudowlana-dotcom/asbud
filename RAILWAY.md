# Wdrożenie BuildSmart AI na Railway

1. Utwórz konto na [Railway](https://railway.app/) i połącz je z kontem GitHub.
2. Utwórz nowy projekt, wybierz **Deploy from GitHub Repo** i wskaż repozytorium z tym projektem.
3. Po utworzeniu usługi aplikacji kliknij **New** → **Database** → **Add PostgreSQL**.
4. Otwórz usługę aplikacji → **Variables** i dodaj:

   ```text
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   JWT_SECRET=własny-długi-losowy-tekst
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
