from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
#Import relatif : rapport au fichier courant.
#   . : "le dossier courant"
#   .. : "le dossier parent"
from tasks.models import Task

'''
import unittest
import json
from pathlib import Path
from django.test.runner import DiscoverRunner
'''


#TEST_RESULTS = {}

def tc(case_id):
    def decorator(func):
        func.test_case_id = case_id
        return func
    return decorator

class TaskModelTest(TestCase):
    
    @tc("TC001")
    def test_str_returns_title(self):
        task = Task(title="My task")

        self.assertEqual(str(task), "My task")


class TaskViewsTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Demo task")

    @tc("TC002")
    def test_homepage_renders(self):
        response = self.client.get(reverse("list"))
        self.assertEqual(response.status_code, 200)

    @tc("TC003")
    def test_create_task_via_post(self):
        response = self.client.post(reverse("list"), {"title": "New task"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="New task").exists())

    @tc("TC004")
    def test_update_page_renders(self):
        response = self.client.get(reverse("update_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    @tc("TC005")
    def test_update_task_via_post(self):
        response = self.client.post(
            reverse("update_task", args=[self.task.id]),
            {"title": "Updated title"},
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated title")

    @tc("TC006") 
    def test_delete_page_renders(self):
        response = self.client.get(reverse("delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    @tc("TC007")
    def test_delete_task_via_post(self):
        response = self.client.post(reverse("delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

class TestDatasetLoading(TestCase):
    @tc("TC008")
    def test_load_initial_data(self):
        call_command('loaddata', 'dataset.json')

        self.assertEqual(Task.objects.count(), 3)
        titles = set(Task.objects.values_list("title", flat=True))
        self.assertSetEqual(
            titles,
            {"Configurer Ruff", "Ecrire des tests", "Preparer la release"},
        )

'''
class JSONResult(unittest.TextTestResult):


    def _record(self, test, status: str) -> None:
        tc_id = getattr(test, "test_case_id", None)

        if tc_id is None:
            method_name = getattr(test, "_testMethodName", None)
            if method_name:
                method = getattr(test, method_name, None)
                tc_id = getattr(method, "test_case_id", None)

        if not tc_id:
            return

        TEST_RESULTS[tc_id] = status

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record(test, "passed")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record(test, "failed")

    def addError(self, test, err):
        super().addError(test, err)
        self._record(test, "failed")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._record(test, "failed")


class JSONTestRunner(DiscoverRunner):

    def get_resultclass(self):
        return JSONResult

    def run_suite(self, suite, **kwargs):
        result = super().run_suite(suite, **kwargs)

        out_file = Path("result_test_auto.json")
        with out_file.open("w", encoding="utf-8") as f:
            json.dump(TEST_RESULTS, f, indent=2, ensure_ascii=False)

        print(f"\nRésultats auto exportés dans {out_file.resolve()}")
        return result
        '''