from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def rank_abstracts_by_similarity(abstracts, ref_document):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    ref_embedding = model.encode([ref_document])
    abstract_embeddings = model.encode(abstracts)
    similarities = cosine_similarity(ref_embedding, abstract_embeddings)
    return similarities.flatten()
