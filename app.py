from flask import Flask,redirect,url_for,render_template,request,jsonify
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from datetime import datetime, timedelta
from bson import ObjectId
import os
from os.path import join, dirname
from dotenv import load_dotenv

app=Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

SECRET_KEY = "ALIM"

@app.route('/',methods=['GET','POST'])
def home():
    testimoni = list(db.testimoni.find({}))
    return render_template('index.html',testi=testimoni)


# Login
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/sign_in", methods=["POST"])
def sign_in():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    print(username_receive, pw_hash)
    result = db.users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )


@app.route('/testi',methods=['GET'])
def gettesti():
    return render_template('formtesti.html')

@app.route("/posttesti", methods=['POST'])
def posttesti():
    foto = request.files['foto']
    nama = request.form['nama']
    jabatan = request.form['jabatan']
    pesan = request.form['pesan']

    if foto :
        nama_file_asli = foto.filename
        nama_file_gambar = nama_file_asli.split('.')
        file_path = f'static/imgtesti/{nama_file_gambar}'
        foto.save(file_path)
    else :
        foto = None

    doc = {
        'foto' : nama_file_gambar, 
        'nama' : nama,
        'jabatan' : jabatan,
        'pesan' : pesan,
        }
    db.testimoni.insert_one(doc)
    return redirect(url_for('home', succes=True))


# Admin Panel

@app.route("/admin",methods=['GET','POST'])
def admin():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        testimoni = list(db.testimoni.find({}))
        return render_template('admin.html', testi=testimoni, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="There was problem logging you in"))

@app.route('/delete/<_id>',methods=['GET','POST'])
def delete(_id):
    db.testimoni.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)