import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'output.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Process the data
data['Score'] = data['Score'].str.replace(',', '').astype(float)
data['Accuracy'] = data['Score'] / 1000000

# Convert 'Timestamp' to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Filter out Grade 'E' data points
grade_e_data = data[data['Grade'] == 'E']
filtered_data = data[data['Grade'] != 'E']

# Calculate average accuracy for all data, excluding Grade 'E'
average_accuracy = filtered_data.groupby('Difficulty Level')['Accuracy'].mean().reset_index()

# Filter data for the last month
last_month_data = filtered_data[filtered_data['Timestamp'] >= (filtered_data['Timestamp'].max() - pd.DateOffset(months=1))]

# Calculate average accuracy for the last month
last_month_average = last_month_data.groupby('Difficulty Level')['Accuracy'].mean().reset_index()

# Plot the individual data points (excluding Grade 'E') in gray
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['Difficulty Level'], filtered_data['Accuracy'], color='gray', alpha=0.5, s=50, label='Individual Data Points')

# Plot the average accuracy line
plt.plot(average_accuracy['Difficulty Level'], average_accuracy['Accuracy'], marker='o', linestyle='-', linewidth=2, label='Overall Average Accuracy')

# Plot the last month's average accuracy line in purple
plt.plot(last_month_average['Difficulty Level'], last_month_average['Accuracy'], marker='o', linestyle='--', linewidth=2, color='purple', label='Last Month Average Accuracy')

# Plot the excluded Grade 'E' data points with red Xs at 30% opacity
plt.scatter(grade_e_data['Difficulty Level'], grade_e_data['Accuracy'], alpha=0.3, color='red', marker='x', s=100, label='Grade E (Excluded)')

# Add title, labels, and legend
plt.title('Accuracy Over Difficulty Level (Excluding Grade E)', fontsize=14)
plt.xlabel('Difficulty Level', fontsize=12)
plt.ylabel('Accuracy (%)', fontsize=12)
plt.grid(True)
plt.xticks(sorted(data['Difficulty Level'].unique()))
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
