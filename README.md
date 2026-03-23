# Human Body Alphabet – Zadanie 3 (KCK)

Program rozpoznaje litery alfabetu tworzone z ciała człowieka (np. I, T, Y, L) na podstawie obrazu z kamerki lub z pliku wideo, korzystając z MediaPipe Pose oraz OpenCV.

## Zalecane wymagania

- Python 3.10
- testowano na Python 3.12.3

## Instalacja

```bash
git clone git@github.com:oliwier-ob04/lab3_HBA_KCK.git
cd lab3_HBA_KCK

python3 -m venv venv
source venv/bin/activate  # na Linux
# .\venv\Scripts\activate # na Windows

pip install --upgrade pip
pip install -r requirements.txt
```

## Uruchomienie

Skrypt `main.py` może działać w dwóch trybach:
- z kamerki (`camera`)
- z pliku wideo (`video`)

### Tryb kamerki

```bash
python3 main.py camera
```

### Tryb pliku wideo

```bash
python3 main.py video <ścieżka_do_pliku_wideo>
```

Przykład:

```bash
python3 main.py video ./video_zespolu.mp4
```
