import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Function to load the metrics results
def load_metrics(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    
    # Extract numerical part from the file name for sorting
    df['file_number'] = df['file'].apply(lambda x: int(re.search(r'(\d+)', x).group()))
    df = df.sort_values(by="file_number").drop(columns=["file_number"])
    return df

# Function to visualize metrics, show averages, and save output
def visualize_and_save_metrics(df, output_folder):
    # Create results folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Set up the figure and axes
    metrics = ["tfidf_similarity", "chrf_score", "rouge_l", "sbert_similarity"]
    num_metrics = len(metrics)
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))  # 2 rows, 2 columns grid
    fig.suptitle("Comparing Translation Similarity Metrics Between XL8 and OpenAI for Korean to Vietnamese Translations", fontsize=16)

    # Plot each metric
    averages = {}
    axes = axes.flatten()  # Flatten axes array for easier iteration
    for i, metric in enumerate(metrics):
        df.plot(x="file", y=metric, kind="bar", ax=axes[i], legend=False)
        axes[i].set_title(f"{metric.replace('_', ' ').capitalize()} (Avg: {df[metric].mean():.4f})")
        axes[i].set_xlabel("File")
        axes[i].set_ylabel("Score")
        axes[i].set_xticklabels(df['file'], rotation=45, ha="right")
        averages[metric] = df[metric].mean()

    # Hide any unused subplot (if the number of metrics is odd)
    if num_metrics < len(axes):
        axes[-1].axis("off")

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)  # Make room for the main title

    # Save the output image
    output_path = os.path.join(output_folder, "metrics_visualization_vi.png")
    plt.savefig(output_path, dpi=300)
    print(f"Visualization saved to: {output_path}")

    # Print the averages
    print("\nAverage Scores:")
    for metric, avg in averages.items():
        print(f"{metric.replace('_', ' ').capitalize()}: {avg:.4f}")

    plt.show()

# Main Execution
if __name__ == "__main__":
    metrics_file = "metrics_results_vi.json"  # Path to the JSON file
    results_folder = "./results"  # Folder to save the visualization

    # Load metrics into a DataFrame
    metrics_df = load_metrics(metrics_file)
    print(metrics_df)  # Display the sorted data table for verification

    # Visualize and save metrics
    visualize_and_save_metrics(metrics_df, results_folder)