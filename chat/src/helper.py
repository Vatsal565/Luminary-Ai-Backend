from langchain.embeddings import HuggingFaceEmbeddings

#Download the Embeddings from HuggingFace 
def download_hugging_face_embeddings():
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')  #this model return 384 dimensions
    return embeddings