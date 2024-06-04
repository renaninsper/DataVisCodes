import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
from adjustText import adjust_text

# Carregar os dados
url = "https://github.com/viniciusoike/restateinsight/raw/main/static/data/gdp-vs-happiness.csv"
owid = pd.read_csv(url)

# Limpando os nomes das colunas e renomeando
dat = owid.rename(columns={
    owid.columns[3]: 'life_satisfaction',
    owid.columns[4]: 'gdppc',
    owid.columns[5]: 'pop'
})

# Filtrando linhas com valores não-nulos para 'gdppc' e 'life_satisfaction'
dat = dat.dropna(subset=['gdppc', 'life_satisfaction'])

# Aplicando log10 para 'gdppc'
dat['gdppc'] = np.log10(dat['gdppc'])

# Filtrando linhas para o último ano disponível para cada entidade
dat = dat.sort_values('Year').groupby('Entity').tail(1)

# Selecionando apenas as colunas desejadas
dat = dat[['Entity', 'pop', 'gdppc', 'life_satisfaction']]

# Obtendo as dimensões do continente
dim_continent = owid[['Entity', 'Continent']].dropna().drop_duplicates()

# Juntando os dados com as dimensões do continente
dat = pd.merge(dat, dim_continent, on='Entity', how='left')

# Criar um conjunto de strings únicas
strings_unicas = dat['Continent'].unique()

# Criar um mapeamento entre as strings únicas e os códigos numéricos
mapeamento = {string: i + 0 for i, string in enumerate(strings_unicas)}

# Função para atribuir o código numérico único para cada string
def atribuir_codigo(texto):
    return mapeamento[texto]

# Aplicar a função à coluna 'texto' e atribuir o resultado à nova coluna 'codigo'
dat['Continent_id'] = dat['Continent'].apply(atribuir_codigo)


# Definir os países a serem destacados
sel_countries = [
    "Brazil", "China", "Russia", "South Africa", "India"
]

# Criar uma coluna para destacar os países selecionados
dat['highlight'] = dat['Entity'].apply(lambda x: x if x in sel_countries else None)

# Definir os países a serem destacados em cinza
sel_countries_2 = [
    "Ireland", "Qatar", "Hong Kong", "Switzerland", "United States", "France",
  "Japan", "Costa Rica", "Turkey", "Indonesia",
  "Iran", "Egypt", "Botswana", "Lebanon", "Philippines", "Bolivia", "Pakistan",
  "Bangladesh", "Nepal", "Senegal", "Burkina Faso", "Ethiopia", "Tanzania",
  "Democratic Republic of Congo", "Mozambique", " Somalia", "Chad", "Malawi",
  "Burundi"
]

# Criar uma coluna para destacar os países selecionados em cinza
dat['highlight_2'] = dat['Entity'].apply(lambda x: x if x in sel_countries_2 else None)


# Define os rótulos do eixo x
xbreaks = [3, 3.3, 3.7, 4, 4.3, 5]
xlabels = ['$1,000', '$2,000', '$5,000', '$10,000', '$20,000', '$100,000']

# Definir cores
colors = ['#4C6A9C', '#A2559C', '#00847E', '#E56E5A', '#883039', '#9A5129']

# Definir fontes
plt.rcParams['font.family'] = 'Bahnschrift'

# Gráfico
fig, ax = plt.subplots(figsize=(16, 9))

# Definindo a cor de fundo da área de plotagem (eixo)
ax.set_facecolor('#FFFFFF')

# Configurando o fundo da figura (fora do eixo)
fig.patch.set_facecolor('#FFFFFF')

# Adicionando pontos para cada país
for index, row in dat.iterrows():
    ax.scatter(row['gdppc'], row['life_satisfaction'], s=(row['pop']/250000), c=colors[row['Continent_id']], alpha=0.8, edgecolors='#A5A9A9', linewidths=0.5, zorder=2)

# Adicionando rótulos para países selecionados 
texts = []
for index, row in dat.iterrows():
    if row['highlight'] is not None:
        texts.append(ax.text(row['gdppc'], row['life_satisfaction'], row['highlight'], c=colors[row['Continent_id']], fontsize=19, ha='center', va='center', zorder=3, bbox=dict(facecolor='white', alpha=0.7, edgecolor='white')))
texts_2 = []
for index, row in dat.iterrows():
    if row['highlight_2'] is not None:
        texts.append(ax.text(row['gdppc'], row['life_satisfaction'], row['highlight_2'], c='lightgray', fontsize=12, ha='center', va='center', zorder=3, ))


# Ajustando os rótulos para evitar sobreposição
adjust_text(texts, expand_text=(1.1, 1.1))
adjust_text(texts_2, expand_text=(1.1, 1.1))

# Grids
plt.grid(True, linestyle=':', color='gray', linewidth=0.5)

# Definindo os limites dos eixos
ax.set_xlim(2.5, 5.5)
ax.set_ylim(2.5, 8)

# Definindo os ticks dos eixos x e y
ax.set_xticks(xbreaks)
ax.set_xticklabels(xlabels)
ax.set_yticks(range(3, 8))

# Adicionando rótulos aos eixos e título/subtítulo
ax.set_xlabel('PIB per capita', fontsize=15, color='#3d3d29')
ax.set_ylabel('Grau de Felicidade (0-10)', fontsize=15, color='#3d3d29')
plt.suptitle('BRICS: RENDA E PERCEPÇÃO DE FELICIDADE', fontname='Bahnschrift', fontsize=25, color='#1f1f14')
plt.title('Felicidade vs. PIB per capita, 2022', fontname='Bahnschrift', fontsize=15, color='#5c5c3d')

# Alterando a cor dos números nos eixos x e y
ax.tick_params(axis='x', colors='#8a8a5c')
ax.tick_params(axis='y', colors='#8a8a5c')

# Removendo as bordas do gráfico
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Adicionando legenda
legend_handles = []
for i, continent in enumerate(dat['Continent'].unique()):
    legend_handles.append(mpatches.Patch(color=colors[i], label=continent))
ax.legend(handles=legend_handles, loc='center right')

# Adicionando anotação
caption = "Brasil é o país mais feliz\n entre os BRICS"
fig.text(0.5, 0.68, caption, ha='center', fontsize=15, color='#8a8a5c')

plt.show()
