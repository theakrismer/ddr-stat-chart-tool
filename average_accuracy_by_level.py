import pandas as pd
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime

def load_and_process_data(file_path):
    """
    Loads and processes the CSV data for a single player.
    """
    # Extract player name from the filename
    player_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Load the CSV
    data = pd.read_csv(file_path)
    
    # Process the data
    data['Score'] = data['Score'].str.replace(',', '').astype(float)
    data['Accuracy'] = data['Score'] / 1000000
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y-%m-%d %I:%M %p', errors='coerce')
    data['Player'] = player_name  # Add player name column
    
    return data

def main(file1, file2=None, last_month_only=False):
    # Load and process the first file
    player1_data = load_and_process_data(file1)
    
    # Load and process the second file, if provided
    if file2:
        player2_data = load_and_process_data(file2)
        data = pd.concat([player1_data, player2_data], ignore_index=True)
    else:
        data = player1_data
    
    # Filter out Grade 'E' data points
    filtered_data = data[data['Grade'] != 'E']
    
    # Filter data for the last month if the flag is set
    if last_month_only:
        one_month_ago = datetime.now() - pd.DateOffset(months=1)
        filtered_data = filtered_data[filtered_data['Timestamp'] >= one_month_ago]
    
    # Calculate average accuracy for all data
    average_accuracy = filtered_data.groupby(['Player', 'Difficulty Level'])['Accuracy'].mean().reset_index()
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    
    # Define a color map for players
    color_map = {player: color for player, color in zip(filtered_data['Player'].unique(), plt.cm.tab10.colors)}

    # Plot individual data points for each player
    for player in filtered_data['Player'].unique():
        player_data = filtered_data[filtered_data['Player'] == player]
        plt.scatter(
            player_data['Difficulty Level'], 
            player_data['Accuracy'], 
            alpha=0.5, 
            s=50, 
            color=color_map[player], 
            label=f'{player} - Individual Data'
        )

    # Plot average accuracy lines for each player
    for player in average_accuracy['Player'].unique():
        player_avg = average_accuracy[average_accuracy['Player'] == player]
        plt.plot(
            player_avg['Difficulty Level'], 
            player_avg['Accuracy'], 
            marker='o', 
            linestyle='-', 
            linewidth=2, 
            color=color_map[player], 
            label=f'{player} - Average Accuracy'
        )

    # Add title, labels, and legend
    title = 'Accuracy Over Difficulty Level (Last Month)' if last_month_only else 'Accuracy Over Difficulty Level (All Data)'
    plt.title(title, fontsize=14)
    plt.xlabel('Difficulty Level', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    plt.grid(True)
    plt.xticks(sorted(data['Difficulty Level'].unique()))
    plt.legend()
    plt.tight_layout()
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Example usage: python script.py player1.csv player2.csv --last-month
    if len(sys.argv) < 2:
        print("Usage: python script.py <file1.csv> [file2.csv] [--last-month]")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
    last_month_only = "--last-month" in sys.argv
    main(file1, file2, last_month_only)
