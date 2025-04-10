from torchreid.utils import FeatureExtractor
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

extractor = FeatureExtractor(model_name='osnet_x1_0', model_path=None, device='cpu')

def extract_features(crop_paths):
    return extractor(crop_paths)

def match_features(features_a, features_b, threshold=0.75):
    matches = []
    similarities = cosine_similarity(features_a, features_b)
    for i, row in enumerate(similarities):
        best_j = np.argmax(row)
        score = row[best_j]
        if score >= threshold:
            matches.append({
                "a_index": i,
                "b_index": best_j,
                "similarity": round(float(score), 2)
            })
    return matches
