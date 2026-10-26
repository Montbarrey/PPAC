"""Moteur exploratoire PPAC : règles candidates uniquement, sans prescription."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def generate(patient: dict, ruleset: dict) -> dict:
    candidates = []
    for rule in ruleset['rules']:
        status = patient.get('expositions', {}).get(rule['trigger'], 'inconnu')
        if status not in ('recues', 'recus'):
            continue
        missing = [field for field in rule['required'] if patient.get(field) is None or patient.get(field) == 'non_renseignees']
        candidates.append({
            'reference': rule['source'], 'domaine': rule['domain'],
            'risque_a_examiner': rule['risk'], 'informations_manquantes': missing,
            'note_medicale': rule['review'], 'statut': 'a_valider',
            'examens_prescrits': [], 'periodicite': None
        })
    return {
        'type': 'DEMONSTRATION_NON_CLINIQUE',
        'patient_fictif': patient['patient_id'],
        'diagnostic': patient.get('diagnostic'),
        'candidats': candidates,
        'alerte': 'Ce document ne constitue pas une prescription. Ne pas interpréter une donnée inconnue comme une absence d’exposition.',
        'validation_medicale': False
    }

if __name__ == '__main__':
    patient = json.loads((ROOT / 'patient_fictif.json').read_text(encoding='utf-8'))
    rules = json.loads((ROOT / 'rules.json').read_text(encoding='utf-8'))
    result = generate(patient, rules)
    (ROOT / 'sortie_demonstration.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"{len(result['candidats'])} règles candidates ; aucune périodicité ni prescription générée.")
