"""Run with python3 -m unittest discover -s tests -v."""
import copy
import importlib
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import campus


class CampusTests(unittest.TestCase):
    def setUp(self):
        importlib.reload(campus)

    def call(self, function, *args):
        output = io.StringIO()
        with redirect_stdout(output):
            function(*args)
        return output.getvalue()

    def snapshot(self):
        return copy.deepcopy((campus.resources, campus.borrow_records))

    def test_required_demo(self):
        output = self.call(campus.run_demo)
        self.assertEqual([r['available'] for r in campus.resources], [9, 2, 3])
        self.assertEqual([r['outstanding'] for r in campus.borrow_records], [1, 3])
        for text in ('Total units: 18', 'Available units: 14',
                     'Units currently borrowed: 4', 'Keyboard (R002): 2 available',
                     'Keyboard: 3 units currently borrowed'):
            self.assertIn(text, output)

    def test_rejected_borrowing_preserves_all_state(self):
        for args in [('F999', 'R001', 1), ('F001', 'R999', 1),
                     ('F001', 'R001', 11), ('F001', 'R001', 0),
                     ('F001', 'R001', -2), ('F001', 'R001', '2'),
                     ('F001', 'R001', 1.5), ('F001', 'R001', True)]:
            with self.subTest(args=args):
                before = self.snapshot()
                self.assertIn('Error:', self.call(campus.borrow_resource, *args))
                self.assertEqual(self.snapshot(), before)

    def test_return_across_multiple_loans(self):
        self.call(campus.borrow_resource, 'F001', 'R001', 2)
        self.call(campus.borrow_resource, 'F001', 'R001', 3)
        self.call(campus.return_resource, 'F001', 'R001', 4)
        self.assertEqual(campus.find_resource('R001')['available'], 9)
        self.assertEqual([r['outstanding'] for r in campus.borrow_records], [0, 1])
        before = self.snapshot()
        self.call(campus.return_resource, 'F001', 'R001', 2)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_returns_preserve_state(self):
        self.call(campus.borrow_resource, 'F001', 'R001', 2)
        for args in [('F999', 'R001', 1), ('F001', 'R999', 1),
                     ('F002', 'R001', 1), ('F001', 'R001', 0),
                     ('F001', 'R001', -1), ('F001', 'R001', '1')]:
            before = self.snapshot()
            self.assertIn('Error:', self.call(campus.return_resource, *args))
            self.assertEqual(self.snapshot(), before)

    def test_inventory_validation(self):
        self.call(campus.add_resource, ' r004 ', ' Projector ', ' Electronics ', 4)
        self.assertEqual(campus.find_resource('R004')['total'], 4)
        for args in [('r004', 'Mouse', 'Accessories', 2),
                     ('R005', 'Monitor', 'Electronics', -2),
                     ('', 'Monitor', 'Electronics', 2)]:
            before = self.snapshot()
            self.assertIn('Error:', self.call(campus.add_resource, *args))
            self.assertEqual(self.snapshot(), before)

    def test_search_and_category(self):
        self.assertIn('Laptop', self.call(campus.search_resources, 'LAPtop'))
        output = self.call(campus.filter_by_category, 'ACCESSORIES')
        self.assertIn('Keyboard', output)
        self.assertIn('Headset', output)
        self.assertNotIn('Laptop', output)
        self.assertIn('No resources', self.call(campus.search_resources, 'Printer'))
        self.assertIn('Error:', self.call(campus.search_resources, ' '))

    def test_tied_leaders(self):
        self.call(campus.borrow_resource, 'F001', 'R001', 3)
        self.call(campus.borrow_resource, 'F002', 'R002', 3)
        output = self.call(campus.generate_report)
        self.assertIn('Laptop: 3 units currently borrowed', output)
        self.assertIn('Keyboard: 3 units currently borrowed', output)

    def test_empty_inventory_and_no_loans(self):
        self.assertIn('No resources are currently borrowed', self.call(campus.generate_report))
        campus.resources.clear()
        self.assertIn('No resources found', self.call(campus.list_resources))
        self.assertIn('Total units: 0', self.call(campus.generate_report))

    def test_menu_invalid_input_and_exit(self):
        answers = ['9', '3', 'f001', ' R001 ', 'solo', '0', '2', '2', '0']
        with patch('builtins.input', side_effect=answers):
            output = self.call(campus.main)
        self.assertIn('Choose a menu option from 0 to 7', output)
        self.assertIn('Enter a whole number', output)
        self.assertIn('Enter a number greater than zero', output)
        self.assertIn('Available: 8', output)
        self.assertIn('Goodbye!', output)


if __name__ == '__main__':
    unittest.main()
