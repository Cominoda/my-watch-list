'''
import json
from pathlib import Path
from django.test.runner import DiscoverRunner
import unittest

# Dictionnaire global pour stocker les résultats
TEST_RESULTS = {}


class JSONResult(unittest.TextTestResult):
    """Classe qui capture les résultats des tests avec leurs IDs."""
    
    def _record(self, test, status: str) -> None:
        """Enregistre le résultat d'un test avec son ID."""
        # Récupère le test_case_id depuis le décorateur @tc
        tc_id = None
        
        # Essaie d'abord de récupérer directement depuis l'instance
        if hasattr(test, "test_case_id"):
            tc_id = test.test_case_id
        else:
            # Sinon, récupère via le nom de la méthode
            method_name = getattr(test, "_testMethodName", None)
            if method_name:
                method = getattr(test, method_name, None)
                if method:
                    tc_id = getattr(method, "test_case_id", None)
        
        if tc_id:
            TEST_RESULTS[tc_id] = {
                "id": tc_id,
                "type": "auto",
                "status": status
            }
    
    def addSuccess(self, test):
        """Test réussi."""
        super().addSuccess(test)
        self._record(test, "passed")
    
    def addFailure(self, test, err):
        """Test échoué (assertion failed)."""
        super().addFailure(test, err)
        self._record(test, "failed")
    
    def addError(self, test, err):
        """Test en erreur (exception)."""
        super().addError(test, err)
        self._record(test, "failed")
    
    def addSkip(self, test, reason):
        """Test ignoré."""
        super().addSkip(test, reason)
        self._record(test, "skipped")


class JSONTestRunner(DiscoverRunner):
    """Test runner personnalisé qui génère result_test_auto.json."""
    
    def get_resultclass(self):
        """Utilise notre classe JSONResult pour capturer les résultats."""
        return JSONResult
    
    def run_suite(self, suite, **kwargs):
        """Exécute les tests et génère le fichier JSON."""
        # Réinitialise les résultats
        global TEST_RESULTS
        TEST_RESULTS = {}
        
        # Exécute les tests
        result = super().run_suite(suite, **kwargs)
        
        # Génère le fichier JSON
        out_file = Path("result_test_auto.json")
        
        # Convertit le dictionnaire en liste d'objets
        results_list = list(TEST_RESULTS.values())
        
        with out_file.open("w", encoding="utf-8") as f:
            json.dump(results_list, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Résultats auto exportés dans {out_file.resolve()}")
        
        return result
'''

import json
from pathlib import Path
from django.test.runner import DiscoverRunner
import unittest

# Dictionnaire global pour stocker les résultats
TEST_RESULTS = {}


class JSONResult(unittest.TextTestResult):
    """Classe qui capture les résultats des tests avec leurs IDs."""
    
    def _record(self, test, status: str) -> None:
        """Enregistre le résultat d'un test avec son ID."""
        # Récupère le test_case_id depuis le décorateur @tc
        tc_id = None
        
        # Essaie d'abord de récupérer directement depuis l'instance
        if hasattr(test, "test_case_id"):
            tc_id = test.test_case_id
        else:
            # Sinon, récupère via le nom de la méthode
            method_name = getattr(test, "_testMethodName", None)
            if method_name:
                method = getattr(test, method_name, None)
                if method:
                    tc_id = getattr(method, "test_case_id", None)
        
        if tc_id:
            TEST_RESULTS[tc_id] = status
    
    def addSuccess(self, test):
        """Test réussi."""
        super().addSuccess(test)
        self._record(test, "passed")
    
    def addFailure(self, test, err):
        """Test échoué (assertion failed)."""
        super().addFailure(test, err)
        self._record(test, "failed")
    
    def addError(self, test, err):
        """Test en erreur (exception)."""
        super().addError(test, err)
        self._record(test, "failed")
    
    def addSkip(self, test, reason):
        """Test ignoré."""
        super().addSkip(test, reason)
        self._record(test, "skipped")


class JSONTestRunner(DiscoverRunner):
    """Test runner personnalisé qui génère result_test_auto.json."""
    
    def get_resultclass(self):
        """Utilise notre classe JSONResult pour capturer les résultats."""
        return JSONResult
    
    def run_suite(self, suite, **kwargs):
        """Exécute les tests et génère le fichier JSON."""
        # Réinitialise les résultats
        global TEST_RESULTS
        TEST_RESULTS = {}
        
        # Exécute les tests
        result = super().run_suite(suite, **kwargs)
        
        # Génère le fichier JSON
        out_file = Path("result_test_auto.json")
        with out_file.open("w", encoding="utf-8") as f:
            json.dump(TEST_RESULTS, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Résultats auto exportés dans {out_file.resolve()}")
        
        return result

        