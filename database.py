from sqlalchemy import create_engine
#Bu, SQLAlchemy'nin santral merkezidir. Veritabanına nasıl bağlanacağını (hangi sürücü, hangi kullanıcı adı, hangi adres) bilir.
#Ancak hemen bağlantı kurmaz; sadece bir "bağlantı noktası" oluşturur.
#Görevi: Veritabanı ile konuşacak olan düşük seviyeli bağlantıyı yönetmek.

from sqlalchemy.orm import sessionmaker
#Bu bir fabrikadır. Veritabanındaki tabloları temsil edecek Python sınıfları oluşturmanız için size bir "temel sınıf" (Base class) verir.
#Sizin modelleriniz bu sınıftan miras alır.
#Görevi: Python sınıfları ile veritabanı tabloları arasındaki haritalamayı (mapping) kayıt altına almak.


from sqlalchemy.ext.declarative import declarative_base
#Bu aslında genellikle Base.metadata.create_all(engine) şeklinde kullanılır.
#Görevi: Kodunuzda tanımladığınız tüm modelleri (tabloları) tarar ve eğer veritabanında henüz yoklarsa onları otomatik olarak fiziksel olarak oluşturur.

# Veritabanı dosyasının adını belirliyoruz
SQLALCHEMY_DATABASE_URL = "sqlite:///./books_app.db"

# SQLite için özel bir ayar: 'check_same_thread' False olmalı (FastAPI'nin async yapısı için)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Veritabanı ile konuşacak oturum (session) fabrikasını kuruyoruz
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modellerimizin miras alacağı ana sınıfı oluşturuyoruz
Base = declarative_base()