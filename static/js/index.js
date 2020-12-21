function host_scan() {
    console.log("helloworld")
    document.querySelector(".left h2").innerText="host scan (wait...)"

    var url = '/scan/host_scan';
    var first_ip = document.querySelector(".left>div>div input:nth-child(1)").value
    var last_ip = document.querySelector(".left>div>div input:nth-child(2)").value

    var data = {"first_ip":first_ip,"last_ip":last_ip};
    console.log(first_ip)
    console.log(last_ip)

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