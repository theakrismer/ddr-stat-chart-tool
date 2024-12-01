import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'output.csv'  # Replace with the actual file path
df = pd.read_csv(file_path)

# Convert the Timestamp column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Sort the data by Timestamp
df = df.sort_values('Timestamp')

# Set the Timestamp as the index for easier resampling
df.set_index('Timestamp', inplace=True)

# Set filtering
fails = df[df['Grade'] == 'E']
passes = df[df['Grade'] != 'E']

# Resample the data to calculate the biweekly average
average_df = passes['Difficulty Level'].resample('2W').mean()



# Plot the original data as unconnected data points

plt.figure(figsize=(12, 6))
plt.scatter(
    passes.index, 
    passes['Difficulty Level'], 
    color='gray', 
    alpha=0.5, 
    label='Original Data Points'
)

# Highlight data points with Grade: E as red 'X'

plt.scatter(
    fails.index, 
    fails['Difficulty Level'], 
    color='red', 
    marker='x', 
    alpha=0.2, 
    s=100,  # Size of the red 'X'
    label='Fail'
)

# Plot the biweekly average as a connected line
plt.plot(
    average_df.index, 
    average_df.values, 
    marker='o', 
    linestyle='-', 
    color='blue', 
    label='Biweekly Average'
)

# Add plot details
plt.title('Biweekly Average of Difficulty Level Over Time')
plt.xlabel('Time')
plt.ylabel('Difficulty Level')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save or display the plot
plt.show()
