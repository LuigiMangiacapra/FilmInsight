# FilmInsight

**FilmInsight** è un sistema di raccomandazione di film basato sulla conoscenza, progettato per fornire suggerimenti altamente personalizzati sfruttando dati strutturati e tecniche avanzate. Combina informazioni provenienti dal dataset MovieLens Small con metadati arricchiti da DBpedia tramite query SPARQL. Il sistema utilizza algoritmi di *Multi-Armed Bandit (MAB)* per bilanciare esplorazione e sfruttamento, garantendo suggerimenti sempre aggiornati e rilevanti.

---

## 🌟 Funzionalità principali
- **Estrazione di conoscenze da DBpedia**: Recupera informazioni avanzate sui film, come cast, registi, temi e altro ancora.
- **Sistema di raccomandazione basato su conoscenza**: Suggerisce film in base alle preferenze dell'utente e alle caratteristiche dei film.
- **Bilanciamento Exploration vs Exploitation**: Integra algoritmi MAB come *Epsilon-Greedy* e *UCB* per ottimizzare le raccomandazioni.
- **Valutazione rigorosa**: Metriche standard per garantire accuratezza e rilevanza nelle raccomandazioni.

---

## 🗂️ Struttura del progetto
- **`data/`**: 
  - Contiene i dataset originali (`raw/`), i file processati (`processed/`) e i risultati delle query DBpedia (`dbpedia/`).
- **`src/`**: 
  - Include gli script principali per la gestione dei dati, le query SPARQL e l'implementazione del recommender system.
- **`notebooks/`**: 
  - Jupyter Notebook per analisi preliminari, esplorazioni ed esperimenti.
- **`tests/`**: 
  - Contiene test unitari per verificare il corretto funzionamento del codice.
- **`docs/`**: 
  - Documentazione aggiuntiva, come architettura del sistema e riferimenti bibliografici.

---

## 🔧 Installazione

1. **Clona il repository**:
   ```bash
   git clone <URL-del-repo>
   cd FilmInsight
