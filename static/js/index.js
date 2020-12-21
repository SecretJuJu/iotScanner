function host_scan() {
    console.log("helloworld")
    document.querySelector(".left h2").innerText="host scan (wait...)"

    var url = '/scan/host_scan';
    var ip_range = document.querySelector(".left>div>div input").value

    var data = {"ip_range":ip_range};
    console.log(data)

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
    console.log("get all host info from server")
    url = "/host/getAllHost"
    fetch(url).then(function(res) {
        if(res.ok) {
            console.log(res)
            console.log(res.json)
            return res.json
        }
        throw new Error('Network response was not ok.');
    })
    .then(function(e) {
        console.log(e)
    })
    .catch(function(error) {
        console.log('There has been a problem with your fetch operation: ', error.message);
    });

}

const about_host = function (ip){
    console.log("this is about_host")
    console.log(ip)
}