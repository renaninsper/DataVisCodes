import matplotlib.pyplot as plt

# Dados do gráfico
sizes = [98, 70, 45]
labels = ['A', 'B', 'C']
cores = ['#ccccff', '#f2ccff', '#ffcce6']

# Criar uma figura
fig, ax = plt.subplots()

# Plotar o gráfico de pizza
ax.pie(sizes, labels=labels, autopct='%1.1f%%',
       textprops={'fontsize': 12, 'fontweight': 'bold', 'fontname':'Bahnschrift'}
       ,colors=cores, wedgeprops={'edgecolor': 'gray'})

# Adicionar um círculo no centro para criar o buraco
centre_circle = plt.Circle((0,0),0.70,fc='white', edgecolor='gray',linewidth=1)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Ajustar o aspecto da figura para que seja um círculo
ax.axis('equal')  

# Mostrar o gráfico
plt.tight_layout()
plt.show()