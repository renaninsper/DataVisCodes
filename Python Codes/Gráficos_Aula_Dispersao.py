import matplotlib.pyplot as plt

# Dados para o gráfico
categorias = ['2015', '2016', '2017', '2018', '2019', '2020', '2021']
valores = [20, 35, 48, 53, 60, 62, 70]
valores2 = [21, 25, 39, 45, 71, 60, 69]
valores3 = [78, 70, 45, 34, 46, 24, 19]
cores = ['#ccccff', '#d9ccff', '#e6ccff', '#f2ccff', '#ffccff', '#ffccf2', '#ffcce6']

# Criando a figura e os eixos
fig, ax = plt.subplots()

# Definindo a cor de fundo da área de plotagem (eixo)
ax.set_facecolor('#ffffff')

# Configurando o fundo da figura (fora do eixo)
fig.patch.set_facecolor('#ffffff')

# Criando o gráfico de linha
plt.plot(categorias, valores, marker='o', color=cores[0], linestyle='-', linewidth=2, label='A')
plt.plot(categorias, valores2, marker='o', color=cores[3], linestyle='-', linewidth=2, label='B')
plt.plot(categorias, valores3, marker='o', color=cores[6], linestyle='-', linewidth=2, label='C')

# Adicionando a legenda
plt.legend()

# Plotando grades do gráfico no eixo y
plt.grid(axis='y', color='#e6e6e6')

# Alterando a cor dos números nos eixos x e y
ax.tick_params(axis='x', colors='#8a8a5c')
ax.tick_params(axis='y', colors='#8a8a5c')

# Configurações do título e rótulos dos eixos
ax.set_xlabel('Anos', fontname='Bahnschrift', fontsize=12, color='#3d3d29')
ax.set_ylabel('Valores', fontname='Bahnschrift', fontsize=12, color='#3d3d29')

# Adicionando o subtítulo e título
plt.suptitle('GRÁFICO DE DISPERSÃO COM LINHAS', fontname='Bahnschrift', fontsize=14, color='#1f1f14')
plt.title('Subtítulo', fontname='Bahnschrift', fontsize=12, color='#5c5c3d')

# Acessando as bordas da grade e alterando a cor
plt.gca().spines['bottom'].set_color('lightgray')
plt.gca().spines['left'].set_color('lightgray')
plt.gca().spines['top'].set_color('lightgray')
plt.gca().spines['right'].set_color('lightgray')

# Remover bordas da grade
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
