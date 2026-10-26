import unittest
import json
from pathlib import Path
from engine import generate
ROOT = Path(__file__).resolve().parent
RULES = json.loads((ROOT/'rules.json').read_text(encoding='utf-8'))
PATIENT = json.loads((ROOT/'patient_fictif.json').read_text(encoding='utf-8'))
class EngineTests(unittest.TestCase):
    def test_five_candidates(self):
        out = generate(PATIENT, RULES)
        self.assertEqual(len(out['candidats']), 5)
        self.assertTrue(all(x['periodicite'] is None and x['examens_prescrits'] == [] for x in out['candidats']))
    def test_unknown_exposure_does_not_trigger_rule(self):
        p = dict(PATIENT)
        p['expositions'] = {'anthracyclines':'inconnu','corticosteroides':'non_recus'}
        self.assertEqual(len(generate(p, RULES)['candidats']), 0)
    def test_missing_dose_is_flagged(self):
        out = generate(PATIENT, RULES)
        cardio = next(x for x in out['candidats'] if x['reference'].endswith('§34'))
        self.assertIn('anthracyclines_doses_mg_m2', cardio['informations_manquantes'])
if __name__ == '__main__': unittest.main()
