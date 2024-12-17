import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util
import sacrebleu

# Load SBERT model
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to read text files
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Metrics
def compute_tfidf_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

def compute_chrf(reference, hypothesis):
    """
    Compute ChrF score using sacrebleu's sentence_chrf function.
    """
    return sacrebleu.sentence_chrf(hypothesis, [reference]).score

def compute_rouge_l(reference, hypothesis):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return scores['rougeL'].fmeasure

def compute_sbert_similarity(text1, text2):
    embeddings = sbert_model.encode([text1, text2], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

# Process Files for Metrics
def evaluate_translations(full_translation_path, merged_translation_path):
    results = []

    full_text = read_text_file(full_translation_path)
    merged_text = read_text_file(merged_translation_path)

    # Compute Metrics
    tfidf_sim = compute_tfidf_similarity(full_text, merged_text)
    chrf = compute_chrf(full_text, merged_text)
    rouge_l = compute_rouge_l(full_text, merged_text)
    sbert_sim = compute_sbert_similarity(full_text, merged_text)

    # Print Results
    print(f"TF-IDF Similarity: {tfidf_sim:.4f}")
    print(f"ChrF Score: {chrf:.4f}")
    print(f"ROUGE-L: {rouge_l:.4f}")
    print(f"SBERT Similarity: {sbert_sim:.4f}\n")

    # Store Results
    results.append({
        "tfidf_similarity": tfidf_sim,
        "chrf_score": chrf,
        "rouge_l": rouge_l,
        "sbert_similarity": sbert_sim
    })

    return results

# Main Execution
if __name__ == "__main__":
    full_translation_path = "full-duration-output/translate-xl8-vi/full_subtitle.txt"
    merged_translation_path = "full-duration-output/translate-xl8-vi/merged_translation.txt"

    # Evaluate translations
    metrics_results = evaluate_translations(full_translation_path, merged_translation_path)

    # Save results to JSON file
    with open("metrics_results.json", "w", encoding="utf-8") as file:
        json.dump(metrics_results, file, ensure_ascii=False, indent=4)

    print("Evaluation completed! Results saved to 'metrics_results.json'.")