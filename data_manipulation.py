import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

pd.read_csv('cnpj_clean_data.csv')

# get situacao dummies
df = pd.get_dummies(df, columns=['situacao'])
df.corr()
plt.subplots(figsize=(12, 9))
sns.heatmap(df.corr(), vmax=.8, square=True);



# motivo not_ativo plot bar? 
df[df.motivo_situacao != ''].motivo_situacao.value_counts().plot.bar()



# idade_empresa

def group_by_step(value, step_size = 5, separator = '-'):    
    if(value == 0): return "0"+separator+str(step_size)    
    value = value-1 if(value % step_size == 0) else value
    value = (value // step_size) * step_size
    start = value if(value == 0) else value+1
    range = str(start) + separator + str(value + step_size)    
    return range

df.idade_empresa.apply(lambda x: group_by_step(x)).value_counts().sort_index(key=lambda x: x.str.split('-').str[0].astype(int)).plot.bar()
df.idade_empresa.hist()
df.idade_empresa.value_counts()

# norte? sul? plot map?
df['possui_endereco'] = df.apply(lambda x: 0 if x.uf == '' else 1, axis=1)
df.uf.value_counts()
df.idade_empresa.hist()
df.idade_empresa.hist(bins=50)
df[df.is_ativo == True].shape[0] / df.shape[0]
df[df.is_ativo == False].shape[0] / df.shape[0]
df.is_ativo.value_counts().plot.pie()