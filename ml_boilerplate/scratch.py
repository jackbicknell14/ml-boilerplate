import pandas as pd
from tools import get_X_and_y, TrainLinearReg

df = pd.read_csv('/Users/jackbicknell/Documents/github/divyd/analysis/df.csv', index_col=0)
print(df.head())

binary_cols = []
categorical_cols = ['category', 'customer_id', 'weekday', 'day_of_month']
text_cols = []
numeric_cols = []
target_column = 'amount'
cols_to_drop = ['made_on']

# Partition data set into training/test split (2 to 1 ratio)
X, y, x_cols = get_X_and_y(df, target_column, cols_to_drop, binary_cols, categorical_cols, text_cols, numeric_cols)
linreg = TrainLinearReg(X, y, x_cols, binary_cols, text_cols, categorical_cols, numeric_cols)
print('')
print(x_cols)
print('')
# print(linreg.pipeline[0][1].transformer_list[0])
print('')
# print(linreg.pipeline[0][1].transformer_list[-1])
linreg.train_model()
