import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, jsonify
)
from scan import Scanner


app = Flask(__name__)
scanner = Scanner()

@app.route("/")
def index():
    print("index!")
    return render_template("index.html",data="this is data")

## /scan/host_scan
@app.route("/scan/host_scan",methods=["POST"])
def host_scan():
    print("host scanning")
    scan_type = (request.json)['scan_type']
    #print("scan type : "+str(scan_type))

    res = None
    if(scan_type == "sP"): # arp scan
        print("arp scan")
        scanner.host_scan(host="192.168.43.0/24",argument="-sP")
    elif(scan_type == "sn"): # ping scan
        print("ping scan")
        scanner.host_scan(host="192.168.43.0/24", argument="-sn")
    elif(scan_type == "Pn"):
        print("no ping scan")
        scanner.host_scan(host="192.168.43.0/24", argument="-Pn")


    print("-- response --")
    return jsonify(scanner.get_all_host())


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response