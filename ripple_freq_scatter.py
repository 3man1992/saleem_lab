# Custom Libaries
from utils.meta_data import Meta
from sharp_wave_ripple_analysis import ripple_frequency_analysis_scatter as freq

# Os Libaries
import matplotlib.pyplot as plt

# Load data
sessions = list(Meta().dictionary.keys())

# Loop over sessions
pre_frequency_counts = []
post_frequency_counts = []

for session in sessions:
    pre_ripples_path = Meta().dictionary[session]['pre']
    post_ripples_path = Meta().dictionary[session]['post']
    pre_centers = freq.find_center_ripple(pre_ripples_path)
    post_centers = freq.find_center_ripple(post_ripples_path)
    pre_frequency_counts.append(freq.avg_calc_ripples_per_minute(pre_centers))
    post_frequency_counts.append(freq.avg_calc_ripples_per_minute(post_centers))

# Plot scatter
plt.scatter(pre_frequency_counts[:-2], post_frequency_counts[:-2], label = 'Light conditions')
plt.scatter(pre_frequency_counts[-2:], post_frequency_counts[-2:], label = 'Dark conditions')
plt.plot([0, 30], [0, 30], color='k', linestyle='dashed')
plt.title('Average number of SWRs per minute', fontsize=20)
plt.legend()
plt.xlabel('Sleep Session \n Pre-Task')
plt.ylabel('Sleep Session \n Post-Task')
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.show()
