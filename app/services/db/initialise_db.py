from app.services.db.meta import meta
from app.services.db.base import Base

def initialize_db():
    meta.create_all(Base)