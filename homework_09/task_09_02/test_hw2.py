import unittest

from random import randint
from .task_02_01 import Department


class MyTest(unittest.TestCase):
    def test_budget_plan(self):
        budget = randint(1, pow(10, 6))
        employers = {str(i): randint(0, 10) for i in range(10)}
        dep = Department('education', employers, budget)
        self.assertEqual(budget - sum(employers.values()), dep.get_budget_plan())
        budget = 0
        dep = Department('education', employers, budget)
        self.assertRaises(Department.BudgetError, dep.get_budget_plan)

    def test_average_salary(self):
        employers = {str(i): randint(0, 10) for i in range(10)}
        budget = randint
        dep = Department('1', employers, budget)
        self.assertEqual(sum(employers.values()) / len(employers), dep.average_salary)

    def test_merge_departments(self):
        dep1 = Department('education', {'1': 1500}, 1000)
        dep2 = Department('medicine', {'2': 1000}, 3000)
        dep3 = Department('enum', {'3': 1000}, 2000)
        merged = Department.merge_departments(dep1, dep2, dep3)
        self.assertEqual(merged.name, 'education - enum - medicine')

        dep2.budget = 0
        self.assertRaises(Department.BudgetError, Department.merge_departments, *[dep1, dep2, dep3])

    def test_add(self):
        dep1 = Department('education', {'1': 1500}, 1000)
        dep2 = Department('medicine', {'2': 1000}, 3000)

        dep_sum = dep1 + dep2
        self.assertEqual('education - medicine', dep_sum.name)

        dep2.budget = 0
        self.assertRaises(Department.BudgetError, Department.merge_departments, *[dep1, dep2])

    def test_str(self):
        dep1 = Department('education', {'1': 1500}, 1000)
        self.assertEqual('education (1 - 1500.0, 1000)', dep1.__str__())

    def test_or(self):
        dep1 = Department('education', {'1': 1500}, 2000)
        dep2 = Department('medicine', {'2': 1000}, 3000)
        self.assertEqual(dep2, dep1 | dep2)

        dep2.budget = 1500
        self.assertEqual(dep1, dep1 | dep2)

        dep1.budget = 1000
        self.assertRaises(Department.BudgetError, dep1.__or__, dep2)


if __name__ == '__main__':
    unittest.main()
