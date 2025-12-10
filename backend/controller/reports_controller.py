import io
from datetime import datetime, timedelta

import pandas as pd
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

from backend.model import Category


class ReportsController:
    def __init__(self, budgets_service, transactions_service):
        self.budgets = budgets_service
        self.transactions = transactions_service

    def get_bar_chart_img(self):
        end_date = datetime.now()
        start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        transactions_last_30_days = self.transactions.get_transactions_by_date(start_date=start_date,
                                                                                  end_date=end_date)

        df = pd.DataFrame([{
            'category': t.category_name,
            'date': t.date,
            'amount': self.signed_amount(t)
        } for t in transactions_last_30_days
            if not next(c for c in Category if c.category_name == t.category_name).is_income])

        budget_limits = {
            category.category_name: budget.limit
            for category, budget in self.budgets.budgets.items()
        }

        df_grouped = df.groupby('category')['amount'].sum()
        categories = df_grouped.index
        amounts = df_grouped.values

        colors = []
        for cat, amount in zip(categories, amounts):
            limit = budget_limits.get(cat)
            absolute_amount = abs(amount)
            if limit is None:
                colors.append('grey')
            elif absolute_amount < 0.5 * limit:
                colors.append('green')
            elif absolute_amount < 0.8 * limit:
                colors.append('yellow')
            else:
                colors.append('red')

        plt.bar(categories, amounts, color=colors)

        x_pos = range(len(categories))
        limit_values = []
        for cat in categories:
            limit = budget_limits.get(cat)

            if limit is not None:
                limit_values.append(-limit)
            else:
                limit_values.append(0)
        plt.hlines(
            limit_values,
            [p - 0.4 for p in x_pos],
            [p + 0.4 for p in x_pos],
            color='black',
            linestyle='--',
            linewidth=1.5
        )

        legend_handles = [
            Patch(facecolor='green', label='less than 50% spent'),
            Patch(facecolor='yellow', label='50% - 80% spent'),
            Patch(facecolor='red', label='80% or more spent'),
            Patch(facecolor='grey', label='no budget limit')
        ]

        limit_line_handle, = plt.plot(
            [], [],
            color='black',
            linestyle='--',
            linewidth=1.5,
            label='Budget limit'
        )

        legend_handles.append(limit_line_handle)

        plt.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1.05, 1), title='Legend')

        plt.title('Already spent amounts of budget limits in current month:')
        plt.ylabel('Amount (€)')
        plt.xticks(rotation=45, ha='right')
        plt.gca().invert_yaxis()

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
        img.seek(0)
        plt.close()

        return img

    def get_monthly_spending_share_chart_img(self, year, month):
        """
        Creates a donut-chart with expense shares by categories for a specified month with matplotlib.
        The png-image is returned as a picture stream.
        """
        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1) - relativedelta(seconds=1)

        all_transactions = self.transactions.get_transactions_by_date(start_date=start_date, end_date=end_date)

        spending_data = {}

        for t in all_transactions:
            category = Category.from_category_as_string(t.category_name)
            if not category.is_income:
                spending_data[t.category_name] = spending_data.get(t.category_name, 0.0) + t.amount

        labels = spending_data.keys()
        sizes = spending_data.values()

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'width': 0.3}
        )

        plt.title(f'Expenditure shares for {month:02d}.{year}')
        ax.axis('equal')

        ax.legend(loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
        img.seek(0)
        plt.close()

        return img

    def get_monthly_income_share_chart_img(self, year, month):
        """
        Creates a donut-chart with income shares by sub-categories for a specified month with matplotlib.
        The png-image is returned as a picture stream.
        """

        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1) - relativedelta(seconds=1)

        all_transactions = self.transactions.get_transactions_by_date(start_date=start_date, end_date=end_date)

        income_data = {}

        for t in all_transactions:
            category = Category.from_category_as_string(t.category_name)
            if category.is_income:
                income_data[t.sub_category] = income_data.get(t.sub_category, 0.0) + t.amount

        labels = income_data.keys()
        sizes = income_data.values()

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'width': 0.3}
        )

        plt.title(f'Income shares for {month:02d}.{year}')
        ax.axis('equal')

        ax.legend(loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
        img.seek(0)
        plt.close()

        return img

    def get_monthly_summary_chart_img(self):
        """
        Creates an account balance chart for the last 30 days with matplotlib.
        The png-image is returned as a picture stream.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        previous_transactions = self.transactions.get_transactions_by_date(end_date=start_date)
        initial_balance = sum(self.signed_amount(t) for t in previous_transactions)

        transactions_last_30_days = self.transactions.get_transactions_by_date(start_date=start_date,
                                                                                  end_date=end_date)

        df = pd.DataFrame([{
            'date': t.date,
            'amount': self.signed_amount(t)
        } for t in transactions_last_30_days])

        df['date'] = df['date'].dt.normalize()
        df['balance'] = df['amount'].cumsum() + initial_balance
        daily_balance_transactions = df.groupby('date')['balance'].last()
        date_range = pd.date_range(start=start_date.date(), end=end_date.date(), freq='D')
        daily_balance = daily_balance_transactions.reindex(date_range)
        daily_balance.iloc[0] = initial_balance
        daily_balance = daily_balance.ffill()
        daily_balance.iloc[0] = initial_balance

        plt.figure(figsize=(12, 6))
        plt.plot(date_range, daily_balance,
                 marker='o', linewidth=2.5, markersize=5,
                 color='#2196F3', label='Balance')

        plt.title('Account Balance - Last 30 Days',
                  fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Balance (€)', fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
        plt.xticks(rotation=45, ha='right')

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
        img.seek(0)
        plt.close()

        return img

    # helping methods:
    def signed_amount(self, t):
        """Amounts of transactions are saved absolute. This method adds a minus to negative amounts."""
        category = Category.from_category_as_string(t.category_name)
        return t.amount if category.is_income else -t.amount
