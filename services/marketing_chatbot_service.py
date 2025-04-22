import os
import re
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from chat.src.helper import download_hugging_face_embeddings
from chat.src.prompt import system_prompt2

def get_response(msg: str) -> str:
    load_dotenv()

    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

    # Initialize embeddings and chain
    embeddings = download_hugging_face_embeddings()
    index_name = "chatbot2"

    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )

    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    llm = ChatGroq(api_key=GROQ_API_KEY, model_name="deepseek-r1-distill-llama-70b")
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt2),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    response = rag_chain.invoke({"input": msg})
    return response["answer"]


async def get_chat_response(msg: str) -> str:
    answer = str(get_response(msg))
    # Remove think tags from response
    cleaned_response = re.sub(r"<think>.*?</think>\s*", "", answer, flags=re.DOTALL)
    return cleaned_response