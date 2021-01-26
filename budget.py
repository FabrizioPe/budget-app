from math import floor


class Category:
    """
    A budget class, with methods for modifying the budget and
    recording each operation in a ledger.
    """
    def __init__(self, category):
        self.category = category.title()
        self.ledger = list()

    def deposit(self, amount, description=''):
        """Increases the budget by amount parameter."""
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        """Subtracts amount param. from budget, after checking if there's
        enough money in the budget."""
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def transfer(self, amount, destin_budget):
        """Transfers amount from this budget to another budget, if possible."""
        if self.withdraw(amount, f"Transfer to {destin_budget.category}"):
            destin_budget.deposit(amount,  f"Transfer from {self.category}")
            return True
        return False

    def get_balance(self):
        """Returns present balance based on deposits and withdrawals."""
        return sum([transaction['amount'] for transaction in self.ledger])

    def check_funds(self, amount):
        """Checks if the amount is greater than the present balance."""
        return False if amount > self.get_balance() else True

    def __str__(self):
        formatted_budget = self.category.center(30, '*') + '\n'
        for trans in self.ledger:
            formatted_budget += f"{trans['description'][:23]:23}{trans['amount']:7.2f}\n"
        formatted_budget += f"Total: {self.get_balance()}"
        return formatted_budget


def spend_list(categories):
    """Creates a list of categories paired with their percentage spendings,
    and returns it sorted by spendings in reverse order."""
    total_spend = 0
    spend_cat = []
    for cat in categories:
        spendings = -sum([trans['amount'] for trans in cat.ledger if trans['amount'] < 0])
        total_spend += spendings
        spend_cat.append([spendings, cat.category])
    # we now convert spendings to percentage values according to total_spend.
    # These percentages are rounded down to the nearest ten.
    spend_cat = [[floor((item[0] * 100 / total_spend) / 10) * 10, item[1]] for item in spend_cat]

    return spend_cat


def create_spend_chart(categories):
    """Return a string histogram of spendings (percentage) for the
     given categories."""
    data = spend_list(categories)  # extract spending data from the categories
    chart = "Percentage spent by category\n"
    # build the chart row by row (100, 90, 80, ...)
    for perc in range(100, -1, -10):
        chart += f"{perc:3}| "
        for cat in data:
            if perc <= cat[0]: chart += "o  ";
            else: chart += "   ";
        chart += '\n'
    chart += '    -' + '---' * len(data) + '\n'
    # including category names at the bottom
    max_length = max([len(item[1]) for item in data])
    for char_index in range(max_length):
        chart += "     "
        for cat in data:
            try:
                char = cat[1][char_index]
            except IndexError:
                chart += "   "
            else:
                chart += f"{char}  "
        chart += '\n'
    chart = chart[:-1]  # strip last character to match exp. output

    return chart
