import chromadb
from chromadb.config import Settings as ChromaSettings

chroma_client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=ChromaSettings(anonymized_telemetry=False)
)

notes_collection = chroma_client.get_or_create_collection("notes")
tickets_collection = chroma_client.get_or_create_collection("tickets")

def index_note(note_id: int, title: str, body: str, tags: str):
    doc = f"{title}\n{tags}\n{body}"
    notes_collection.upsert(
        documents=[doc],
        ids=[f"note_{note_id}"],
        metadatas=[{"note_id": note_id, "title": title, "tags": tags}]
    )

def index_ticket(ticket_id: int, title: str, description: str, resolution: str):
    doc = f"{title}\n{description}\nResolution: {resolution}"
    tickets_collection.upsert(
        documents=[doc],
        ids=[f"ticket_{ticket_id}"],
        metadatas=[{"ticket_id": ticket_id, "title": title}]
    )

def search_notes(query: str, n: int = 3) -> list:
    results = notes_collection.query(query_texts=[query], n_results=min(n, notes_collection.count() or 1))
    return results.get("metadatas", [[]])[0]

def search_tickets(query: str, n: int = 3) -> list:
    results = tickets_collection.query(query_texts=[query], n_results=min(n, tickets_collection.count() or 1))
    return results.get("metadatas", [[]])[0]

def delete_note(note_id: int):
    try:
        notes_collection.delete(ids=[f"note_{note_id}"])
    except Exception:
        pass

def delete_ticket(ticket_id: int):
    try:
        tickets_collection.delete(ids=[f"ticket_{ticket_id}"])
    except Exception:
        pass
