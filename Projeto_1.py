import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime as dt
from mpl_toolkits.mplot3d import Axes3D


dataframe = pd.read_csv("D:\Downloads\Arquivos Contauto\LPAA\Health_AnimalBites.csv")

##################################### TRATAMENTO DE DADOS #########################################################################################################################################################################################

formato = "%Y-%m-%d %H:%M:%S"

# Fazendo a limpeza de colunas(caracteristicas que serão abordadas) onde tem muitos NAN, a planilha tem 9000 linhas, caso uma coluna tenha mais de 7000 NAN ela será descartada
for coluns in dataframe.columns :
    if dataframe[coluns].isna().sum() > 7000 :
        dataframe = dataframe.drop(coluns, axis=1)

# Fazendo limpeza nas linhas(elementos abordados) caso a linha tenha um NAN na coluna onde diz o tipo de animal ou a data do acontecimento, ela será excluida
# Pelos motivos que, o animal é o objeto mais importante deste data frame no meu entedimento e se não tiver a data da mordida, seria uma data incerta
# Que pode ter acontecido a muito tempo antes ou muito tempo depois dos dados analisados, que no meu entedimento é um dado que irá atrapalha
# 
# Caso o dado seja de antes dos anos 2000, não é interessante pelo mesmo motivo de tirar os dados que tem NAN da coluna da data de acontecimento 
for indice, lines in dataframe.iterrows() :
    if pd.isna(dataframe.loc[indice,'SpeciesIDDesc']) or pd.isna(dataframe.loc[indice,'bite_date']) or int(dataframe.loc[indice,'bite_date'][0:4]) < 2008 or int(dataframe.loc[indice,'bite_date'][0:4]) > 2017 :
        dataframe = dataframe.drop(indice)
# Re-indexando o dataframe para ter os indexadores certos
dataframe = dataframe.reset_index(drop=True)

###################################################################################################################################################################################################################################################################

##################################### ANALISE DE DADOS ####################################################################################################################################################

bite_without_vacination = {};bite_with_vacination  = {};animal = {}; gen = {}; data_time_bite_month_B = {}; where_Bitten = {}

# começando a analise de dados, começo analisando o
for indice, lines in dataframe.iterrows() :
    ## Dados que estou analisando das linhas
    data_gen = dataframe.loc[indice, 'GenderIDDesc']
    data_animal = dataframe.loc[indice, 'SpeciesIDDesc']
    data_time_bite = dataframe.loc[indice, 'bite_date']
    data_where_bite = dataframe.loc[indice, 'WhereBittenIDDesc']
    data_vacination_day = dataframe.loc[indice, 'vaccination_date']
    data_type_dog = dataframe.loc[indice, 'BreedIDDesc']

    if pd.isna(data_where_bite) :
        data_where_bite = 'UNKNOWN'
    if data_where_bite in where_Bitten :
        where_Bitten[data_where_bite] = where_Bitten[data_where_bite] + 1
    else :
        where_Bitten[data_where_bite] = 1

    data_time_bite = dt.strptime(data_time_bite, formato)
    ano_mes = '%Y=%m'
    data_time_bite_month = data_time_bite.strftime('%Y-%m')

    # Biblioteca mordidas por Ano e Mês
    if data_time_bite_month in data_time_bite_month_B :
        data_time_bite_month_B[data_time_bite_month] = data_time_bite_month_B[data_time_bite_month] + 1
    else :
        data_time_bite_month_B[data_time_bite_month] = 1



    # Analisando a data de vacinação
    if not(pd.isna(data_vacination_day)) and not(pd.isna(data_type_dog)) :
        date_time_vacination = dt.strptime(data_vacination_day, formato)
        if data_time_bite < date_time_vacination :
            if data_type_dog in bite_with_vacination :
                bite_with_vacination[data_type_dog] = bite_with_vacination[data_type_dog] + 1
            else :
                bite_with_vacination[data_type_dog] = 1
        else :
            if data_type_dog in bite_without_vacination :
                bite_without_vacination[data_type_dog] = bite_without_vacination[data_type_dog] + 1
            else :
                bite_without_vacination[data_type_dog] = 1
        

    # Biblioteca para genero
    if pd.isna(data_gen) :
        data_gen = 'UNKNOWN'
    if data_gen in gen :
        gen[data_gen] = gen[data_gen] + 1
    else :
        gen[data_gen] = 1

    # Biblioteca para cada animal
    if data_animal in animal :
        animal[data_animal] = animal[data_animal] + 1
    else :
        animal[data_animal] = 1

