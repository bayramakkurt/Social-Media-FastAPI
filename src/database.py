#Veritabanı işlemleri

from sqlalchemy import create_engine #fonksiyonu, bir veritabanı bağlantısı (database engine) oluşturur.
from sqlalchemy.ext.declarative import declarative_base #çağrıldığında bir Base sınıfı döner; bu sınıf, tüm ORM modellerinin (yani veritabanı tablolarını temsil eden Python sınıflarının) temeli olur.
from sqlalchemy.orm import sessionmaker #sayesinde veritabanına veri ekleme, silme, güncelleme gibi işlemler yapılır.

DB_URL = "sqlite:///./src/veritabani.db"

engine = create_engine(DB_URL, pool_pre_ping=True) #Veritabanı için Motor oluşturuldu. Veritabanı bağlanmadan önce ping atılması için parametre True yapıldı.
SessionLocal = sessionmaker(bind=engine, autoflush=False) #Veritabanı için oturum açıldı. Veritabanı değişiklikleri commit edilmeden SQL gönderilmesin diye parametre False yapıldı.
Base = declarative_base() #SQLAlchemy’de ORM modellerini tanımlamak için temel (base) sınıfı oluşturur.

def get_db(): #Burada veritabanı oturumu try-yield ile açılır ve işlem bitince finally ile oturumu kapatır.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()