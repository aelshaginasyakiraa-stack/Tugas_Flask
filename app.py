from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "praktikum_flask"

daftar_mahasiswa = []

class Mahasiswa:

    def __init__(self, nama, nim, email, password,
                 jurusan, jenis_kelamin, hobi, alamat):

        self.nama = nama
        self.nim = nim
        self.email = email
        self.password = password
        self.jurusan = jurusan
        self.jenis_kelamin = jenis_kelamin
        self.hobi = hobi
        self.alamat = alamat
        
    def validasi_nama(self):
        return len(self.nama.strip()) >= 3
    
    def validasi_nim(self):
        return self.nim.isdigit() and len(self.nim) == 10
    
    def validasi_email(self):
        return "@" in self.email and "." in self.email
    
    def validasi_password(self):
        return len(self.password) >= 8
    
    def validasi_alamat(self):
        return len(self.alamat.strip()) >= 10
    
    def cek_nim(self):

        for mhs in daftar_mahasiswa:
            if mhs.nim == self.nim:
                return False

        return True
    
    def validasi(self):

        if not self.validasi_nama():
            return False, "Nama minimal 3 karakter"

        if not self.validasi_nim():
            return False, "NIM harus 10 digit angka"

        if not self.cek_nim():
            return False, "NIM sudah terdaftar"

        if not self.validasi_email():
            return False, "Email tidak valid"

        if not self.validasi_password():
            return False, "Password minimal 8 karakter"

        if self.jurusan == "":
            return False, "Jurusan wajib dipilih"

        if self.jenis_kelamin == "":
            return False, "Jenis Kelamin wajib dipilih"

        if not self.validasi_alamat():
            return False, "Alamat minimal 10 karakter"

        return True, "Valid"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():

    nama = request.form["nama"]
    nim = request.form["nim"]
    email = request.form["email"]
    password = request.form["password"]
    jurusan = request.form["jurusan"]

    jenis_kelamin = request.form.get(
        "jenis_kelamin", ""
    )

    hobi = request.form.getlist("hobi")

    alamat = request.form["alamat"]

    mhs = Mahasiswa(
        nama,
        nim,
        email,
        password,
        jurusan,
        jenis_kelamin,
        hobi,
        alamat
    )

    valid, pesan = mhs.validasi()

    if not valid:
        flash(pesan)
        return redirect(url_for("index"))
    
    daftar_mahasiswa.append(mhs)

    return render_template(
    "hasil.html",
    mhs=mhs
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)