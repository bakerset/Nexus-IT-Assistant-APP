from langchain_community.llms import Ollama
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from agent.system_prompt import SYSTEM_PROMPT
from agent.rag import search_notes, search_tickets
from config import settings

llm = Ollama(
    base_url=settings.ollama_base_url,
    model=settings.ollama_model,
    temperature=0.3,
)

def build_rag_context(message: str) -> str:
    """Search notes and tickets for relevant context to inject."""
    note_hits = search_notes(message, n=3)
    ticket_hits = search_tickets(message, n=2)

    context_parts = []
    if note_hits:
        note_lines = "\n".join([f"- [{h.get('title','')}] (tags: {h.get('tags','')})" for h in note_hits])
        context_parts.append(f"Relevant notes:\n{note_lines}")
    if ticket_hits:
        ticket_lines = "\n".join([f"- [{h.get('title','')}]" for h in ticket_hits])
        context_parts.append(f"Related past tickets:\n{ticket_lines}")

    return "\n\n".join(context_parts)

def chat(message: str, history: list = None) -> str:
    """
    Send a message to Nexus agent and get a response.
    history: list of {"role": "user"|"assistant", "content": "..."}
    """
    rag_context = build_rag_context(message)

    system = SYSTEM_PROMPT
    if rag_context:
        system += f"\n\n## Context from your knowledge base\n{rag_context}"

    # Build prompt manually for Ollama (no native chat history in basic Ollama)
    prompt_parts = [f"System: {system}\n"]
    if history:
        for h in history[-6:]:  # last 6 turns max
            role = "User" if h["role"] == "user" else "Nexus"
            prompt_parts.append(f"{role}: {h['content']}")
    prompt_parts.append(f"User: {message}")
    prompt_parts.append("Nexus:")

    prompt = "\n".join(prompt_parts)

    try:
        response = llm.invoke(prompt)
        return response.strip()
    except Exception as e:
        return f"Agent unavailable: {str(e)}. Make sure Ollama is running (`ollama serve`)."
