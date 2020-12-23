function host_scan() {
    document.querySelector(".left h2").innerText="host scan (wait...)"

    var url = '/scan/host_scan';
    var ip_range = document.querySelector(".left>div>div input").value

    var data = {"ip_range":ip_range};

    fetch(url, {
      method: 'POST',
      body: JSON.stringify(data),
      headers:{
        'Content-Type': 'application/json'
      }
    }).then(res => {
        document.querySelector(".left h2").innerText="host scan"
        let hostData = res.json()
        hostData.then((data) => {
            refresh_host_list(data)
            // save data
            localStorage.setItem('host_data', JSON.stringify(data));

        })
    })
    .catch(err =>{
        document.querySelector(".left h2").innerText="host scan"
        console.log("this is error")
        console.log(err)
    })
}

const refresh_host_list = function(data) {
    console.log(data)

    new Promise((resolve, reject) => {
        html =""
         data.forEach((element,index,array) => {
            html += `
                <li>
                    <button onClick="about_host('`+element.ip+`')">
                        `+element.ip+`
                    </button>
                </li>
            `
            console.log("running")
            if (index === array.length -1){
                console.log("done")
                resolve(html);
            }
        })
    }).then((html)=>{
        document.querySelector(".main .cont .left ul").innerHTML = html
    })

}

Current_host_detail_ip = ""

var test = {}

const set_host_detail = function(data){
        console.log(data)
        document.querySelector(".main .cont .right ul.host_detail>li:nth-child(1)>span").innerText = data.addresses.ipv4
        document.querySelector(".main .cont .right ul.host_detail>li:nth-child(3)>span").innerText = data.addresses.mac
        if(data.vendor[Object.keys(data.vendor)[0]]){
            document.querySelector(".main .cont .right ul.host_detail>li:nth-child(5)>span").innerText = data.vendor[Object.keys(data.vendor)[0]]
        }else if(data.addresses.mac){
            let tmp = data.addresses.mac.replace(":","").replace(":","").slice(0,5)
            console.log(tmp)
            fetch("/host/vender?mac="+tmp).then(res=>{
                res.json().then(data=>{
                    document.querySelector(".main .cont .right ul.host_detail>li:nth-child(5)>span").innerText = data
                    console.log(data)
                }).catch(err =>{
                    console.log(err)
                })
            }).catch(err => {
                console.log(err)
            })
        }else {
            document.querySelector(".main .cont .right ul.host_detail>li:nth-child(5)>span").innerText = "mac not founded"
        }
        document.querySelector(".main .cont .right ul.host_detail>li:nth-child(7)>p").innerText=""
        if (data.tcp != null) {
        Object.keys(data.tcp).forEach(e=>{
            document.querySelector(".main .cont .right ul.host_detail li:nth-child(7)>p").innerText+="\n"+e+"->"+data.tcp[e].name
        })
        }
        fetch_and_refresh_host_list()

}

const about_host = function (ip){
    Current_host_detail_ip = ip
    url = "/host/detail?ip="+ip
    fetch(url).then(res =>{
        res.json().then(data=>{
            set_host_detail(data)
        }).catch(err=>{
            console.log(err)
        })
    }).catch(err => {console.log(err)})
}

const refresh_host_detail = function () {
    url = "/host/refresh_detail?ip="+Current_host_detail_ip
    fetch(url).then(res=>{
        res.json().then(data => {
            set_host_detail(data)
        })
        .catch(err => {console.log(err)})
    }).catch(err => {console.log(err)})
}

const fetch_and_refresh_host_list = function () {
    url = "/host/getAllHost"
    fetch(url).then(res =>{
        res.json().then(data=>{
            refresh_host_list(data)
        }).catch(err=>{
            console.log(err)
        })
    }).catch(err => {console.log(err)})
}
window.onload = function(){
   fetch_and_refresh_host_list()
}
