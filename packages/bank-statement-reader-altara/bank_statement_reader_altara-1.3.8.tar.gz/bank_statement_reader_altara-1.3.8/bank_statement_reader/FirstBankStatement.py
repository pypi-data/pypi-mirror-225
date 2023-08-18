from bank_statement_reader.BaseBankStatementReport import BankStatementReport
import re


class FirstBankStatement(BankStatementReport):

    def __init__(self, pdf_directory, password, min_salary, max_salary):
        if pdf_directory is None or pdf_directory == '':
            pdf_directory = "pdfs/firstbank.pdf"
            password = "81054"
        super().__init__(password=password, pdf_directory=pdf_directory, min_salary=min_salary, max_salary=max_salary, bank_name='first')

    def get_opening_balance(self, text):
        pattern = r'Opening Balance[:.]?\s*(-?[\d,.]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            opening_balance = match.group(1)
            return opening_balance
        else:
            return None
        pass

    def get_closing_balance(self, text):
        pattern = r'Closing Balance[:.]?\s*(-?[\d,.]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            closing_balance = match.group(1)
            return closing_balance
        else:
            return None

    def get_transactions_table_header_mapping(self):
        return {
            'transdate': 'TransDate',
            'reference': 'Reference',
            'transaction_details': 'Transaction Details',
            'valuedate': 'ValueDate',
            'deposit': 'Deposit',
            'withdrawal': 'Withdrawal',
            'balance': 'Balance'
        }

    def get_transactions_table_headers(self, reader):
        return self.get_transactions_table_header_mapping().values()

    def pad_header_with_unknown(self, rows, headers):
        if len(rows[0]) > len(headers):
            # New item to be inserted
            unknown = 'Unknown'

            # Index of "Value Date" in the list
            value_date_index = headers.index('Value Date')

            # Insert the new item before "Value Date"
            headers.insert(value_date_index, unknown)
            return headers
        else:
            return headers

    def get_transactions_table_rows(self, reader, page=0):
        split_balance_bf_balance = 0
        if page == 0:
            table = reader.pages[page].extract_tables()[0]
            rows_without_header = table[1:]
            balance_bf = [item for item in rows_without_header if 'Balance B/F' in item[0]]

            split_balance_bf = balance_bf[0][0].split()
            split_balance_bf_balance = split_balance_bf[len(split_balance_bf) - 1]
            balance_bf[0][2] = 'Balance B/F'
            balance_bf[0][6] = split_balance_bf_balance
        else:
            table = reader.pages[page].extract_tables()[0]
            rows_without_header = table[1:]
        rows_without_header = [item for item in rows_without_header if 'END OF STATEMENT' not in item[0]]
        rows_without_header = [item for item in rows_without_header if 'Balance B/F' not in item[0]]
        for row in rows_without_header:
            split_list = row[0].split()
            last_item_in_split_list = split_list[len(split_list) - 1]
            trans_date = split_list[0]
            reference = ''
            transaction_details = split_list[1] + ' ' + split_list[2] + ' ' + split_list[3] + last_item_in_split_list
            value_date = split_list[4]

            deposit = split_list[5]
            withdrawal = split_list[5]
            balance = split_list[len(split_list) - 2]
            row[0] = trans_date
            row[1] = reference
            row[2] = transaction_details
            row[3] = value_date
            row[4] = deposit
            row[5] = withdrawal
            row[6] = balance
        modified_rows = [[item.replace('\n', '').strip() if item else '' for item in row] for row in
                         rows_without_header]

        for index, row in enumerate(modified_rows):
            current_row = modified_rows[index]
            previous_row = modified_rows[index - 1]
            current_row_balance = current_row[6]
            previous_row_balance = previous_row[6]
            if index != 0:
                if current_row_balance > previous_row_balance:
                    balance = row[4]
                    row[4] = balance
                    row[5] = None
                else:
                    row[4] = None
                    row[5] = balance
            else:
                if current_row_balance > split_balance_bf_balance:
                    balance = row[4]
                    row[4] = balance
                    row[5] = None

        return modified_rows

    def result(self):
        reader, status, message = self.get_pdf_reader()
        print(message)
        if status == 0:
            raise Exception("Reading of file failed")
        text = self.get_pdf_page_text(reader)
        cleaned_text = self.clean_text(text)

        statement_period_extracted = self.get_statement_period(cleaned_text)
        account_name_extracted = self.get_account_name(cleaned_text)
        account_number_extracted = self.get_account_number(cleaned_text)
        total_withdrawals_extracted = self.get_total_withdrawal(cleaned_text)
        total_deposit_extracted = self.get_total_deposit(cleaned_text)
        opening_balance_extracted = self.get_opening_balance(cleaned_text)
        closing_balance_extracted = self.get_closing_balance(cleaned_text)

        table_headers = self.get_transactions_table_headers(reader)

        num_pages = len(reader.pages)
        trans_rows = []
        for page_num in range(num_pages):
            try:
                new_rows = self.get_transactions_table_rows(reader, page_num)
                trans_rows.extend(new_rows)
            except Exception as e:
                print(page_num)
                print("from result", e)
        if opening_balance_extracted is None:
            opening_balance_extracted = trans_rows[0][5]

        if closing_balance_extracted is None:
            closing_balance_extracted = trans_rows[len(trans_rows) - 1][5]
        formatted_df = self.format_dataframe_columns(table_headers, table_rows=trans_rows)
        average_monthly_balance = self.get_average_monthly_balance(formatted_df)

        return {
            'dataframe': formatted_df,
            'period': statement_period_extracted,
            "account_name": account_name_extracted,
            "account_number": account_number_extracted,
            "total_turn_over_credit": total_deposit_extracted,
            "total_turn_over_debits": total_withdrawals_extracted,
            "opening_balance": opening_balance_extracted,
            "closing_balance": closing_balance_extracted,
            "average_monthly_balance": average_monthly_balance,
        }

    def predict_salary_income(self, dataframe, table_headers):
        # Filter the DataFrame to get rows with values within the specified range
        filtered_df = dataframe[(dataframe['Deposits'] >= self.min_salary) & (dataframe['Deposits'] <= self.max_salary)]
        if filtered_df.empty:
            return None

        potential_salary = []
        for index, row in filtered_df.iterrows():
            unique = self.is_unique_amount_in_month_year(row, filtered_df)
            if not unique:
                continue
            potential_salary.append([
                row['Transaction Date'],
                row['Reference'],
                row['Description'],
                row['Value Date'],
                row['Deposits'],
                row['Withdrawals'],
                row['Balance'],
            ])
        salary_df = self.format_dataframe_columns(table_headers, potential_salary)
        return salary_df
