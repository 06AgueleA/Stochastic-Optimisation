import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

#The Pure Data from Task 2 (arrival rates)
mu = np.array([0.55, 0.36, 0.09, 0.00])

#The objective function (accepts h as a variable for MCS)
def objective(G, h_val):
    C = np.sum(G) #Total cycle time
    R = C - G #Red time is equal to the lanes own Cycle time minus lanes own green time
    omega = np.zeros(4)
    
    for i in range(4):
        #Wait time formula
        sigma = (mu[i] * R[i] - (G[i] / h_val) - 1.5) * R[i]

        #Non-linear penalty function formula
        if sigma > 0:
            omega[i] = sigma * np.log(sigma)
        else:
            omega[i] = 0
            
    return np.sum(omega)

#Given Boundaries and Constraints -Realistic minimum of 5 green seconds but 0 for exit only lane
bounds = ((5, 150), (5, 150), (5, 150), (0, 150))

# Since R_i + G_i = Total Cycle (C), this is equivalent to 4 * C <= 600
constraints = ({
    'type': 'ineq', 
    'fun': lambda G: 600 - sum([(np.sum(G) - G[i]) + G[i] for i in range(4)])
})

#Starting point to be optimised - Will not change end result
initial_G = [20.0, 20.0, 20.0, 0.0]

#The Monte Carlo Loop
n_simulations = 10000
optimal_greens = []

print(f"Running {n_simulations} Stochastic Optimizations...")

for number in range(n_simulations):
    # Sample h(saturation headway) from a uniform distribution [1.8, 2.2] as per the brief
    h_random = np.random.uniform(1.8, 2.2)
    
    # Run the solver with this specific 'h'
    res = minimize(objective, initial_G, args=(h_random,), 
                   method='SLSQP', bounds=bounds, constraints=constraints)
    
    if res.success:
        optimal_greens.append(res.x) #Appends verison of initial_G which is optimised after minimising wait time

# Process and Visualize Results
df_results = pd.DataFrame(optimal_greens, columns=['North', 'East', 'South', 'West'])

print("\nMONTE CARLO RESULTS (Mean Optimal Green Time)")
print(df_results.mean().round(1))

# Plot the distributions for the report
plt.figure(figsize=(15, 5))
colors = ['blue', 'red', 'green']
active_lanes = ['North', 'East', 'South']

for i, lane in enumerate(active_lanes):
    plt.subplot(1, 3, i+1)
    plt.hist(df_results[lane], bins=40, color=colors[i], alpha=0.7, edgecolor='black')
    plt.title(f'Optimal Green Time Distribuiton: {lane}')
    plt.xlabel('Green Time (s)')
    plt.ylabel('Frequency (Out of 10,000)')
    plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()