from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, jsonify
)
from scan import Scanner
import sqlite3
import hashlib
import fleep
import sys
import os
import time
import zipfile
import json




app = Flask(__name__)
scanner = Scanner()
dbCon = sqlite3.connect("database/scanner.db", check_same_thread=False)
dbCur = dbCon.cursor()

EXCUTE_FILE_NAME = "run.py"

@app.route("/",methods=["GET"])
def index():
    return render_template("index.html",data={"all_host":jsonify(scanner.get_all_host())})

## /scan/host_scan
@app.route("/scan/host_scan",methods=["POST"])
def host_scan():
    print("host scanning")
    ip_range = (request.json)['ip_range']
    scanner.host_scan(host=ip_range,argument="-sP")
    return jsonify(scanner.get_all_host())

@app.route("/host/vender")
def get_all_mac_addr():
    macAddr = request.args.get("mac")
    sql = "select company from MacVender where macAddr = ?"
    dbCur .execute(sql,[macAddr])
    rows = dbCur.fetchall()
    for r in rows:
        print(r)
    return jsonify(rows)

@app.route("/host/getAllHost")
def getAllHost():
    return jsonify(scanner.get_all_host())

@app.route("/host/detail")
def host_detail():
    ip = request.args.get("ip")
    return jsonify(scanner.get_host_detail(ip))

@app.route("/host/refresh_detail")
def refresh_detail():
    ip = request.args.get("ip")
    return jsonify(scanner.refresh_host_detail(ip))

@app.route("/exploit/search")
def exploit_search():
    keyword = request.args.get("keyword")
    sql = "select * from Exploit where name like ? or company like ? or productName like ? or exploitMovement like ? or path like ? limit 10"
    foo = "%"+keyword+"%"
    dbCur.execute(sql, [foo,foo,foo,foo,foo])
    rows = dbCur.fetchall()
    return jsonify(rows)

@app.route("/exploit/detail")
def exploit_detail():
    id = request.args.get("id")
    sql = "select * from Exploit where id=?"
    dbCur.execute(sql,[id])
    row = dbCur.fetchone()
    return render_template("exploit_detail.html",data=row)

@app.route("/exploit/upload",methods=["GET","POST"])
def exploit_upload():
    if request.method == "POST":
        tmp_file_path = ""
            # code 1 : not a zip file
            # code 2 : already exist
            # code 3 : file didn't uploaded
            # code 4 : etc (check your contents)
        try:
            file = request.files['file']
            tmp_file_path = "exploit/"+str(time.time())
            file.save(tmp_file_path)
        except Exception as e:
            return jsonify({"result":False,"code":3})
        try :
            with open(tmp_file_path, "rb") as f:
                info = fleep.get(f.read(128))
                data = f.read()
                f.close()
            if ("zip" in info.extension):
                print("file extention is right")
                path = "exploit/"+hashlib.md5(data).hexdigest()
                if (os.path.isdir(path)):
                    return jsonify({"result":False,"code":2})
                path += "/"
                with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
                    zip_ref.extractall(path=path)
                    # needs : name,company,version,productName,args(json),exploitMovement,path
                    try:
                        name = request.form.get("name")
                        company = request.form.get("company")
                        version = request.form.get("version")
                        productName = request.form.get("productName")
                        args = request.form.getlist("args[]")
                        args_json = json.dumps(args)
                        print("---- args_json ----")
                        exploitMovement = request.form.get("exploitMovement")
                        sql = "insert into Exploit (name,company,version,productName,args,exploitMovement,path) values (?,?,?,?,?,?,?);"
                        dbCur.execute(sql, [name,company,version,productName,args_json,exploitMovement,path])
                        dbCon.commit()
                    except Exception as e :
                        return jsonify({"result":False,"code":4})
                return jsonify({"result":True})
            else :
                return jsonify({"result":False,"code":1})
        except Exception as e :
            return jsonify({"result":False,"code":4})
        finally :
            print("remove tmp file")
            os.remove(tmp_file_path)

    elif request.method == "GET":
        return render_template("exploit_upload.html")

@app.route("/exploit/exec",methods=["POST"])
def exploit_exec():
    return "test"

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


app.run(host='0.0.0.0',debug=True)
