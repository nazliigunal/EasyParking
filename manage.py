from flask import Flask, render_template, request, redirect, url_for, flash, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators 
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_mail import Mail, Message





app = Flask(__name__)
admin=Admin(app)
app.secret_key = "n_g_key_123321"
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYQL_DB"]="veriler"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/easyparking'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MYSQL_CURSORCLASS"] = "DictCursor" 
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['DEBUG'] = True
app.config['TESTİNG']=False
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ada.unal52@gmail.com '
app.config['MAIL_PASSWORD'] = 'rdhkmqguzlsvjfsc'
app.config['MAIL_DEFAULT_SENDER']='ada.unal52@gmail.com'
#app.config['MAIL_DEBUG'] = True
app.config['MAIL_MAX_EMAILS'] = 5
#app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

Session = sessionmaker(bind=engine)
db = SQLAlchemy(app)
mysql=MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db_session = Session()
mail = Mail(app)


# Veritabanı tabloları oluşturma
class Otoparklar(db.Model):
    __tablename__ = 'otopark'
    id = db.Column(db.Integer, primary_key=True)
    oto_ad = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)
    kapasite=db.Column(db.Integer, nullable=False)
    calisanlar=db.relationship('Calisan', backref='otopark')
    araclar=db.relationship('Arac', backref='otopark')

class Calisan(UserMixin,db.Model):
    __tablename__ = 'calisan'
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(25), nullable=False)
    soyad = db.Column(db.Text, nullable=False)
    kullanici_adi = db.Column(db.String(25), unique=True, nullable=False)
    sifre = db.Column(db.String(25), nullable=False)
    otopark_id = db.Column(db.Integer, db.ForeignKey('otopark.id'), nullable=False)

    def __init__(self, user_id):
        self.id = user_id


