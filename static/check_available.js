function checkAvailable(){
    var xhttp = new XMLHttpRequest();
    var uname = document.getElementById("uname").value;
    xhttp.open("get","/check/"+uname, true);
    xhttp.send();

    xhttp.onreadystatechange = function() {
        if(this.readyState == 4) {
            if(this.responseText == "available" || this.responseText == "unavailable"){
            document.getElementById("availability").innerHTML = this.responseText;
            } else {
            document.getElementById("availability").innerHTML = '';
            }
        }
    };
}