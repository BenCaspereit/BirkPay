import logging
from app.db.session import engine, Base, SessionLocal

try:
    from app.models.user import User
    from app.models.product import Product
    from app.models.transaction import Transaction
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Erstellt alle in SQLAlchemy definierten Tabellen in PostgreSQL,
    falls diese noch nicht existieren.
    """
    logger.info("Erstelle Datenbank-Tabellen...")
    
    # Liest alle Klassen, die von Base erben, und legt sie in Postgres an
    Base.metadata.create_all(bind=engine)
    
    logger.info("Tabellen erfolgreich erstellt!")


def seed_demo_data() -> None:
    """
    Fügt optionale Testdaten (Admin & Beispielprodukt) ein, 
    falls die Datenbank noch leer ist.
    """
    db = SessionLocal()
    try:
        # Prüfen, ob bereits User existieren
        from app.models.user import User
        if not db.query(User).first():
            logger.info("Füge Initiale Test-Daten ein...")
            
            demo_admin = User(
                school_id="schule-1",
                nfc_uid="ADMIN_NFC_123",
                name="Kassen Admin",
                balance_cents=5000,  # 50,00 € Startguthaben
                role="admin"
            )
            db.add(demo_admin)
            db.commit()
            logger.info("Demo-Admin erfolgreich angelegt!")
    except Exception as e:
        logger.warning(f"Seeding übersprungen oder fehlgeschlagen: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_demo_data()

# python -m app.db.init_db