📚 BookTracker API
BookTracker, kitaplarınızı dijital olarak takip etmenizi ve onlara puan/yorum bırakmanızı sağlayan, kurumsal standartlarda geliştirilmiş bir backend projesidir. Proje, veri bütünlüğünü korumak için İlişkisel Veritabanı (RDBMS) mimarisini kullanır.

🚀 Öne Çıkan Özellikler
İlişkisel Veri Yapısı: Kitaplar ve Yorumlar arasında One-to-Many (Bire-Çok) ilişki kurgulandı.
Gelişmiş Validasyon: Pydantic Field özellikleri kullanılarak puanların 1-5 arasında olması ve sayfa sayısının negatif olmaması gibi kontroller sağlandı.
CRUD Operasyonları: Kitap ekleme, silme, güncelleme ve detaylı listeleme özellikleri tam kapsamlı olarak uygulandı.
Nested JSON Response: Bir kitap çağrıldığında, o kitaba ait tüm yorumların otomatik olarak liste şeklinde gelmesi sağlandı.

🛠️ Kullanılan Teknolojiler
Framework: FastAPI
Veritabanı & ORM: SQLite & SQLAlchemy
Veri Doğrulama: Pydantic
Sunucu: Uvicorn

📂 Proje Yapısı
database.py: Veritabanı bağlantı ayarları ve motor kurulumu.
models.py: SQLAlchemy tablo tanımları ve ilişkiler.
schemas.py: Pydantic veri giriş/çıkış şemaları.
main.py: API uç noktaları ve iş mantığı.
