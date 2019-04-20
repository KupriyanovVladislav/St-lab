class Department:

    def __init__(self, name: str, employees: dict, budget: int):
        self.name = name
        self.employees = employees
        self.budget = budget

    class BudgetError(ValueError):
        pass

    def get_budget_plan(self):
        salaries = sum(self.employees.values())
        budget_plan = self.budget - salaries
        if budget_plan < 0:
            raise Department.BudgetError
        else:
            return budget_plan

    @property
    def average_salary(self):
        return round(sum(self.employees.values())/len(self.employees), 2)

    @staticmethod
    def merge_departments(*args):
        budgets = list()
        new_employees = dict()
        names = list()
        for obj in args:
            budgets.append(obj.budget)
            new_employees.update(obj.employees)
            names.append((obj.name, obj.average_salary))
        new_budget = sum(budgets)
        names.sort(key=lambda x: (-x[1], x[0]))
        new_name = " - ".join([name[0] for name in names])
        new_department = Department(new_name, new_employees, new_budget)
        if new_department.get_budget_plan() >= 0:
            return new_department

    def __add__(self, other):
        return Department.merge_departments(self, other)

    def __str__(self):
        return f"{self.name} ({len(self.employees)} - {self.average_salary}, {self.budget})"

    def __or__(self, other):
        plan_budjet_1 = self.get_budget_plan()
        plan_budjet_2 = other.get_budget_plan()
        if plan_budjet_1 == plan_budjet_2:
            return self
        else:
            return self if plan_budjet_1 > plan_budjet_2 else other
