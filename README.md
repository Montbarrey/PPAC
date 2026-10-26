# PPAC v0.2 — prototype de démonstration

Application Streamlit expérimentale pour **données fictives uniquement**. Ne pas utiliser pour des décisions médicales ou des données personnelles.

## Tester sans installation avec GitHub Codespaces
1. Créer un dépôt **privé** sur GitHub.
2. Importer **tout le contenu de ce dossier**, y compris `.devcontainer/devcontainer.json` (à la racine du dépôt).
3. `Code` → `Codespaces` → `Create codespace on main`.
4. Attendre la fin de `pip install -r requirements.txt` dans le terminal.
5. Exécuter `streamlit run app.py --server.address 0.0.0.0 --server.port 8501`.
6. Ouvrir l'onglet **Ports**, puis le port **8501** (ou la notification d'ouverture automatique). Garder le port privé.

## Sur un ordinateur avec Python
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Tests du moteur
```bash
python -m unittest discover -v
```

## Contenu
- `app.py` : interface de saisie et export Markdown / JSON
- `engine.py` : moteur de sélection de *candidats*, sans prescription
- `rules.json` : cinq règles exploratoires COG v6 (sections 33, 34, 37, 38, 39)
- `patient_fictif.json` : cas fictif LAL 22 ans
- `test_engine.py` : tests unitaires

## Limites
Les règles ne sont ni exhaustives ni validées par un comité clinique. Le modèle ne gère pas encore les seuils, les fréquences, les expositions combinées, ni une surveillance individualisée. Une absence de règle déclenchée ne signifie pas absence de risque. Aucune base de données ou connexion au SI hospitalier. Ne pas importer de données patient réelles. Le dépôt privé ne constitue pas à lui seul un environnement conforme à l'hébergement de données de santé.

Source : Children's Oncology Group, Long-Term Follow-Up Guidelines, version 6.0 (octobre 2023). Vérifier toute adaptation avant application clinique.
