from datetime import datetime, timedelta
from sqlmodel import Session, select
from models.ticket import Ticket
from models.device import Device
from models.threat import ThreatItem

def get_nudges(session: Session) -> list:
    nudges = []

    # Stale open tickets (open > 3 days)
    cutoff = datetime.utcnow() - timedelta(days=3)
    stale = session.exec(
        select(Ticket).where(Ticket.status == "open").where(Ticket.created_at < cutoff)
    ).all()
    for t in stale:
        days = (datetime.utcnow() - t.created_at).days
        nudges.append({
            "type": "stale_ticket",
            "severity": "warning",
            "message": f"Ticket '{t.title}' has been open for {days} days with no resolution.",
            "link": f"/tickets/{t.id}"
        })

    # Devices past EOL
    today = datetime.utcnow().date()
    devices = session.exec(select(Device)).all()
    for d in devices:
        if d.eol_date and d.eol_date <= today:
            nudges.append({
                "type": "eol_device",
                "severity": "danger",
                "message": f"Device '{d.hostname}' ({d.os}) is past end-of-life ({d.eol_date}).",
                "link": f"/devices/{d.id}"
            })

    # New critical threats (last 48h)
    threat_cutoff = datetime.utcnow() - timedelta(hours=48)
    critical_threats = session.exec(
        select(ThreatItem)
        .where(ThreatItem.relevant == True)
        .where(ThreatItem.severity == "CRITICAL")
        .where(ThreatItem.fetched_at >= threat_cutoff)
    ).all()
    for t in critical_threats:
        nudges.append({
            "type": "critical_threat",
            "severity": "danger",
            "message": f"New critical threat affecting your environment: {t.title}",
            "link": f"/threats"
        })

    return nudges
