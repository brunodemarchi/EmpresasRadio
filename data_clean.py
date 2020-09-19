import pandas as pd
import numpy as np
import json
import ast
import unidecode
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser


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

# transform empty strings into null
df = df.replace('', np.nan)

# remove irrelavant columns
df = df.drop(columns=['extra', 'billing'])

# insert atividade_principal content inside dataframe columns
df['atividade_principal_code'] = df.apply(lambda x: ast.literal_eval(json.loads('"' + str(x.atividade_principal[0]) + '"'))["code"], axis=1)
df['atividade_principal'] = df.apply(lambda x: ast.literal_eval(json.loads('"' + str(x.atividade_principal[0]) + '"'))["text"], axis=1)


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
df['is_ativo'] = df.apply(lambda x: 1 if x.situacao == 'ATIVA' else 0, axis=1)

# clean accents characters because Portuguese is weird
df.motivo_situacao = df.motivo_situacao.apply(lambda x: unidecode.unidecode(x) if type(x) == str else x)

# bool situacao_especial?
df['tem_situacao_especial'] = df.apply(lambda x: 1 if x.situacao_especial != '' else 0, axis=1)

# clean natureza_juridica code/text
df['natureza_juridica_code'] = df.apply(lambda x: x.natureza_juridica.split(' - ')[0], axis=1)
df['natureza_juridica'] = df.apply(lambda x: x.natureza_juridica.split(' - ')[1], axis=1)

# idade empresa (abertura)
df['idade_empresa'] = df.apply(lambda x: relativedelta(datetime.now(), datetime.strptime(x.abertura, '%d/%m/%Y')).years, axis=1)

# atualizado_ultimo_x_meses? update: every company is updated within the last 3 months. Dont know how relevant this information is anymore
df.apply(lambda x: relativedelta(datetime.now(), parser.isoparse(x.ultima_atualizacao).replace(tzinfo=None)).months, axis=1)

# tem_socios?
df["tem_socios"] = df.apply(lambda x: 1 if x.qsa else 0, axis=1)

# socios em lista
def socios_into_list(x):
    list = []
    for socio in x:
        t = socio['nome']
        list.append(t)
    return sorted(list)

df["socios_list"] = df.apply(lambda x: socios_into_list(x.qsa), axis=1)

# numero de socios
df["socios_count"] = df.apply(lambda x: len(x.socios_list), axis=1)


# criar outro df para socios? 
socios = pd.Series([socio for sublist in df.socios_list for socio in sublist]).value_counts() # count how many times these names appear in different socios_list

socios = pd.DataFrame({'socio_name': socios.keys().tolist(), 'empresas_count': socios.values})


# capital social  | edit: ask for help to know what the hell is going on
# maybe irrelevant?

df["capital_social"] = pd.to_numeric(df.capital_social)

# tipo (matriz filial) dummies?
# porte (micro etc) dummies?


df.to_csv('cnpj_clean_data.csv', index=False)
