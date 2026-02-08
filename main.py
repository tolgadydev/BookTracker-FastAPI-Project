from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, SessionLocal
from typing import List, Annotated

app = FastAPI()

# Veritabanı tablolarını otomatik oluşturur
models.Base.metadata.create_all(bind=engine)

# Veritabanı oturumu (session) yönetimi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# --- KİTAP ENDPOINTLERİ ---

@app.post("/books/", status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
async def create_book(book_request: schemas.BookCreate, db: db_dependency):
    # Yeni bir kitap nesnesi oluşturuyoruz
    new_book = models.Books(**book_request.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books/", response_model=List[schemas.Book])
async def read_all_books(db: db_dependency):
    # Tüm kitapları (ilişkili yorumlarıyla birlikte) çeker
    return db.query(models.Books).all()

@app.get("/books/{book_id}", response_model=schemas.Book)
async def read_book(book_id: int, db: db_dependency):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    return book


#Bu Kodda Neler Yaptık?
#models.Base.metadata.create_all(bind=engine): Uygulama her başladığında models.py dosyanı kontrol eder ve eğer veritabanında bu tablolar yoksa otomatik olarak oluşturur.
#db_dependency: Bağımlılık enjeksiyonu (Dependency Injection) kullanarak her istekte veritabanı bağlantısının güvenli bir şekilde açılıp kapanmasını sağladık.
#model_dump(): Pydantic nesnesini bir Python sözlüğüne (dict) çevirdik. Hatırlarsan önceki projende dict() yerine bunu kullanmanın daha güncel olduğunu konuşmuştuk.
#response_model: FastAPI'ye "Kullanıcıya veri gönderirken schemas.Book yapısına sadık kal" dedik. Bu sayede ilişkisel veriler (kitabın yorumları gibi) otomatik olarak JSON formatına girer.


# --- YORUM (REVIEW) ENDPOINTLERI ---

@app.post("/reviews/", status_code=status.HTTP_201_CREATED, response_model=schemas.Review)
async def create_review(review_request: schemas.ReviewCreate, book_id: int, db: db_dependency):
    # Önce böyle bir kitap var mı kontrol edelim
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Yorum yapmak istediğiniz kitap bulunamadı")

    # Yeni yorumu oluşturuyoruz
    new_review = models.Reviews(**review_request.model_dump(), book_id=book_id)

    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@app.get("/reviews/", response_model=List[schemas.Review])
async def read_all_reviews(db: db_dependency):
    return db.query(models.Reviews).all()

#Burada Ne Değişti?
#book_id Kontrolü: Yorumu rastgele bir yere eklemiyoruz. Önce veritabanında o ID'ye sahip bir kitap var mı bakıyoruz. Eğer yoksa kullanıcıya 404 hatası fırlatıyoruz.
#İlişkiyi Kurma: models.Reviews nesnesini oluştururken, Pydantic'ten gelen verilere ek olarak dışarıdan aldığımız book_id bilgisini de veritabanına kaydediyoruz.


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: db_dependency):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Silmek istediğiniz kitap bulunamadı")

    # Kitaba bağlı yorumları da siliyoruz (Opsiyonel: Modellerde cascade ayarı yoksa manuel silme)
    db.query(models.Reviews).filter(models.Reviews.book_id == book_id).delete()

    db.delete(book)
    db.commit()



@app.put("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_review(review_id: int, review_request: schemas.ReviewCreate, db: db_dependency):
    review = db.query(models.Reviews).filter(models.Reviews.id == review_id).first()

    if review is None:
        raise HTTPException(status_code=404, detail="Güncellemek istediğiniz yorum bulunamadı")

    review.rating = review_request.rating
    review.comment = review_request.comment

    db.add(review)
    db.commit()

















