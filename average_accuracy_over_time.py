import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def process_and_plot(file1, file2=None, show_fail=True):
    def load_and_process_data(file_path):
        # Load the CSV file
        data = pd.read_csv(file_path)
        
        # Process the data
        data['Score'] = data['Score'].str.replace(',', '').astype(float)
        data['Accuracy'] = data['Score'] / 1000000
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Convert 'Timestamp' to datetime
        
        # Separate "E" grade data
        grade_e_data = data[data['Grade'] == 'E']
        filtered_data = data[data['Grade'] != 'E']
        
        # Group the data biweekly
        filtered_data['Biweekly'] = filtered_data['Timestamp'].dt.to_period('2W').dt.start_time
        average_accuracy_biweekly = filtered_data.groupby('Biweekly')['Accuracy'].mean().reset_index()
        
        return filtered_data, grade_e_data, average_accuracy_biweekly

    # Determine player names based on file names
    player1_name = os.path.splitext(os.path.basename(file1))[0]
    player2_name = os.path.splitext(os.path.basename(file2))[0] if file2 else None

    # Load and process data for each file
    filtered_data1, grade_e_data1, avg_acc_biweekly1 = load_and_process_data(file1)
    if file2:
        filtered_data2, grade_e_data2, avg_acc_biweekly2 = load_and_process_data(file2)

    # Plot data
    plt.figure(figsize=(12, 6))
    
    # Plot data for player 1
    plt.scatter(filtered_data1['Timestamp'], filtered_data1['Accuracy'], color='blue', alpha=0.5, s=50, label=f'{player1_name} Data Points')
    plt.plot(avg_acc_biweekly1['Biweekly'], avg_acc_biweekly1['Accuracy'], marker='o', linestyle='-', color='blue', linewidth=2, label=f'{player1_name} Average (Biweekly)')
    if show_fail:
        plt.scatter(grade_e_data1['Timestamp'], grade_e_data1['Accuracy'], color='blue', alpha=0.3, marker='x', s=100, label=f'{player1_name} Grade E (Excluded)')

    if file2:
        # Plot data for player 2
        plt.scatter(filtered_data2['Timestamp'], filtered_data2['Accuracy'], color='green', alpha=0.5, s=50, label=f'{player2_name} Data Points')
        plt.plot(avg_acc_biweekly2['Biweekly'], avg_acc_biweekly2['Accuracy'], marker='o', linestyle='-', color='green', linewidth=2, label=f'{player2_name} Average (Biweekly)')
        if show_fail:
            plt.scatter(grade_e_data2['Timestamp'], grade_e_data2['Accuracy'], color='green', alpha=0.3, marker='x', s=100, label=f'{player2_name} Grade E (Excluded)')

    # Add title, labels, and legend
    plt.title('Comparison of Average Accuracy Over Time (Biweekly)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Show the plot
    plt.show()

# Main script execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file1.csv> [<file2.csv>] [--no-fail]")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    show_fail = '--no-fail' not in sys.argv

    process_and_plot(file1, file2, show_fail)
