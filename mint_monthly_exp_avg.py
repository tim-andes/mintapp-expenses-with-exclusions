import pandas as pd

# TODO add pytest unit test to test_unit.py
# get csv file
filename = "data/transactions.csv"
df = pd.read_csv(filename)

# convert date to datetime object
df['Date'] = pd.to_datetime(df['Date'])

# extract pertinent information
lean_df = df[['Date', 'Amount', 'Transaction Type', 'Category']]

# set date as index
lean_df = lean_df.set_index('Date')

# filter debits
categories_exclusion = ['Buy', 'Investments', 'Transfer',
			'Credit Card Payment',
			'Hide from Budgets & Trends']
debit_filter = (
		(lean_df['Transaction Type'] == 'debit') &
		(~lean_df['Category'].isin(categories_exclusion))
)

df_debit_filter = lean_df.loc[debit_filter, 'Amount']

# group by month/year, add monthly transactions, and average
grp_fil_debits = df_debit_filter.groupby(
	[(df_debit_filter.index.year), (df_debit_filter.index.month)]).sum()
  
mo_avg_expenses = grp_fil_debits.mean()

print(f"Average Monthly Expenses: $ {mo_avg_expenses:.2f}")

# for import to other modules
def mo_mint_exp(mo_avg_expenses):
	"""For purposes of importing average monthly expenses to other modules."""
	return mo_avg_expenses
