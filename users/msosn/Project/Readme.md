Projekt został opracowany na zbiorze danych superbohaterów dostępnym pod linkiem [Superheros](https://www.kaggle.com/datasets/shreyasur965/super-heroes-dataset)
W ramach projektu została przeprowadzona analiza zbioru danych, przetworzenie go w celu przygotowania do modelowania aoraz modelowanie z wykorzystaniem XGBoost.
Model na podstawie podanych cech bohatera określa jego przynależnośc do jednej z 4 klas: <u>other</u>, <u>good</u>, <u>bad</u> i <u>neutral</u>

Projekt składa się z następujących plików
- [requirements.txt](requirements.txt) - informacja o wymaganych bibliotekach
- [my_report.html](my_report.html) - raport z analiza statystyczną danych
- [data_set_profile.ipnyb](data_set_profile.ipynb) - skrypt wykorzystany do wygenerowania [my_report.html](my_report.html)
- [data_analysis_and_preparation.ipynb](data_analysis_and_preparation.ipynb) - skrypt zawierający operacje przygotowujące data set do modelowania
- [model.ipynb](model.ipynb) - właściwy skrypt w którym odbywa się końcowe przygtowanie danych do modelowanie (SMOTE, PCA), samo modelowanie, dostrajanie i analiza modelu przy pomocy wartości Shapleya
- [utils](utils) - katalog ze skryptami pomocniczymi:
  - [analizing_utlis.py](utils/analizing_utils.py) - funkcje wykorzystane przy analizie i przygotowaniu danych
  - [extraction_utils.py](utils/extraction_utils.py) - funkcje wykorzystane do ekstrakcji danych z column zawierajacych bardziej zlozone struktury (w tym wypadku lista w kolumnie)
  - [json_utils.py](utils/json_utils.py) - funkcje wykorzystywane do zapisu i odczytu danych z jsona
  - [optuna_utils.py](utils/optuna_utils.py) - funkcje wspomagające pracę z optuna
  - [pca_utils.py](utils/pca_utils.py) - funkcje wspomagające pracę z PCA
- [configuration](configuration) - katalog z konfiguracją
  - [config.jso](configuration/config.json) - plik konfiguracyjny m.in. z random state i tablicą nazw kolun wykorzystywanych przy modelowaniu
  - [configuration.py](configuration/configuration.py) - zawiera klase obsługującą konfiguraje oraz kod umożliwiający jej odczyt i zapis do pliku json
  - [xgb_hiperparameters.json](configuration/xgb_hiperparameters.json) - plik zwierający najlepsze hiperparametry wyznaczone przy pomocy Optuna