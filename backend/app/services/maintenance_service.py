from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.session import Session as DBSession


def cleanup_sessions(db: Session):
    now = datetime.utcnow()

    # expire sessions that have passed their expiration time
    db.query(DBSession).filter(
        DBSession.expires_at < now).delete()

    # delete revoked sessions that are older than a day
    db.query(DBSession).filter(
        DBSession.is_revoked == True,
        DBSession.expires_at < now - timedelta(days=1)
    ).delete()

    db.commit()
