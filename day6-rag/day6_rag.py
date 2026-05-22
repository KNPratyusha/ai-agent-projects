from groq import Groq
from dotenv import load_dotenv
import os
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─── Step 1: Your "documents" (fake company knowledge base) ───
documents = [
    "Our refund policy allows returns within 30 days of purchase with a valid receipt.",
    "Customer support is available Monday to Friday, 9am to 6pm IST.",
    "We offer free shipping on all orders above Rs 500.",
    "Our premium membership costs Rs 999 per year and includes priority support.",
    "To reset your password, click 'Forgot Password' on the login page.",
    "We accept payments via UPI, credit card, debit card, and net banking.",
]

# ─── Step 2: Set up ChromaDB (vector database) ───
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="company_docs")

# ─── Step 3: Convert documents to embeddings and store them ───
print("Storing documents in vector database...")
model = SentenceTransformer('all-MiniLM-L6-v2')

for i, doc in enumerate(documents):
    embedding = model.encode(doc).tolist()
    collection.add(
        embeddings=[embedding],
        documents=[doc],
        ids=[f"doc_{i}"]
    )

print(f"Stored {len(documents)} documents!")

# ─── Step 4: Ask a question ───
def ask(question):
    print(f"\nQuestion: {question}")
    
    # Convert question to embedding
    question_embedding = model.encode(question).tolist()
    
    # Search for most similar documents
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=2
    )
    
    # Get the relevant chunks
    relevant_docs = results['documents'][0]
    context = "\n".join(relevant_docs)
    print(f"Found relevant docs: {relevant_docs}")
    
    # Send to AI with context
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """Answer questions using ONLY the context provided.
If the answer isn't in the context, say 'I don't have that information.'"""},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    
    print(f"Answer: {response.choices[0].message.content}")

# ─── Step 5: Test it ───
ask("What is your refund policy?")
ask("How much does premium membership cost?")
ask("What payment methods do you accept?")
ask("What is the CEO's name?")  # not in docs — watch what happens!
