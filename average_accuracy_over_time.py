import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'output.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Process the data
data['Score'] = data['Score'].str.replace(',', '').astype(float)
data['Accuracy'] = data['Score'] / 1000000
data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Convert 'Timestamp' to datetime

# Exclude grade "E" and separate them
grade_e_data = data[data['Grade'] == 'E']
filtered_data = data[data['Grade'] != 'E']

# Group the data biweekly
filtered_data['Biweekly'] = filtered_data['Timestamp'].dt.to_period('2W').dt.start_time
average_accuracy_biweekly = filtered_data.groupby('Biweekly')['Accuracy'].mean().reset_index()

# Plot original data points (excluding Grade "E") in gray
plt.figure(figsize=(12, 6))
plt.scatter(filtered_data['Timestamp'], filtered_data['Accuracy'], color='gray', alpha=0.5, s=50, label='Individual Data Points')

# Plot average accuracy over time (biweekly)
plt.plot(average_accuracy_biweekly['Biweekly'], average_accuracy_biweekly['Accuracy'], marker='o', linestyle='-', linewidth=2, label='Average Accuracy (Biweekly)')

# Plot excluded Grade "E" data points as red Xs at 30% opacity
plt.scatter(grade_e_data['Timestamp'], grade_e_data['Accuracy'], alpha=0.3, color='red', marker='x', s=100, label='Grade E (Excluded)')

# Add title, labels, and legend
plt.title('Average Accuracy Over Time (Biweekly)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Accuracy (%)', fontsize=12)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
