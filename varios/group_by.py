import pandas as pd

pagos = pd.read_excel("./varios/RepFormatoPago.xlsx")

print('\n' * 2, 'Agrupacion por columna')
print(pagos.groupby('co_tipo_doc')[['mont_doc']].sum())

print('\n' * 2, 'Agrupacion por dos columnas')
print(pagos.groupby(['co_tipo_doc', 'co_prov'])[['mont_doc']].sum())

print('\n' * 2, 'Agrupacion por tipo de documento con mayor monto')
docMaxMonto = pagos.groupby(['co_tipo_doc'])[['mont_doc']].sum()
print(docMaxMonto['mont_doc'].idxmax())
print(docMaxMonto['mont_doc'].max())

technologies  = ({
    'Courses':["Spark","PySpark","Hadoop","Python","Pandas","Hadoop","Spark","Python"],
    'Fee' :[22000,25000,23000,24000,26000,25000,25000,22000],
    'Duration':['30days','50days','55days','40days','60days','35days','55days','50days'],
    'Discount':[1000,2300,1000,1200,2500,1300,1400,1600]
                })
df = pd.DataFrame(technologies, columns=['Courses','Fee','Duration','Discount'])
print(df)

# Use GroupBy() to compute the sum
df2 = df.groupby('Courses').sum()
print(df2)

# Using GroupBy multiple column
df2 = df.groupby(['Courses','Duration'])['Fee'].sum()
print(df2)

# Groupby and get sum() and count()
df2 = df.groupby('Courses')['Fee'].agg(['sum','count'])
print(df2)

# Pandas groupby get sum() and count()
df2 = df.groupby('Courses').agg({'Fee': ['sum','count']})
print(df2)

# Remove sorting on grouped results
df2=df.groupby(by=['Courses'], sort=False).sum()
print(df2)

# Sorting group keys on descending order
groupedDF = df.groupby('Courses',sort=False).sum()
sortedDF=groupedDF.sort_values('Courses', ascending=False)
print(sortedDF)

# Using as_index=False
df2 = df.groupby('Courses', as_index =False)['Fee'].sum()

# Using reset_index()
df2 = df.groupby(['Courses'])['Fee'].sum().reset_index()
print(df2)

# GroupBy multiple columns using agg()
df2 = df.groupby(['Courses', 'Duration'])['Discount'].agg("sum")
print(df2)

# GroupBy multiple columns using transform()
df2 = df.groupby(['Courses', 'Fee'])['Discount'].transform('sum')
print(df2)

print("pivot(columns=['Courses', 'Duration'])")
# GroupBy multiple columns using pivot function
df2 = df.groupby(['Courses', 'Duration'], as_index=False).sum().pivot(columns=['Courses', 'Duration']).fillna(0)
print(df2)

