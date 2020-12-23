
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, jsonify
)
from scan import Scanner
import sqlite3

app = Flask(__name__)
scanner = Scanner()
dbCon = sqlite3.connect("database/scanner.db", check_same_thread=False)
dbCur = dbCon.cursor()
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
        sql = "select id from Exploit where rowid=last_insert_rowid()"
        dbCur.execute(sql)
        currentid = dbCur.fetchone()
        print(currentid)
        file = request.files["File"]
        sql = "insert into Exploit (name,company,productName,exploitMovement,path) values (?,?,?,?);"
        return "Test"
    elif request.method == "GET":
        return render_template("exploit_upload.html")


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


app.run(host='0.0.0.0',debug=True)
