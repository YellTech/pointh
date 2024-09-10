import matplotlib.pyplot as plt
import numpy as np

# Dados de exemplo
categories = ['Horas Estimadas']
horas_esperadas = np.array([220])
horas_cumpridas = np.array([209])

# Criar o gráfico de barras empilhadas
fig, ax = plt.subplots(figsize=(10, 6))

# Plotar as barras empilhadas
bar_width = 0.4
index = np.arange(len(categories))

bars2 = ax.bar(index, horas_esperadas, bar_width, label='Horas Esperadas', color='blue')
bars1 = ax.bar(index, horas_cumpridas, bar_width, bottom=horas_esperadas, label='Horas Cumpridas', color='green')

# Adicionar título e rótulos
ax.set_xlabel('Funcionários')
ax.set_ylabel('Horas')
ax.set_title('Horas Esperadas e Cumpridas')
ax.set_xticks(index)
ax.set_xticklabels(categories)
ax.legend()

# Adicionar rótulos de valor em cada barra
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom')

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2.0, height + bar.get_y(), f'{height}', ha='center', va='bottom')

# Exibir o gráfico
plt.tight_layout()
plt.show()