class Arac(db.Model):
    __tablename__ = 'arac'
    park_yeri=db.Column(db.String(50), primary_key=True)
    plaka = db.Column(db.Text, nullable=False)
    giris_saati = db.Column(db.DateTime)
    cikis_saati = db.Column(db.DateTime)
    otopark_id = db.Column(db.Integer, db.ForeignKey('otopark.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Calisan.query.get(int(user_id))

#Tabloları admin panalde görüntüleme
admin.add_view(ModelView(Calisan,db.session))
admin.add_view(ModelView(Otoparklar,db.session))
admin.add_view(ModelView(Arac,db.session))

#İletişim formu
class iletisimform(Form):
    ad=StringField(validators=[validators.DataRequired()])
    soyad=StringField(validators=[validators.DataRequired()])
    email = StringField( validators=[validators.DataRequired(), validators.Email(message="Geçerli bir email adresi giriniz!!")])
    mesaj = StringField( validators=[validators.DataRequired(), validators.Length(min=5, max=300)])

#Giriş yap formu
class girisyapform(Form):
    kullaniciadi=StringField("Kullanıcı Adı",validators=[validators.DataRequired()])
    sifre=PasswordField("Şifre")

#Araç giriş-cıkış formu
class parkyeriformu(Form):
    parkyeri=StringField("Park Yeri")
    plaka=StringField("Plaka")


#Anasayfa
@app.route("/")
def giris():
    return render_template("anasayfa.html")

#Hakkımızda sayfası
@app.route("/hakkimizda")
def hakkimizda():
    return render_template("hakkimizda.html")

#İletişim sayfası
@app.route("/iletisim",methods=["GET","POST"])
def iletisim():
    form = iletisimform(request.form)

    if request.method == "POST" and form.validate():
        ad = form.ad.data
        soyad = form.soyad.data
        email = form.email.data
        mesaj = form.mesaj.data

        # E-posta gönderme işlemi
        msg = Message("İletişim Formu Mesajı", recipients=["ada.unal52@gmail.com"])
        msg.body = f"Ad: {ad}\nSoyad: {soyad}\nE-posta: {email}\nMesaj: {mesaj}"
        mail.send(msg)

        flash("Mesaj Başarıyla Gönderildi", "success")
        return redirect(url_for("iletisim"))
    
    return render_template("iletisim.html", form=form)

#Giriş Sayfası
@app.route("/giris.yap", methods=["GET","POST"])
def girisyap():
    form=girisyapform(request.form)
    if request.method=="POST":
        kullaniciadi=form.kullaniciadi.data
        sifre=form.sifre.data
        
        calisan = Calisan.query.filter_by(kullanici_adi=kullaniciadi).first()
        
        if calisan and calisan.sifre == sifre:
            login_user(calisan)
            session["logged_in"]=True
            
            flash("Giriş Başarıyla Gerçekleşti","success")
            if calisan.otopark_id == 1:
                session["kontrol"]="1"
                return redirect(url_for("olcay"))
            elif calisan.otopark_id == 2:
                return redirect(url_for("nazli"))
            elif calisan.otopark_id == 3:
                return redirect(url_for("gunisigi"))
            elif calisan.otopark_id==4:
                return redirect(url_for("kader"))
            elif calisan.otopark_id==5:
                return redirect(url_for("kapali"))
            elif calisan.otopark_id==6:
                return redirect(url_for("necatibey"))
        else:
          flash("Giriş Başarısız Oldu","danger")
          return redirect(url_for("girisyap"))
    
    return render_template('giris_yap.html', form=form)

#Çıkış yapma işlemi
@app.route("/cikis.yap")
def logout():
    session.clear()
    flash("Çıkış Başarıyla Gerçekleşti","success")
    return redirect(url_for("giris"))



    
#Olcay Otopark Sayfası    
@app.route("/olcay.otopark", methods=["GET", "POST"])
def olcay():
    Session = sessionmaker(bind=db.engine)
    db_session = Session()
    form = parkyeriformu(request.form)  
    otopark_id=1
    checkbox_ids = ["OA{}".format(i) for i in range(1, 29)]
    if request.method == "POST":
        park_yeri_ = "O" + form.parkyeri.data if form.parkyeri.data is not None else ""
        otopark(db_session,checkbox_ids,park_yeri_,otopark_id, form)
            
    db_session.close()    
    arac_data = checkbox()
    return render_template("olcay.html", form=form, arac_data=arac_data)




#Nazlı Otopark Sayfası
@app.route("/nazli.otopark" , methods=["GET","POST"])
def nazli():
    Session = sessionmaker(bind=db.engine)
    db_session = Session()
    form = parkyeriformu(request.form) 
    otopark_id=2
    checkbox_ids = ["ZA{}".format(i) for i in range(1, 25)]
    if request.method == "POST":
        park_yeri_ = "Z" + form.parkyeri.data if form.parkyeri.data is not None else ""
        otopark(db_session,checkbox_ids,park_yeri_,otopark_id, form)
    db_session.close()    
    arac_data = checkbox()
    return render_template("nazli.html", form=form, arac_data=arac_data)



#Kader Otopark sayfası
@app.route("/kader.otopark" , methods=["GET","POST"])
def kader():
    Session = sessionmaker(bind=db.engine)
    db_session = Session()
    form = parkyeriformu(request.form)  
    otopark_id=4
    checkbox_ids = ["KA{}".format(i) for i in range(1, 27)]
    if request.method == "POST":
        park_yeri_ = "K" + form.parkyeri.data if form.parkyeri.data is not None else ""
        otopark(db_session,checkbox_ids,park_yeri_,otopark_id, form)
            
    db_session.close()    
    arac_data = checkbox()
    return render_template("kader.html", form=form, arac_data=arac_data)



#Günışığı Otopark
@app.route("/gunisigi.otopark" , methods=["GET","POST"])
def gunisigi():
    Session = sessionmaker(bind=db.engine)
    db_session = Session()
    form = parkyeriformu(request.form)  
    otopark_id=3
    checkbox_ids = ["GA{}".format(i) for i in range(1, 27)]
    if request.method == "POST":
        park_yeri_ = "G" + form.parkyeri.data if form.parkyeri.data is not None else ""
        otopark(db_session,checkbox_ids,park_yeri_,otopark_id, form)
            
    db_session.close()    
    arac_data = checkbox()
    return render_template("gunisigi.html", form=form, arac_data=arac_data)


#Kapalı Otopark
@app.route("/kapali.otopark" , methods=["GET","POST"])
def kapali():
    Session = sessionmaker(bind=db.engine)
    db_session = Session()
    form = parkyeriformu(request.form)  
    otopark_id=5
    checkbox_ids = ["PA{}".format(i) for i in range(1, 27)]
    if request.method == "POST":
        park_yeri_ = "P" + form.parkyeri.data if form.parkyeri.data is not None else ""
        otopark(db_session,checkbox_ids,park_yeri_,otopark_id, form)
    db_session.close()    
    arac_data = checkbox()
    return render_template("kapali.html", form=form, arac_data=arac_data)


#Necatibey Otopark sayfası
@app.route("/necatibey.otopark", methods=["GET","POST"])
def necatibey():
    Session = sessionmaker(bind=db.engine)
    db_session = Session()
    form = parkyeriformu(request.form)  
    otopark_id=6
    checkbox_ids = ["BA{}".format(i) for i in range(1, 27)]
    if request.method == "POST":
        park_yeri_ = "B" + form.parkyeri.data if form.parkyeri.data is not None else ""
        otopark(db_session,checkbox_ids,park_yeri_,otopark_id, form)
    db_session.close()    
    arac_data = checkbox()
    return render_template("necatibey.html", form=form, arac_data=arac_data)


#Her otoparkın kullanıcağı fonksiyon
def otopark(db_session,checkbox_ids,park_yeri_,otopark_id, form):
        ücret=None
        session["ücret"] = ücret
        # giris butonuna basınca başlıcak olan işlemler
        if 'giris' in request.form:
            ücret=None
            session["ücret"] = ücret
            park_yeri = form.parkyeri.data
            plaka = form.plaka.data
            if plaka and park_yeri:
                if park_yeri_ in checkbox_ids :
                    arac_ekle(db_session,park_yeri_,plaka,otopark_id)
                else:
                    flash("Park Etme İşlemi Geçersiz", "danger")
            else:
                flash("Eksik bilgi girildi", "danger")
        #çıkış butonuna basınca başlıcak olan işlemler
        elif 'cikis' in request.form:
            plaka = form.plaka.data
            park_yeri = form.parkyeri.data
            if park_yeri and plaka:
                arac1 = db_session.query(Arac).filter_by(park_yeri=park_yeri_, plaka=plaka, otopark_id=otopark_id).first()
                if arac1:
                    arac_sil(db_session,arac1)
                else:
                    flash("Araç bulunamadı.", "danger")
            elif park_yeri:
                park_yeri = form.parkyeri.data
                arac1 = db_session.query(Arac).filter_by(park_yeri=park_yeri_,  otopark_id=otopark_id).filter(Arac.plaka != "0").first()
                if arac1:
                    arac_sil(db_session,arac1)
                else:
                     flash("Böyle bir park yeri bulunamadı.", "danger")
            elif plaka:
                 arac1 = db_session.query(Arac).filter_by(plaka=plaka, otopark_id=otopark_id).first()
                 if arac1:
                     arac_sil(db_session,arac1)
                 else:
                    flash("Böyle bir plakaya sahip araç bulunamadı.", "danger")
            else:
               flash("Lütfen plaka veya park yeri bilgisini girin.", "danger")


# arac eklemek için fonksiyon
def arac_ekle(db_session,park_yeri_, plaka, otopark_id):
    arac1 = db_session.query(Arac).filter_by(park_yeri=park_yeri_, otopark_id=otopark_id).first()


    if arac1:
        if arac1.plaka == "0":
            arac1.plaka = plaka
            arac1.giris_saati = datetime.now()
            flash("Araç Başarıyla Giriş Yaptı", "success")
            
        else:
            flash("Bu Park Yeri Dolu", "danger")
    else:
        yeni_arac = Arac(
            park_yeri=park_yeri_,
            plaka=plaka,
            giris_saati=datetime.now(),
            otopark_id=otopark_id
        )
        db_session.add(yeni_arac)
        flash("Yeni Park Yeri Oluşturuldu ve Araç Girişi Yapıldı", "success")
       
    db_session.commit()  
     

#araç silme fonksiyonu
def arac_sil(db_session,arac1):
    arac1.cikis_saati = datetime.now()
    durulan_saat = arac1.cikis_saati - arac1.giris_saati
    hours = durulan_saat.seconds // 3600
    minutes = (durulan_saat.seconds % 3600) // 60
    ücret = (hours * 60 + minutes) * 20
    session["ücret"] = ücret
    arac1.plaka = "0"
    arac1.giris_saati = None
    arac1.cikis_saati = None
    db_session.commit()
    
    flash("Araç başarıyla çıkış yaptı.", "success")
    
#checkbox kontrol fonksiyonu
def checkbox():
    arac_data = []
    
    araclar = Arac.query.all()  
    for arac in araclar:
        arac_sözlük = {
            "park_yeri": arac.park_yeri,
            "plaka": arac.plaka
        }
        arac_data.append(arac_sözlük)
    
    return arac_data


with app.app_context():
  if __name__=="__main__":
    db.create_all()
    app.run(debug=True)


