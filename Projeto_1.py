import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


dataframe = pd.read_csv("D:\Downloads\Arquivos Contauto\LPAA\Health_AnimalBites.csv")

##################################### TRATAMENTO DE DADOS #########################################################################################################################################################################################

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
    if pd.isna(dataframe.loc[indice,'SpeciesIDDesc']) or pd.isna(dataframe.loc[indice,'bite_date']) or int(dataframe.loc[indice,'bite_date'][0:4]) < 2000 :
        dataframe = dataframe.drop(indice)

# Re-indexando o dataframe para ter os indexadores certos
dataframe = dataframe.reset_index(drop=True)

###################################################################################################################################################################################################################################################################

##################################### ANALISE DE DADOS ####################################################################################################################################################

male_num = 0 ;female_num = 0 ;unknown_num = 0; animal = {}; gen = {}

# começando a analise de dados, começo analisando o
for indice, lines in dataframe.iterrows() :
    
    ## Dados que estou analisando das linhas
    data_gen = dataframe.loc[indice, 'GenderIDDesc']
    data_animal = dataframe.loc[indice, 'SpeciesIDDesc']

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

labels_a = [f'{Animais_Keys[2]} ({animais[2]})',f'{Animais_Keys[3]} ({animais[3]})'
          ,f'{Animais_Keys[4]} ({animais[4]})',f'{Animais_Keys[5]} ({animais[5]})',f'{Animais_Keys[6]} ({animais[6]})',
          f'{Animais_Keys[7]} ({animais[7]})',f'{Animais_Keys[8]} ({animais[8]})']

animais = animais[2:]



labels_g = [f'female({generos[0]})',f'male ({generos[1]})',f'unknown ({generos[2]})']
cores_g = ['blue','red','gray']

fig = plt.figure(figsize=(10,10))

ax1 = fig.add_subplot(2,1,1)
ax1.set_title('Mordidas por Gênero')
ax1 = plt.pie(generos, labels=labels_g, colors=cores_g, autopct='%1.1f%%')

ax2 = fig.add_subplot(2,1,2)
ax2.set_title('Mordidas por Animais')
ax2 = plt.bar(labels_a, animais)

plt.tight_layout()
plt.show()
