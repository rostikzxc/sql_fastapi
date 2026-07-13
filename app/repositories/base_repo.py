from sqlalchemy.orm import Session

def get_by_id(model, obj_id: int, db: Session):
    return db.query(model).filter(model.id == obj_id).first()