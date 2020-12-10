import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,Flask
)
from scan import Scanner


app = Flask(__name__)
scanner = Scanner()

@app.route("/")
def index():
    print("index!")
    print(scanner.scanFromIp(host="192.168.43.0/24", argument="sP"))
    return render_template("index.html",data="this is data")

## /scan/host_scan
@app.route("/scan/host_scan",methods=["POST"])
def host_scan():
    scan_type = json.loads(request.json)
    if(scan_type == "arp"):
        res = scanner.scanFromIp(host="192.168.43.0/24",argument="sP")
    else :
        res = "false"
    return res


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response