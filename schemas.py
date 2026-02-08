#schemas.py dosyası, API'mize dışarıdan gelen verilerin kapı görevlisidir.
# Burada Pydantic kullanarak verilerin tipini, zorunluluğunu ve senin de belirttiğin gibi "sayfa sayısının eksi olmaması" gibi kuralları belirleyeceğiz.

from pydantic import BaseModel, Field
from typing import Optional, List

# Yorumlar için temel şema
class ReviewBase(BaseModel):
    rating: int = Field(gt=0, le=5, description="Puan 1 ile 5 arasında olmalıdır")
    comment: Optional[str] = Field(None, max_length=250)

# Yeni yorum oluştururken kullanılacak şema
class ReviewCreate(ReviewBase):
    pass

# API'den yorum dönerken kullanılacak şema
class Review(ReviewBase):
    id: int
    book_id: int

    class Config:
        from_attributes = True

# Kitaplar için temel şema
class BookBase(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    pages: int = Field(gt=0, description="Sayfa sayısı 0'dan büyük olmalıdır")
    status: str = Field(default="Okunacak")

# Yeni kitap oluştururken kullanılacak şema
class BookCreate(BookBase):
    pass #Python'da bir bloğun (sınıf veya fonksiyon) gövdesi boş bırakılamaz. pass, "burada ekstra bir şey yapma, sadece yukarıdaki özellikleri kullan" demektir.

# API'den kitap dönerken (yorumlarıyla birlikte) kullanılacak şema
class Book(BookBase):
    id: int
    reviews: List[Review] = [] # İlişkili yorumları liste olarak döner

    class Config:
        from_attributes = True