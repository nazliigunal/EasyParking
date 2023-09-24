
# EASYPARKİNG

EasyParking Projesi, bir otopark yönetim sistemi uygulamasıdır. Bu uygulama ile farklı otoparklar için araç giriş ve çıkışlarını kaydedebilir, otopark kapasitelerini yönetebilir ve iletişim formu aracılığıyla yönetici ile iletişime geçebilirsiniz.

## Başlangıç

Bu talimatlar, projenizin yerel bir makinede nasıl çalıştırılacağını ve geliştirileceğini açıklar. 

### Gereksinimler

Bu projeyi çalıştırmak ve geliştirmek için aşağıdaki gereksinimlere ihtiyacınız vardır:

- Python (3.x)
- Flask (Python web uygulama çerçevesi)
- Flask SQLAlchemy (SQL veritabanı işlemleri için Flask eklentisi)
- Flask MySQLdb (MySQL veritabanı için Flask eklentisi)
- Flask Mail (E-posta gönderme için Flask eklentisi)
  
Gereksinimleri yüklemek için aşağıdaki komutları kullanabilirsiniz:
- pip install Flask Flask-SQLAlchemy Flask-MySQLdb Flask-Login Flask-Mail

## Geliştirme Ortamı
- Flask Framework
- SQLAlchemy
- Flask-Admin
- WTForms
- Flask-Mail
  
## Veritabanı Ayarları
Proje, MySQL veritabanını kullanır. Veritabanı bağlantı bilgileri aşağıdaki gibidir:
- Host: localhost
- Kullanıcı Adı: root
- Şifre: (şifre yok)
- Veritabanı Adı: easyparking

### Kurulum

1. Bu projeyi bilgisayarınıza klonlayın
2. Proje dizinine gidin
3. Uygulamayı başlatmak için aşağıdaki komutu çalıştırın:
   python main.py

Uygulama şimdi `http://localhost:5000` adresinde çalışıyor olmalıdır.

## Kullanım

Uygulama, aşağıdaki temel özellikleri içerir:

- Ana Sayfa
- Hakkımızda Sayfası
- İletişim Sayfası
- Giriş Yap Sayfası
- Otopark Sayfaları (Her otopark için ayrı sayfa bulunmaktadır)

Eğer giriş yaptıysanız topark sayfalarında araç girişi ve çıkışı yapabilirsiniz.Diğer türlü otoparkların dolu-boş yerleri gösterilecektir. Her otoparkın kendi özel sayfası bulunmaktadır ve otoparkın kapasitesi, doluluk durumu gibi bilgiler görüntülenir.

### Hızlı Başlangıç Kılavuzu
- Uygulamaya tarayıcınızdan erişin.
- Otopark seçin
- Doluluk durumuna bakın
- İletişim sayfasına gidin
- Formu doldurun
- Giriş yapın 
- Araç giriş/cıkış işlemlerini gerçekleştirin.