import matplotlib.pyplot as plt
import numpy as np

# Data from the image
tests = ['Test-math', 'Test-fmath', 'Test-llong', 'Test-printf']
categories = ['Total # of Instructions', 'Load %', 'Store %', 'Uncond branch %', 
              'Cond branch %', 'Integer computation%', 'FP computation%']

alpha_values = [
    [49367, 17.16, 10.43, 3.94, 11.05, 55.38, 1.88],
    [19456, 17.69, 12.55, 4.71, 11.23, 53.24, 0.43],
    [10584, 17.75, 14.66, 5.44, 12.32, 49.54, 0],
    [983430, 17.99, 10.73, 4.82, 11.39, 54.85, 0.01]
]

# Replace with actual Pisa values
pisa_values = [
    [213703, 15.96, 10.67, 4.22, 13.84, 54.52, 0.88],
    [53459, 16.14, 14.43, 4.24, 15.09, 49.95, 0.11],
    [29642,	16.34,	18.02,	4.36,	15.42,	45.81,	0.00],
    [1813891,	19.22,	9.28,	5.13,	17.01,	49.33,	0.01]
]

# Plotting each bar chart for each category
# Plotting each bar chart for each category
for i in range(len(categories)):
    plt.figure(figsize=(10,5))
    y_pos = np.arange(len(tests))
    alpha_data = [alpha_values[j][i] for j in range(len(tests))]
    pisa_data = [pisa_values[j][i] for j in range(len(tests))]
    plt.bar(y_pos - 0.2, alpha_data, 0.4, label='Alpha')
    plt.bar(y_pos + 0.2, pisa_data, 0.4, label='Pisa')
    plt.xticks(y_pos, tests)
    plt.ylabel(categories[i])
    plt.title('Comparison of ' + categories[i] + ' between Alpha and Pisa')
    plt.legend()
    plt.show()

