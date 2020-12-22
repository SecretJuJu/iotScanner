
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, jsonify
)
from scan import Scanner
import sqlite3

app = Flask(__name__)
scanner = Scanner()
macMapConn = sqlite3.connect("./database/macMap.db", check_same_thread=False)
macMapCur = macMapConn.cursor()

@app.route("/")
def index():
    print("index!")
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
    sql = "select * from MacVender where macAddr = ?"
    macMapCur.execute(sql,[macAddr])
    rows = macMapCur.fetchall()
    for r in rows:
        print(r)
    return jsonify(rows)

@app.route("/host/getAllHost")
def getAllHost():
    return jsonify(scanner.get_all_host())

@app.route("/host/detail")
def host_detail():
    ip = request.args.get("ip")
    return scanner.get_host_detail(ip)

@app.route("/exploit/detail")
def exploit_detail():
    id = request.args.get("id")

    return render_template("exploit_detail.html",data="this is data")

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response