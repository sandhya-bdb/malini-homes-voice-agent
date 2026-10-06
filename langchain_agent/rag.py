import sys

from langchain_groq import ChatGroq
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from config import settings


def retrieve(
    client: QdrantClient,
    embedder: SentenceTransformer,
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """Embed the query and return the top-k most similar chunks from Qdrant."""
    query_vector = embedder.encode(query).tolist()

    hits = client.query_points(
        collection_name=settings.collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )

    return [{**hit.payload, "score": round(hit.score, 4)} for hit in hits.points]


def build_context(retrieved_chunks: list[dict]) -> str:
    """Build a context string from retrieved chunks."""
    parts = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        parts.append(f"[Source {i}]\n{chunk['chunk_text']}")
    return "\n\n---\n\n".join(parts)


def rag(query: str, top_k: int = 5, client=None, embedder=None):
    """
    End-to-end RAG pipeline:
      1. Retrieve relevant chunks from Qdrant
      2. Format as context
      3. Send context + query to Groq LLM

    Returns:
        tuple: (answer_text, context_used)
    """
    if embedder is None:
        embedder = SentenceTransformer(settings.embedding_model)
    if client is None:
        client = QdrantClient(path=settings.qdrant_path)

    # Step 1 — Retrieve
    chunks = retrieve(client, embedder, query, top_k=top_k)
    if not chunks:
        return (
            "I couldn't find specific information about that in our Malini Homes documentation. "
            "Could you rephrase your question or ask about our properties, room rates, or amenities?",
            "",
        )

    # Step 2 — Build context
    context = build_context(chunks)

    # Step 3 — Generate answer
    system_prompt = (
        "You are Malini Voice, a warm, helpful homestay customer assistant for Malini Homes in Guwahati, Assam.\n"
        "Answer the guest's question using ONLY the context provided below.\n"
        "If the context does not contain enough information, politely say so — do not make things up.\n"
        "Always mention the relevant property name (Silpukhuri, Zoo Road, or Bhangagarh) when answering.\n"
        "Keep responses brief, polite, and conversational for voice calls "
        "(1 to 2 sentences max).\n"
        "Format any prices with ₹ symbol and specify rates per night."
    )

    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    llm = ChatGroq(
        model=settings.groq_model,
        temperature=0.2,
    )
    messages = [
        ("system", system_prompt),
        ("user", user_message),
    ]

    response = llm.invoke(messages)
    return response.content, context


def main():
    """CLI interface for testing RAG independently."""
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "What properties and rooms does Malini Homes offer in Guwahati?"

    print(f"Question: {query}\n")
    print("Generating answer...\n")

    answer, context = rag(query)

    print(f"ANSWER:\n{answer}")
    print(f"\n{'='*60}")
    print(f"\nSOURCES:\n{context}")


if __name__ == "__main__":
    main()
