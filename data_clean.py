import pandas as pd
import json
import ast
import unidecode
from datetime import datetime
from dateutil.relativedelta import relativedelta

# import cnpj information in string format
df_t = pd.read_csv('cnpj_list.csv')

# create array to transform string into json
matrix = df_t[df_t.columns[0]].to_numpy()
matrix = matrix.flatten()
matrix = matrix.tolist()
json_list = list(map(lambda x: json.loads(x), matrix))

# create dataframe with jsons
df_json = []
for j in json_list:
    df_json.append(pd.DataFrame([j]))
df = pd.concat(df_json, ignore_index=True, sort=False)

# remove cnpjs with status ERROR
df = df[df.status != 'ERROR']

# insert atividade_principal content inside dataframe columns
df['atividade_principal_text'] = df.apply(lambda x: ast.literal_eval(json.loads('"' + str(x.atividade_principal[0]) + '"'))["text"], axis=1)
df['atividade_principal_code'] = df.apply(lambda x: ast.literal_eval(json.loads('"' + str(x.atividade_principal[0]) + '"'))["code"], axis=1)


# bool possui_atividade_secundaria
df['possui_atividade_secundaria'] = df.apply(lambda x: 0 if x.atividades_secundarias[0]['text'] == 'Não informada' else 1, axis=1)

# transform atividades_secundarias into lists
def atividades_secundarias_into_list(x):
    list = []
    for atv in x:
        t = atv['text']
        if t != 'Não informada': list.append(t)
    return sorted(list)


df['atividade_secundaria_list'] = df.apply(lambda x: atividades_secundarias_into_list(x.atividades_secundarias), axis=1)

# bool is_ativo
df.situacao.value_counts()
df['is_ativo'] = df.apply(lambda x: 1 if x.situacao == 'ATIVA' else 0, axis=1)

# clean accents characters because Portuguese is weird
df.motivo_situacao = df.motivo_situacao.apply(unidecode.unidecode)

# motivo not_ativo plot bar? 
df[df.motivo_situacao != ''].motivo_situacao.value_counts().plot.bar()

# bool situacao_especial?
df['tem_situacao_especial'] = df.apply(lambda x: 1 if x.situacao_especial != '' else 0, axis=1)

# clean natureza_juridica code/text
df['natureza_juridica_code'] = df.apply(lambda x: x.natureza_juridica.split(' - ')[0], axis=1)
df['natureza_juridica_text'] = df.apply(lambda x: x.natureza_juridica.split(' - ')[1], axis=1)

# idade empresa (abertura)
df['idade_empresa'] = df.apply(lambda x: relativedelta(datetime.now(), datetime.strptime(x.abertura, '%d/%m/%Y')).years, axis=1)


# norte? sul? etc?




# atualizado_ultimo_x_meses?



# socios em lista
# numero de socios
# tem_socios?

# criar outro df para socios?



# get lat/long? edit: it's impractical for our purposes, since we'd have to use a paid API to do it. Conclusion: do? no