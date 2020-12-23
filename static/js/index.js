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

const about_host = function (ip){
    console.log("this is about_host")
    console.log(ip)
}
window.onload = function(){
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
    url = "/host/detail?ip="
    fetch(url).then(res =>{
        res.json().then(data=>{
            refresh_host_list(data)
        }).catch(err=>{
            console.log(err)
        })
    }).catch(err => {console.log(err)})
}

function textLengthOverCut(txt, len, lastTxt) {
        if (len == "" || len == null) {
            len = 20;
        }
        if (lastTxt == "" || lastTxt == null) {
            lastTxt = "...";
        }
        if (txt.length > len) {
            txt = txt.substr(0, len) + lastTxt;
        }
        return txt;
    }

