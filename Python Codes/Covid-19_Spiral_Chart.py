import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime, timedelta

# Leitura e tratamento dos dados
owid_url = "https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true"
country = "United States"
covid = pd.read_csv(owid_url)
covid['date'] = pd.to_datetime(covid['date'])
covid_cases = covid[(covid['location'] == country) & (covid['date'] <= '2023-05-31')]
covid_cases = covid_cases[['date', 'new_cases', 'new_cases_smoothed']].sort_values('date')
start_date = pd.to_datetime("2020-01-01")
end_date = covid_cases['date'].max()
date_range = pd.date_range(start_date, end_date)
covid_cases = covid_cases.set_index('date').reindex(date_range).fillna(0)
covid_cases['day_of_year'] = covid_cases.index.dayofyear
covid_cases['year'] = covid_cases.index.year

# Diagramação
size_factor = 1400
outline_color = "#D97C86"
fill_color = "#F0C0C1"
base_grey = "grey"

# Convert day_of_year to radians
theta = covid_cases['day_of_year'] / 365 * 2 * np.pi #+ np.pi * 365/2

# Create a figure and polar axes
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# Set the starting angle to January
ax.set_theta_zero_location('N')

# Define a direção do theta para anti-horário 
ax.set_theta_direction(-1)  

# Plot the data
ax.plot(theta, covid_cases.index.values, color='black', linewidth=0.5)

# Aplica dados ao gráfico espiral
ax.fill_between(theta, 
    covid_cases.index.values - pd.to_timedelta(covid_cases['new_cases_smoothed'].astype(int)/(2 * size_factor),unit='D'),
    covid_cases.index.values + pd.to_timedelta(covid_cases['new_cases_smoothed'].astype(int)/(2 * size_factor),unit='D'),
    color=fill_color, edgecolor=outline_color, linewidth=0.3)

ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))  # Define os ticks do eixo theta
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])  # Define os rótulos do eixo theta
ax.tick_params(axis='x', pad=15)  # Ajusta a distância dos rótulos do eixo theta

# Remove axis lines, ticks, and labels
ax.spines['polar'].set_visible(False)
ax.set_yticks([]) 

# Show the plot
plt.show()