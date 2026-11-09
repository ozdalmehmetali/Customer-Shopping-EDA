from statistics import quantiles
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)

df = pd.read_csv('/Users/apple/PycharmProjects/PythonProject1/shopping_trends.csv')

df.drop(["Customer ID", "Promo Code Used"], axis=1, inplace=True)

df.head(100)
df.info()
df.shape
df.describe().T
df.columns

cat_cols = [col for col in df.columns if str(df[col].dtypes) in ['object', 'category', 'bool']]

num_but_cat = [col for col in df.columns if df[col].nunique() < 10  and df[col].dtypes in ["int", "float"]]

cat_but_car = [col for col in df.columns if df[col].nunique() > 20 and df[col].dtypes not in ["int", "float"]]

cat_cols = cat_cols + num_but_cat

cat_cols = [col for col in cat_cols if col not in cat_but_car]

df[cat_cols].nunique()


def cat_summary(dataframe, col_name,plot=False):
    if dataframe[col_name].dtypes == "bool":
        dataframe[col_name] = dataframe[col_name].astype(int)

    print(pd.DataFrame({col_name:dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe[col_name])}))
    print("################################################")

    if plot:
        sns.countplot(x=dataframe[col_name],data=dataframe)
        plt.show(block=True)
    else:
        print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                             "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe[col_name])}))
        print("################################################")
        if plot:
            sns.countplot(x=dataframe[col_name],data=dataframe)
            plt.show(block=True)


cat_summary(df, "Gender",  plot=True)

for col in cat_cols:
    if df[col].dtype == "bool":
        df[col] = df[col].astype(int)
        cat_summary(df, col, plot=True)
    else:
        cat_summary(df, col, plot=True)


num_cols = [col for col in df.columns if df[col].dtypes  in ["int", "float"]]
num_cols = [col for col in num_cols if col not in cat_cols]

def num_summary(dataframe, numerical_cols, plot=False):
    quantiles = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    print(dataframe[numerical_cols].describe(quantiles).T)
    print("########################################################")
    if plot:
        dataframe[numerical_cols].hist()
        plt.xlabel(numerical_cols)
        plt.ylabel(numerical_cols)
        plt.show(block=True)


for col in num_cols:
    num_summary(df, col, plot=True)


def target_summary_with_cat(dataframe, target, categorical_cols, plot=False):
    print(pd.DataFrame({"TARGET_MEAN": dataframe.groupby(categorical_cols)[target].mean()}))
    if plot:
        dataframe[categorical_cols].hist()
        plt.xlabel(target)
        plt.ylabel(categorical_cols)
        plt.show(block=True)


target_summary_with_cat(df, "Purchase Amount (USD)", "Season")

for col in cat_cols:
    target_summary_with_cat(df, "Purchase Amount (USD)", col, plot=True)


def target_summary_with_num(dataframe, target, numerical_col, plot=False):
    print(dataframe.groupby(target).agg({numerical_col: "mean"}))

    if plot:
        # categorical_cols yerine numerical_col yazılmalı
        dataframe[numerical_col].hist()
        plt.xlabel(numerical_col)
        plt.title(f"{target} ve {numerical_col}")
        plt.show(block=True)


for col in num_cols:
    target_summary_with_num(df, "Purchase Amount (USD)", col, plot=True)


corr = df[num_cols].corr()

sns.heatmap(corr, annot=True)
plt.show()
