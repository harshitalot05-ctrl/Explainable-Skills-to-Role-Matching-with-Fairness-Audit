from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the pre-trained semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, role_text):

    resume_embedding = model.encode([resume_text])
    role_embedding = model.encode([role_text])

    similarity = cosine_similarity(
        resume_embedding,
        role_embedding
    )[0][0]

    score = similarity * 100

    return round(score, 2)