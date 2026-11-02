# Tray Timer ⏱️

Prosty minutnik siedzący w zasobniku systemowym (tray) Windows.

## Funkcje
- Ikona w trayu (generowana programowo, pokazuje postęp)
- Presety: 5, 10, 15, 25, 45 min + własny czas
- Menu PPM: Start / Pauza / Reset / Ustaw czas / Wyjdź
- Tooltip z pozostałym czasem (MM:SS)
- **Budzik** na konkretną godzinę: PPM → „Ustaw budzik...” → wpisz `HH:MM` (np. `07:30`). Jeśli godzina już minęła, budzik ustawi się na jutro. Anulujesz przez „Anuluj budzik”. Tooltip pokazuje godzinę budzika i ile zostało.
- Po zakończeniu: powiadomienie Windows + sygnał dźwiękowy, tooltip „Koniec!”

## Uruchomienie (Windows)
```bat
pip install -r requirements.txt
python tray_timer.py
```
Bez okna konsoli: `pythonw tray_timer.py`

## Budowa .exe (opcjonalnie)
```bat
pip install pyinstaller
pyinstaller --onefile --noconsole tray_timer.py
```
Plik znajdziesz w `dist\tray_timer.exe`. Wrzuć skrót do `shell:startup`, żeby startował z Windows.
