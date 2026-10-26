"""Interface de démonstration PPAC : dossiers fictifs uniquement."""
import json
from pathlib import Path
import streamlit as st
from engine import generate

ROOT = Path(__file__).resolve().parent
RULES = json.loads((ROOT / 'rules.json').read_text(encoding='utf-8'))
EXAMPLE = json.loads((ROOT / 'patient_fictif.json').read_text(encoding='utf-8'))

st.set_page_config(page_title='PPAC · Démonstration', page_icon='🩺', layout='wide')
st.markdown('''<style>
.block-container {max-width: 1150px; padding-top: 2rem;}
[data-testid="stMetricValue"] {font-size: 1.7rem;}
</style>''', unsafe_allow_html=True)
st.title('PPAC · Générateur de démonstration')
st.caption('Moteur expérimental fondé sur cinq entrées du COG LTFU v6.0 (octobre 2023) — aucun examen ni périodicité prescrits.')
st.warning('Prototype non validé pour la clinique. Utiliser exclusivement des données **fictives et non identifiantes**. Ne pas importer de dossier patient réel.')

with st.sidebar:
    st.header('Dossier fictif')
    st.info('Les saisies ne sont pas enregistrées par cette application. Les téléchargements sont déclenchés uniquement par votre action.')
    st.markdown('**Référentiel** : COG LTFU v6.0, sections 33, 34, 37, 38, 39.')
    st.markdown('**Statut** : démonstration, validation médicale requise.')

left, right = st.columns([1, 1], gap='large')
with left:
    st.subheader('1. Patient et diagnostic')
    dossier = st.text_input('Identifiant fictif', value=EXAMPLE['patient_id'], help='Ne pas saisir de nom, date de naissance ou identifiant réel.')
    age = st.number_input('Âge actuel (ans)', min_value=0, max_value=110, value=22)
    sexe = st.selectbox('Sexe', ['F', 'M', 'Non renseigné'], index=0)
    diagnostic = st.selectbox('Diagnostic', ['LAL', 'LAM', 'Lymphome de Hodgkin', 'Autre'], index=0)
    st.subheader('2. Traitements reçus')
    anthra = st.selectbox('Anthracyclines', ['Reçues', 'Non reçues', 'Inconnu'], index=0)
    cortico = st.selectbox('Corticostéroïdes', ['Reçus', 'Non reçus', 'Inconnu'], index=0)
    autres = st.selectbox('Autres traitements', ['Inconnu', 'Reçus', 'Non reçus'], index=0)
with right:
    st.subheader('3. Expositions et informations complémentaires')
    molecule = st.text_input('Anthracycline(s) (si connue(s))', placeholder='Ex. doxorubicine')
    known_dose = st.checkbox('Dose cumulée d’anthracyclines connue')
    dose = st.number_input('Dose cumulée déclarée (mg/m²)', min_value=0.0, value=0.0, step=10.0, disabled=not known_dose)
    st.caption('Ne pas additionner directement les doses de molécules différentes : équivalence isotoxique à vérifier.')
    radio = st.selectbox('Radiothérapie', ['Non reçue (déclaratif)', 'Reçue', 'Inconnue'], index=0)
    greffe = st.selectbox('Greffe de CSH', ['Non reçue (déclaratif)', 'Autogreffe', 'Allogreffe', 'Inconnue'], index=0)
    fin_traitement = st.text_input('Date de fin des traitements (facultatif)', placeholder='AAAA-MM-JJ')
    complications = st.text_area('Complications connues (fictives uniquement)', placeholder='Non renseignées', height=100)

st.divider()
map_expo = {'Reçues':'recues', 'Reçus':'recus', 'Non reçues':'non_recues','Non reçus':'non_recus','Inconnu':'inconnu'}
patient = {
    'patient_id': dossier or 'FICTIF-SANS-ID', 'age_actuel': int(age), 'sexe': sexe, 'diagnostic': diagnostic,
    'radiotherapie': radio, 'greffe': greffe,
    'expositions': {'anthracyclines':map_expo[anthra], 'corticosteroides':map_expo[cortico], 'autres_traitements':map_expo[autres]},
    'anthracyclines_molecules': molecule.strip() or None,
    'anthracyclines_doses_mg_m2': dose if known_dose else None,
    'date_fin_traitement': fin_traitement.strip() or None,
    'complications': complications.strip() or 'non_renseignees',
}
result = generate(patient, RULES)
if autres != 'Non reçus' or radio != 'Non reçue (déclaratif)' or greffe != 'Non reçue (déclaratif)':
    st.info('Des expositions supplémentaires sont déclarées ou inconnues. Elles ne sont pas couvertes par les cinq règles actuellement implémentées : la sortie est **incomplète**.')
if diagnostic != 'LAL':
    st.info('La sélection d’un autre diagnostic ne constitue pas une adaptation des règles : seul le jeu expérimental d’expositions disponible est appliqué.')

m1,m2,m3 = st.columns(3)
m1.metric('Règles candidates',len(result['candidats']))
m2.metric('Règles validées',0)
m3.metric('Prescriptions générées',0)

st.subheader('4. Risques à examiner')
if not result['candidats']:
    st.info('Aucune règle candidate activée parmi les cinq règles testées. Cela ne signifie **pas** absence de risque ni absence de surveillance nécessaire.')
else:
    for candidate in result['candidats']:
        with st.expander(f"{candidate['reference']} · {candidate['domaine']} — {candidate['risque_a_examiner']}", expanded=True):
            st.write('**Évaluation médicale :**', candidate['note_medicale'])
            st.write('**Données manquantes :**', ', '.join(candidate['informations_manquantes']) if candidate['informations_manquantes'] else 'Aucune parmi les champs testés (vérification clinique toujours nécessaire).')
            st.caption('Statut : à valider · Examen : non défini · Périodicité : non définie')

st.subheader('5. Export de démonstration')
report = [
    '# PPAC — Brouillon non clinique',
    f"Dossier fictif : {patient['patient_id']}",
    f"Diagnostic : {diagnostic} · âge actuel : {age} ans · sexe : {sexe}",
    '## Expositions déclarées',
    f"Anthracyclines : {anthra}; dose : {str(dose) + ' mg/m² (à vérifier)' if known_dose else 'inconnue'}",
    f'Corticostéroïdes : {cortico}; autres traitements : {autres}',
    f'Radiothérapie : {radio}; greffe : {greffe}',
    '## Domaines à examiner (non prescriptifs)',
]
for c in result['candidats']:
    report.append(f"- {c['reference']} : {c['risque_a_examiner']}. Informations manquantes : {', '.join(c['informations_manquantes']) or 'non détectées par le prototype'}.")
report += ['## Limites', 'Règles non exhaustives, non validées cliniquement. Aucun examen ni aucune périodicité fixés. Validation médicale indispensable.']
text_report = '\n\n'.join(report)
a,b = st.columns(2)
with a:
    st.download_button('Télécharger le brouillon (Markdown)', text_report, 'ppac_brouillon_fictif.md', mime='text/markdown')
with b:
    st.download_button('Télécharger les règles candidates (JSON)', json.dumps(result, ensure_ascii=False, indent=2), 'ppac_candidats_fictifs.json', mime='application/json')
st.caption('Ce prototype reste volontairement incomplet : des données non recueillies n’équivalent pas à des expositions absentes. Les référentiels complets doivent être revus par un clinicien.')
