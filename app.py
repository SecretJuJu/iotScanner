
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
    scan_type = (request.json)['scan_type']
    network = "192.168.0.0/24"
    #print("scan type : "+str(scan_type))

    res = None
    if(scan_type == "sP"): # arp scan
        print("arp scan")
        scanner.host_scan(host=network,argument="-sP")
    elif(scan_type == "sn"): # ping scan
        print("ping scan")
        scanner.host_scan(host=network, argument="-sn")
    elif(scan_type == "Pn"):
        print("no ping scan")
        scanner.host_scan(host=network, argument="-Pn")


    print("-- response --")
    return jsonify(scanner.get_all_host())

@app.route("/mac_match")
def get_all_mac_addr():
    macAddr = request.args.get("mac")
    sql = "select * from MacVender where macAddr = ?"
    macMapCur.execute(sql,[macAddr])
    rows = macMapCur.fetchall()
    for r in rows:
        print(r)
    return "success"

@app.route("/exploit_detail")
def exploit_detail():
    return render_template("exploit_detail.html",data="this is data")


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response