import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Function to load the metrics results
def load_metrics(json_file, label):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    df['source'] = label  # Add a 'source' column to identify the source
    return df

# Function to visualize metrics, show averages, and save output
def visualize_and_save_metrics(dfs, output_folder):
    # Create results folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Set up the figure and axes
    metrics = ["tfidf_similarity", "chrf_score", "rouge_l", "sbert_similarity"]
    languages = ["Vietnamese", "Thai"]
    colors = ['#1f77b4', '#ff7f0e']  # Different colors for each source

    for language in languages:
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))  # 2 rows, 2 columns grid
        fig.suptitle(f"Comparing Translation Similarity Metrics Between 10 Seconds Segmentation and Full length for {language}", fontsize=16)

        # Filter DataFrames for the current language
        language_dfs = [(df, label) for df, label in dfs if language in label]

        # Plot each metric
        axes = axes.flatten()  # Flatten axes array for easier iteration
        for i, metric in enumerate(metrics):
            for j, (df, label) in enumerate(language_dfs):
                axes[i].bar(label, df[metric].values[0], color=colors[j], alpha=0.7, label=label if i == 0 else "")
            axes[i].set_title(f"{metric.replace('_', ' ').capitalize()}")
            axes[i].set_xlabel("Translation Source")
            axes[i].set_ylabel("Score")
            if i == 0:
                axes[i].legend(loc="upper right")

        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)  # Make room for the main title

        # Save the output image
        output_path = os.path.join(output_folder, f"{language.lower()}_metrics_visualization.png")
        plt.savefig(output_path, dpi=300)
        print(f"Visualization saved to: {output_path}")

        # Print the averages
        print(f"\nAverage Scores for {language}:")
        for metric in metrics:
            for df, label in language_dfs:
                print(f"{metric.replace('_', ' ').capitalize()} ({label}): {df[metric].mean():.4f}")

        plt.show()

# Main Execution
if __name__ == "__main__":
    # Paths to the JSON files
    metrics_files = {
        "XL8 Vietnamese": "full-duration-output/translate-xl8-vi/metrics_results.json",
        "XL8 Thai": "full-duration-output/translate-xl8-th/metrics_results.json",
        "OpenAI Vietnamese": "full-duration-output/translate-openai-vi/metrics_results.json",
        "OpenAI Thai": "full-duration-output/translate-openai-th/metrics_results.json"
    }
    results_folder = "./results"  # Folder to save the visualization

    # Load metrics into DataFrames
    dfs = [(load_metrics(file, label), label) for label, file in metrics_files.items()]

    # Visualize and save metrics
    visualize_and_save_metrics(dfs, results_folder)