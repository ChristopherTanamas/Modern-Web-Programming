'''
Christopher Nathaniel Tanamas / 222200153
Grace Calista Lim / 222102176
Jemima Alithia Sigar / 222101393
'''

from flask import render_template, request, flash
from datetime import datetime, timedelta
from database import *
from sqlalchemy import desc, func


app.secret_key = "attendance"


# Inisialisasi data untuk Fee sesuai jenis kendaraan
@app.before_request
def insert_fee():
    if not Fee.query.first():   # cek apakah tabel Fee sudah diisi
        fee1 = Fee(kategori='Bus', harga=100000)
        fee2 = Fee(kategori='Travel', harga=50000)
        db.session.add(fee1)
        db.session.add(fee2)
        db.session.commit()


### Register ###
@app.route('/register')
def register():
    return render_template('register.html') 


@app.route('/register', methods=['GET','POST'])
def insert_member():
    if request.method == 'POST':    # insert khusus untuk metode "POST"
        id = request.form.get('id-member')
        nama = request.form.get('nama-member')
        hp = request.form.get('no-telp')
        email = request.form.get('email')
        kategori = request.form.get('kendaraan')
        akun = request.form.get('bank')
        norek = request.form.get('norek')

        # Cek apakah member telah terdaftar
        existing_member = Member.query.filter_by(id=id).first()
        if existing_member:
            flash('Member dengan ID ini sudah terdaftar!', 'error')
        else:
            member = Member(id=id, nama=nama, hp=hp, email=email, kategori=kategori, akun_bank=akun, nomor_rekening=norek)
            db.session.add(member)
            db.session.commit()
            flash('Pendaftaran berhasil!', 'success')
    return register()


### Attendance ###
@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/', methods=['GET','POST'])
def attendance():
    if request.method == 'POST':
        id = request.form.get('id-member')
        # Cek batas waktu
        limit = request.form.get('time-limit')
        if limit == 'time-off':
            time_limit = timedelta(minutes=0)
        elif limit == 'time-on':
            time_limit = timedelta(minutes=2)

        now = datetime.now()
        tgl_kedatangan = now.date()
        waktu_kedatangan = now.replace(microsecond=0).strftime("%H:%M:%S")  # ilangin milisecond

        # Periksa apakah sudah pernah register atau belum
        member = Member.query.filter_by(id=id).first()

        # Cek jumlah kedatangan
        count_attendance = db.session.query(func.count(Attendance.id)).filter(Attendance.id_member == id).scalar()
        count_attendance = (count_attendance + 1) % 5
        if member:
            latest_attend = Attendance.query.filter(Attendance.id_member == id).order_by(desc(Attendance.id)).first()   # cari yang paling baru
            if latest_attend:   # kalau misalkan ada absensi sebelumnya:
                # Cek apakah selisih absensi < 2 menit
                latest_attend_date = str(latest_attend.tgl_kedatangan)
                latest_attend_time = str(latest_attend.waktu_kedatangan)
                latest_attend_datetime = f"{latest_attend_date} {latest_attend_time}"
                full_latest_attend = datetime.strptime(latest_attend_datetime, "%Y-%m-%d %H:%M:%S")

                differ = now - full_latest_attend   # sekarang - waktu terdekat
                if differ < time_limit:
                    flash('Kehadiran masih kurang dari 1 hari!', 'danger')
                    return index()
                else:
                    attend = Attendance(tgl_kedatangan=tgl_kedatangan, waktu_kedatangan=waktu_kedatangan, id_member=id)
                    db.session.add(attend)
                    db.session.commit()
                    flash(f'Kehadiran {count_attendance} ke tercatat!', 'success')
            else:
                attend = Attendance(tgl_kedatangan=tgl_kedatangan, waktu_kedatangan=waktu_kedatangan, id_member=id)
                db.session.add(attend)
                db.session.commit()
                flash(f'Kehadiran {count_attendance} ke tercatat!', 'success')

            if (count_attendance % 5) == 0:
                flash('Anda telah hadir 5 kali.', 'info')
                return index()
            else:
                return index()
        else:
            flash('Member belum terdaftar!', 'error')
            return index()


### Pembayaran ###
@app.route('/pembayaran')
def payment():
    from_attendance = request.args.get('from')
    latest_attend = Attendance.query.order_by(desc(Attendance.id)).first()
    if latest_attend:
        latest_attend_id = latest_attend.id_member

        member = Member.query.join(Attendance, Member.id == latest_attend_id).first()
        member_bank = member.akun_bank
        member_norek = member.nomor_rekening
        print(member_bank)
        print(member_norek)
        latest_attend_pay = Fee.query.join(Member, Member.kategori == Fee.kategori).join(Attendance, Attendance.id_member == Member.id).filter(Attendance.id_member == latest_attend_id).first()
        total_payment = latest_attend_pay.harga * 5
        now = datetime.now()
        tgl_kedatangan = now.date()
        waktu_kedatangan = now.replace(microsecond=0).strftime("%H:%M:%S")

        # Lakukan Transaksi jika sudah 5x
        if from_attendance == "attendance5x":
            trans = Transaction(tgl_pembayaran=tgl_kedatangan, waktu_pembayaran=waktu_kedatangan, total_pembayaran=total_payment, id_member=latest_attend_id)
            db.session.add(trans)
            db.session.commit()
            return render_template('pembayaran.html', show_receipt=True, id_member=latest_attend_id, tgl=tgl_kedatangan, total=total_payment, bank=member_bank, norek=member_norek)
        else:
            return render_template('pembayaran.html', show_receipt=False)  # Jika belum 5x, halaman kosong
    else: 
        return render_template('pembayaran.html', show_receipt=False)
    
    
### Daftar Attendance ###
@app.route('/daftar_attendance')
def attendance_list():
    all_attendance = Attendance.query.all()
    return render_template('daftar_attendance.html', attendances=all_attendance)


### Daftar Pembayaran ###
@app.route('/daftar_pembayaran')
def transaction_list():
    all_transaction = Transaction.query.all()
    return render_template('daftar_pembayaran.html', transactions=all_transaction)


if __name__ == '__main__':
    insert_fee()
    app.config['DEBUG'] = True
    app.run(debug=True)