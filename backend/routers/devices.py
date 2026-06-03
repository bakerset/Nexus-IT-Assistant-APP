from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.device import Device, DeviceCreate, DeviceUpdate, DeviceRead

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get("/", response_model=List[DeviceRead])
def get_devices(session: Session = Depends(get_session)):
    return session.exec(select(Device).order_by(Device.hostname)).all()

@router.get("/{device_id}", response_model=DeviceRead)
def get_device(device_id: int, session: Session = Depends(get_session)):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.post("/", response_model=DeviceRead)
def create_device(device: DeviceCreate, session: Session = Depends(get_session)):
    db_device = Device.from_orm(device)
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

@router.patch("/{device_id}", response_model=DeviceRead)
def update_device(device_id: int, device: DeviceUpdate, session: Session = Depends(get_session)):
    db_device = session.get(Device, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    data = device.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(db_device, k, v)
    db_device.updated_at = datetime.utcnow()
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

@router.delete("/{device_id}")
def delete_device(device_id: int, session: Session = Depends(get_session)):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    session.delete(device)
    session.commit()
    return {"ok": True}
