from flask import Flask,request,render_template
app = Flask(__name__)
import numpy as np
import ast
import pickle
import mysql.connector as mc
# query=("create database gaji")
# query=("use gaji")
# query=("create table gaji(age varchar(100),education varchar(100),isMarried varchar(100),sex varchar(100),workingHours varchar(100),job varchar(100),job_class varchar(100))")
# query="describe gaji"
db=mc.connect(host="localhost",
          port=3306,
          user="root",
          passwd="password",
          database= "gaji")
cs=db.cursor()
# cs.execute(query)
# print(list(cs))
# # Home Route
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/hasil",methods=["GET","POST"])
def hasil():
    if request.method == "POST":
        data = request.form
        #umur
        age = int(data["Umur"])
        age_name = str(age)
        #pendidikan
        edu = int(data["education"])
        edu_dict = {1: '1-4 SD', 2: '5-6 SD', 3: '7-8 SMP', 4: '9 SMP', 5: '10 SMA', 6: '11 SMA',
        7: '12 SMA', 8: 'D3', 9: 'S1/D4', 10: 'Master', 11: 'Doktor', 12: 'Sekolah Professional'}
        edu_name = edu_dict[edu]
        #status
        mar = int(data["marriage"])
        mar_name = "Belum Menikah" if mar==0 else "Menikah" if mar==1 else "Cerai"
        #sex
        sex = int(data["Jenis Kelamin"])
        sex_name = "Perempuan" if sex == 0 else "Laki-Laki"
        #jpm
        jpm = int(data["JPM"])
        jpm_name = str(jpm)
        #job-class
        jc = ast.literal_eval(data["Kelas Pekerja"])
        jc_list = ['Pekerja Bebas Bukan Perusahan', 'Pekerja Bebas Perusahaan',
        'Pemerintah Lokal', 'Pemerintah Negara', 'Pemerintah Provinsi',
        'Tanpa di Bayar', 'Tidak Pernah Bekerja', 'Wiraswasta', 'jc_unknown']
        jc_name = jc_list[jc.index(1)]
        #job
        job = ast.literal_eval(data["Pekerja"])
        job_list = ['Asisten Rumah Tangga', 'Ekesekutif Managerial', 'Mesin Inspeksi',
        'Pembersih', 'Pemuka Agama', 'Penjaga', 'Perbaikan Kerajinan', 'Petani',
        'Sales', 'Servis Lainnya', 'Spesialis', 'Supir', 'Tech-support',
        'Tentara']
        job_name = job_list[job.index(1)] 
        #result
        data_input = [[age, edu, mar, sex, jpm]+jc+job]
        data_scale = scaler.transform(data_input)
        pred = model.predict(data_scale)[0]
        pred_name = "Diatas 5 Juta!!!" if pred==1 else "Dibawah 5 Juta :("
        proba = model.predict_proba(data_scale)[0]
        if pred == 0:
            proba_name = round(proba[0],2) *100
        elif pred == 1:
            proba_name = round(proba[1],2) *100
        query = f"insert into gaji values (%s,%s,%s,%s,%s,%s,%s)"
        gaji_list = [age_name, edu_name, mar_name, sex_name, jpm_name, jc_name, job_name]
        cs.execute(query, gaji_list)
        print(data)
        print(pred)
        db.commit() 
        print(cs.rowcount, "Data tersimpan!")
        
    return render_template(
            "result.html", age = age_name, edu= edu_name,
            mar= mar_name, sex= sex_name, job= job_name, jc= jc_name,
            jpm= jpm_name, 
            pred= pred_name, proba = proba_name
        )

if __name__ == "__main__":
    model = pickle.load(open("modelGB.pkl", 'rb'))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    app.run(
        debug = True
    )