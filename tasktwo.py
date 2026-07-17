import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

#Load your data
df = pd.read_csv('traffic_counts.csv')
directions = ['North', 'East', 'South', 'West']

plt.figure(figsize=(15, 10))

# Store mu values (arrival rates) for Task 3
arrival_rates = {}

#Chooses each column from the csv
for i, col in enumerate(directions, 1):
    data = df[col]
    mu = data.mean()
    vn = data.var()
    arrival_rates[col] = mu
    
    # Create subplot
    plt.subplot(2, 2, i)
    
    # Plot empirical histogram (Actual Data)
    #weights = np.ones_like(data) / len(data)
    plt.hist(data, bins=np.arange(data.max() + 2) - 0.5, 
             alpha=0.6, color='skyblue', edgecolor='black', density=True, label='Actual Data')
    
    # Plot theoretical Poisson distribution (The Model, which uses the arrival rate/mean mu)
    x = np.arange(0, data.max() + 1)
    plt.plot(x, poisson.pmf(x, mu), "o-", ms=6, color="0.1", label=f'Poisson (μ={mu:.2f}, σ²={vn:.2f})') #Calculating mean and variance confirms equidispersion
    
    #Graph formatting
    plt.title(f'Arrival Distribution: {col}')
    plt.xlabel('Cars per Second')
    plt.ylabel('Probability')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

#Useful for accessing calcualted mu values directly
print("Calculated Arrival Rates (mu):", arrival_rates)