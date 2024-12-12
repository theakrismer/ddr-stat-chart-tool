import pandas as pd
import matplotlib.pyplot as plt
import sys

def load_and_process_csv(file_path):
    """Load and process a CSV file."""
    df = pd.read_csv(file_path)
    
    # Convert the Timestamp column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Sort the data by Timestamp
    df = df.sort_values('Timestamp')

    # Set the Timestamp as the index for easier resampling
    df.set_index('Timestamp', inplace=True)
    
    return df

def plot_data(file1, file2=None, no_fail=False):
    """Plot data from one or two CSV files."""
    df1 = load_and_process_csv(file1)
    player1_name = file1.split('.')[0]  # Use filename as player name

    if file2:
        df2 = load_and_process_csv(file2)
        player2_name = file2.split('.')[0]

        # Filter data if --no-fail is passed
        if no_fail:
            df1 = df1[df1['Grade'] != 'E']
            df2 = df2[df2['Grade'] != 'E']

        # Resample for biweekly average
        avg1 = df1['Difficulty Level'].resample('2W').mean()
        avg2 = df2['Difficulty Level'].resample('2W').mean()

        # Plot data for Player 1
        plt.scatter(df1.index, df1['Difficulty Level'], color='blue', alpha=0.5, label=f'{player1_name} Data Points')
        plt.plot(avg1.index, avg1.values, marker='o', linestyle='-', color='blue', label=f'{player1_name} Biweekly Average')

        # Highlight fails for Player 1
        if not no_fail:
            fails1 = df1[df1['Grade'] == 'E']
            plt.scatter(fails1.index, fails1['Difficulty Level'], color='blue', marker='x', alpha=0.5, label=f'{player1_name} Fails')

        # Plot data for Player 2
        plt.scatter(df2.index, df2['Difficulty Level'], color='green', alpha=0.5, label=f'{player2_name} Data Points')
        plt.plot(avg2.index, avg2.values, marker='o', linestyle='-', color='green', label=f'{player2_name} Biweekly Average')

        # Highlight fails for Player 2
        if not no_fail:
            fails2 = df2[df2['Grade'] == 'E']
            plt.scatter(fails2.index, fails2['Difficulty Level'], color='green', marker='x', alpha=0.5, label=f'{player2_name} Fails')

    else:
        # Resample for biweekly average
        avg1 = df1[df1['Grade'] != 'E']['Difficulty Level'].resample('2W').mean()

        # Plot data for Player 1
        plt.scatter(df1.index, df1['Difficulty Level'], color='blue', alpha=0.5, label=f'{player1_name} Data Points')
        plt.plot(avg1.index, avg1.values, marker='o', linestyle='-', color='blue', label=f'{player1_name} Biweekly Average')

        # Highlight fails for Player 1
        if not no_fail:
            fails1 = df1[df1['Grade'] == 'E']
            plt.scatter(fails1.index, fails1['Difficulty Level'], color='blue', marker='x', alpha=0.5, label=f'{player1_name} Fails')

    # Add plot details
    plt.title('Biweekly Average of Difficulty Level Over Time')
    plt.xlabel('Time')
    plt.ylabel('Difficulty Level')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python script.py <file1.csv> [<file2.csv>] [--no-fail]")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "--no-fail" else None
    no_fail = "--no-fail" in sys.argv
    
    plot_data(file1, file2, no_fail=no_fail)