generos = list(gen.values())
animais = list(animal.values())
Animais_Keys = list(animal.keys())
Mordida_Onde = list(where_Bitten.values())


labels_a2 = [f'{Animais_Keys[1]} ({animais[1]})',f'{Animais_Keys[0]} ({animais[0]})']
cores_a2 = ['green','gray']

labels_a = [f'{Animais_Keys[2]} ({animais[2]})',f'{Animais_Keys[3]} ({animais[3]})'
          ,f'{Animais_Keys[4]} ({animais[4]})',f'{Animais_Keys[5]} ({animais[5]})',f'{Animais_Keys[6]} ({animais[6]})',
          f'{Animais_Keys[7]} ({animais[7]})',f'{Animais_Keys[8]} ({animais[8]})']

animais = animais[2:]

labels_g = [f'female({generos[0]})',f'male ({generos[1]})',f'unknown ({generos[2]})']
cores_g = ['blue','red','gray']

labels_where = [f'BODY({Mordida_Onde[0]})',f'HEAD({Mordida_Onde[1]})',f'UNKNOWN({Mordida_Onde[2]})']

fig = plt.figure(figsize=(10,10))

# Plote de mordidas por gênero
# ax1 = fig.add_subplot(1,1,1)
# ax1.set_title('Mordidas por Gênero')
# ax1 = plt.pie(generos, labels=labels_g, colors=cores_g, autopct='%1.1f%%')


# Plote de mordidas por animal incomuns
# ax2 = fig.add_subplot(1,1,1)
# ax2.set_title('Mordidas por Animais')
# ax2 = plt.bar(labels_a, animais)


# Plote de mordidas por animal comuns
# ax3 = fig.add_subplot(1,1,1)
# ax3.set_title('Modidas por Animais Comuns')
# ax3 = plt.pie(animais[0:2], labels=labels_a2, colors=cores_a2, autopct='%1.1f%%')

# Plote de mordidas por local da mordida
# ax4 = fig.add_subplot(1,1,1)
# ax4.set_title('Modidas por Localização da Mordida')
# ax4 = plt.pie(Mordida_Onde, labels=labels_where, colors=cores_g, autopct='%1.1f%%')

# Plote de mordidas vacinadas por raças de cães
plt.plot(list(bite_without_vacination.keys()),list(bite_without_vacination.values()))
plt.xticks(rotation=90, ha='right')


# # Plote para função de quantidade de mordidas X tempo
# # Função de chave para ordenar o dicionário pelas datas
# def chave_ordenacao(data):
#     return (int(data[:4]), int(data[5:]))
# # Ordenar o dicionário pelas datas usando a função sorted e a chave personalizada
# ocorrencias_ordenadas = dict(sorted(data_time_bite_month_B.items(), key=lambda item: chave_ordenacao(item[0])))
# # Gráfico de linha quantidade de mordidas por mês
# plt.plot(list(ocorrencias_ordenadas.keys()),list(ocorrencias_ordenadas.values()), marker='o')
# # Adicionar títulos e rótulos aos eixos
# plt.title('Mordidas X Tempo')
# plt.xlabel('Data')
# plt.ylabel('Quantidade de mordidas')
# # Rotacionar os rótulos do eixo X para melhor visualização
# plt.xticks(rotation=90, ha='right')

# plt.show()

# # Plotar o gráfico de histograma
# plt.hist(list(ocorrencias_ordenadas.values()), bins=20, edgecolor='black')  # O argumento 'bins' define o número de intervalos (bins)

# # Adicionar rótulos aos eixos e título ao gráfico
# plt.xlabel('Mordidas')
# plt.ylabel('Frequência')
# plt.title('Histograma da Quantidade de Mordidas')

plt.show()