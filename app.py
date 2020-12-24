from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, jsonify
)
from scan import Scanner
import sqlite3
import hashlib
import fleep
import os
import time
import zipfile
import json
import subprocess

app = Flask(__name__)
scanner = Scanner()
dbCon = sqlite3.connect("database/scanner.db", check_same_thread=False)
dbCur = dbCon.cursor()

EXCUTE_FILE_NAME = "run.py"

def from_sqlite_Row_to_dict(list_with_rows):
    ''' Turn a list with sqlite3.Row objects into a dictionary'''
    d ={} # the dictionary to be filled with the row data and to be returned

    for i, row in enumerate(list_with_rows): # iterate throw the sqlite3.Row objects
        l = [] # for each Row use a separate list
        for col in range(0, len(row)): # copy over the row date (ie. column data) to a list
            l.append(row[col])
        d[i] = l # add the list to the dictionary
    return d


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

@app.route("/host/getAllHost")
def getAllHost():
    return jsonify(scanner.get_all_host())

@app.route("/host/vender")
def get_all_mac_addr():
    macAddr = request.args.get("mac")
    sql = "select company from MacVender where macAddr = ?"
    dbCur .execute(sql,[macAddr])
    row = dbCur.fetchone()
    return jsonify(row)

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
    data = dict(zip([c[0] for c in dbCur.description], row))
    return render_template("exploit_detail.html", data=data,args=json.loads(data["args"]))

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
                        exploitMovement = request.form.get("exploitMovement")
                        sql = "insert into Exploit (name,company,version,productName,args,exploitMovement,path) values (?,?,?,?,?,?,?);"
                        last_id = dbCur.execute(sql, [name,company,version,productName,args_json,exploitMovement,path]).lastrowid
                        dbCon.commit()
                    except Exception as e :
                        return jsonify({"result":False,"code":4})
                return "<script>location.href="+last_id+"</script>"
            else :
                return jsonify({"result":False,"code":1})
        except Exception as e :
            return jsonify({"result":False,"code":4})
        finally :
            print("remove tmp file")
            os.remove(tmp_file_path)

    elif request.method == "GET":
        return render_template("exploit_upload.html")

def runEx(cmd):
    os.system(cmd)

@app.route("/exploit/exec",methods=["POST"])
def exploit_exec():
    id = request.form.get("id")
    args = request.form.getlist("args[]")
    sql = "select * from Exploit where id=?;"
    dbCur.execute(sql,[id])
    row = dbCur.fetchone()
    data = dict(zip([c[0] for c in dbCur.description], row))
    args = ""
    for arg in json.loads(data["args"]):
        args += " "+arg+" "
    cmd = "python3 "+data["path"]+"/run.py;read"
    subprocess.Popen(["lxterminal", "-e", cmd])

    return "done"

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


app.run(host='0.0.0.0',debug=True)
