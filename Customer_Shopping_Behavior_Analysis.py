import pandas as pd
df = pd.read_csv ('customer_shopping_behavior.csv')
print(df.head())
print(df.info())

print(df.describe(include='all'))
print(df.isnull().sum())
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
print(df.columns)
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})
print(df.columns)

#create new col age_group
labels = ['Young Adult', 'Adult', 'Middle Aged', 'Senior']
df['age_group']= pd.qcut(df['age'], q=4, labels = labels)
print(df[['age','age_group']].head(10))

#create col purchase_frequency_days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['purchase_frequency_days','frequency_of_purchases']].head())

#see if discount and promo both are needed
print(df[['discount_applied','promo_code_used']].head(10))
print((df['discount_applied'] == df['promo_code_used']).all())
#both same so remove one
df = df.drop('promo_code_used', axis=1) 
print(df.columns)

## connect to database

from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = "password"
host = "localhost"
port = "3306"
database = "customer_behavior"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Write DataFrame to MySQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
pd.read_sql("SELECT * FROM customer LIMIT 5;", engine)
