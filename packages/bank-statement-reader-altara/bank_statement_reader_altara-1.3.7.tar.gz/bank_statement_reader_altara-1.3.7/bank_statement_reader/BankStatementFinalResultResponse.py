from typing import Dict


class BankStatementFinalResultResponse:
    def __init__(self,
                 period: Dict[str, str],
                 account_name: str, account_number: str,
                 total_deposits: float, total_withdrawals: float,
                 opening_balance: float, closing_balance: float,
                 average_monthly_balance: float, excel_file_path: str,
                 salary_excel_file_path: str, selected_bank_name: str,
                 min_salary: float | None, max_salary: float | None,
                 ):
        self.account_number = account_number
        self.excel_file_path = excel_file_path
        self.salary_excel_file_path = salary_excel_file_path
        self.average_monthly_balance = average_monthly_balance
        self.closing_balance = closing_balance
        self.opening_balance = opening_balance
        self.total_withdrawals = total_withdrawals
        self.total_deposits = total_deposits
        self.account_name = account_name
        self.period = period
        self.selected_bank_name = selected_bank_name
        self.min_salary = min_salary
        self.max_salary = max_salary
