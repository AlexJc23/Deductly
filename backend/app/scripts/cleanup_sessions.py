from app.db.session import SessionLocal
from app.services.maintenance_service import cleanup_sessions


def run():
    db = SessionLocal()

    try:
        cleanup_sessions(db)
        print("Session cleanup completed")
    finally:
        db.close()


if __name__ == "__main__":
    run()
