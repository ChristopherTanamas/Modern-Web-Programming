'''
Christopher Nathaniel Tanamas / 222200153
Grace Calista Lim / 222102176
Jemima Alithia Sigar / 222101393
'''

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# postgresql://postgres:password@localhost/nama db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nathantanamas@localhost/membership'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Fee(db.Model):
    kategori = db.Column(db.String(30), primary_key = True)
    harga = db.Column(db.Integer)

    member = db.relationship('Member', backref='fee') # 1 Jenis Fee dimiliki banyak member

    def __init__(self, kategori, harga):
        self.kategori = kategori
        self.harga = harga


class Member(db.Model):
    id = db.Column('id', db.String(20), primary_key = True)
    nama = db.Column(db.String(100))
    hp = db.Column(db.String(20))
    email = db.Column(db.String(100))
    kategori = db.Column(db.String(30), db.ForeignKey('fee.kategori'))
    akun_bank = db.Column(db.String(30))
    nomor_rekening = db.Column(db.String(30))

    attendance = db.relationship('Attendance', backref='member')
    transaction = db.relationship('Transaction', backref='member')
 
    def __init__(self, id, nama, hp, email, kategori, akun_bank, nomor_rekening):
        self.id = id
        self.nama = nama
        self.hp = hp
        self.email = email
        self.kategori = kategori
        self.akun_bank = akun_bank
        self.nomor_rekening = nomor_rekening


class Attendance(db.Model):
    id = db.Column('id', db.Integer, primary_key = True, autoincrement=True)
    tgl_kedatangan = db.Column(db.Date) # YYYY-MM-DD
    waktu_kedatangan = db.Column(db.Time) # HH:MM:SS
    id_member = db.Column(db.String(20), db.ForeignKey('member.id'))

    def __init__(self, tgl_kedatangan, waktu_kedatangan, id_member):
        self.tgl_kedatangan = tgl_kedatangan
        self.waktu_kedatangan = waktu_kedatangan
        self.id_member = id_member


class Transaction(db.Model):
    id = db.Column('id', db.Integer, primary_key = True, autoincrement=True)
    tgl_pembayaran = db.Column(db.Date) # YYYY-MM-DD
    waktu_pembayaran = db.Column(db.Time) # HH:MM:SS
    total_pembayaran = db.Column(db.Integer)
    id_member = db.Column(db.String(20), db.ForeignKey('member.id'))

    def __init__(self, tgl_pembayaran, waktu_pembayaran, total_pembayaran, id_member):
        self.tgl_pembayaran = tgl_pembayaran
        self.waktu_pembayaran = waktu_pembayaran
        self.total_pembayaran = total_pembayaran
        self.id_member = id_member