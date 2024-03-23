from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from dotenv import load_dotenv
from mpi4py import MPI
import numpy as np
import os


# Get the number of processes
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


# Load the .env file
load_dotenv()
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')



# Load and process the extracted data
extracted_data = []
if rank == 0:
    print(PINECONE_API_KEY)
    print(PINECONE_API_ENV)
    extracted_data = load_pdf("data2/")
    extracted_data = np.array_split(extracted_data, size)
extracted_data = comm.scatter(extracted_data, root=0)
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


#Initializing the Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY,
              environment=PINECONE_API_ENV)

index_name="medical-chatbot"


#Creating Embeddings for Each of The Text Chunks & storing
docsearch=PineconeVectorStore.from_texts(texts=[t.page_content for t in text_chunks], embedding=embeddings, index_name=index_name)
