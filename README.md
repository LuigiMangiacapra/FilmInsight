# FilmInsight 🎥✨

**FilmInsight** è un sistema avanzato di raccomandazione di film basato sulla conoscenza, pensato per offrire suggerimenti personalizzati sfruttando non solo le preferenze degli utenti, ma anche informazioni arricchite sui film provenienti da fonti esterne. Attraverso l'integrazione di dati da DBpedia e l'uso di algoritmi di *Multi-Armed Bandit (MAB)*, FilmInsight ottimizza continuamente l'esperienza dell'utente, bilanciando esplorazione e sfruttamento.

---

## 🔍 Perché FilmInsight?
L'obiettivo principale di FilmInsight è superare i limiti dei tradizionali sistemi di raccomandazione basati esclusivamente su statistiche o valutazioni degli utenti. Questo sistema:
- Arricchisce i dati con informazioni semantiche (es. registi, trame, temi) da **DBpedia**.
- Offre raccomandazioni non banali, andando oltre i semplici gusti "popolari".
- Adotta approcci di *Reinforcement Learning* per adattarsi dinamicamente agli utenti.

---

## 🚀 Caratteristiche principali
1. **Dati arricchiti**: FilmInsight sfrutta DBpedia per aggiungere metadati sui film (come cast, generi e curiosità), rendendo le raccomandazioni più intelligenti.
2. **Approccio innovativo**: Usa tecniche di *Multi-Armed Bandit* per migliorare continuamente i suggerimenti, esplorando nuovi film senza sacrificare la qualità delle raccomandazioni.
3. **Analisi dettagliata**: Include strumenti per analizzare le performance del sistema attraverso metriche consolidate nel campo della raccomandazione.

---

## 🛠️ Struttura del progetto

- **`data/`**: 
  - Contiene i file di dati grezzi (`raw/`), i dataset processati (`processed/`) e una cache dei risultati delle query a DBpedia (`dbpedia/`).
  
- **`src/`**:
  - **`data_processing.py`**: Pulizia e pre-elaborazione del dataset MovieLens.
  - **`dbpedia_queries.py`**: Interfaccia per estrarre informazioni da DBpedia.
  - **`recommender.py`**: Il cuore del sistema di raccomandazione.
  - **`evaluation.py`**: Strumenti per la valutazione delle performance.

- **`notebooks/`**: Contiene analisi esplorative e prototipi in Jupyter Notebook.

- **`tests/`**: Suite di test per verificare la correttezza del codice.

---

## 📋 Requisiti
1. **Python 3.7+**
2. **Librerie richieste**: Tutte le dipendenze sono elencate nel file `requirements.txt`. Installa con:
   ```bash
   pip install -r requirements.txt
