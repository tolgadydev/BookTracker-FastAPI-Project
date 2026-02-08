from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    status = Column(String)  # "Okunacak", "Okunuyor", "Bitti" gibi

    # Kitap ile yorumlar arasındaki ilişki (Bir kitabın çok yorumu olabilir)
    reviews = relationship("Reviews", back_populates="owner")


class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)  # 1 ile 5 arası
    comment = Column(String)

    # Hangi kitaba ait olduğunu belirten Foreign Key
    book_id = Column(Integer, ForeignKey("books.id"))

    # Yorumun hangi kitaba ait olduğunu anlamamızı sağlayan ters ilişki
    owner = relationship("Books", back_populates="reviews")


#ForeignKey("books.id"): reviews tablosundaki her satırın, books tablosundaki bir id ile eşleşmesini sağlar.
#Yani "sahipsiz" yorum yapılmasını engeller.


#relationship: Bu aslında veritabanında bir sütun değildir. SQLAlchemy'nin bize sunduğu bir "sihirdir".
#Bu sayede bir kitap nesnesini çektiğinde, .reviews diyerek o kitaba ait tüm yorumlara bir liste olarak ulaşabileceksin.

#back_populates: İki tabloya da birbirini tanıtır. Kitap yorumları bilir, yorumlar da hangi kitaba ait olduğunu bilir.