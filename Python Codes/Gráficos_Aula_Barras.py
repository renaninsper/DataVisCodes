import matplotlib.pyplot as plt

# Dados para o gráfico
categorias = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
valores = [20, 35, 48, 53, 60, 62, 70]
cores = ['#ccccff', '#d9ccff', '#e6ccff', '#f2ccff', '#ffccff', '#ffccf2', '#ffcce6']

# Criando a figura e os eixos
fig, ax = plt.subplots()

# Definindo a cor de fundo da área de plotagem (eixo)
ax.set_facecolor('#ffffff')

# Configurando o fundo da figura (fora do eixo)
fig.patch.set_facecolor('#ffffff')

# Criando o gráfico de barras com cores diferentes para cada categoria
plt.bar(categorias, valores, color=cores, width=0.9, edgecolor='gray', linewidth=0.5)

# Acessando as bordas da grade e alterando a cor
plt.gca().spines['bottom'].set_color('lightgray')
plt.gca().spines['left'].set_color('lightgray')
plt.gca().spines['top'].set_color('lightgray')
plt.gca().spines['right'].set_color('lightgray')

# Remover bordas da grade
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Alterando a cor dos números nos eixos x e y
ax.tick_params(axis='x', colors='#8a8a5c')
ax.tick_params(axis='y', colors='#8a8a5c')

# Configurações do título e rótulos dos eixos
ax.set_xlabel('Categorias', fontname='Bahnschrift', fontsize=12, color='#3d3d29')
ax.set_ylabel('Valores', fontname='Bahnschrift', fontsize=12, color='#3d3d29')

# Adicionando o subtítulo e título
plt.suptitle('GRÁFICO DE BARRA', fontname='Bahnschrift', fontsize=14, color='#1f1f14')
plt.title('Subtítulo', fontname='Bahnschrift', fontsize=12, color='#5c5c3d')

# Adicionando os valores do eixo y em cada barra
for i in range(len(categorias)):
    ax.text(i, valores[i] + 1, str(valores[i]), ha='center', fontname='Bahnschrift', fontsize=10, color='#3d3d29')

# Mudando a fonte das etiquetas do eixo x e y para Bahnschrift
plt.xticks(fontname='Bahnschrift', fontsize=10)
plt.yticks(fontname='Bahnschrift', fontsize=10)

# Mostrando o gráfico
plt.show()
