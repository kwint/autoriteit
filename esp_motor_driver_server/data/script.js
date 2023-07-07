var gateway = `ws://${window.location.hostname}/ws`;
var websocket;
window.addEventListener('load', onload);
var cmd;

function onload(event) {
    initWebSocket();
}

function initWebSocket() {
    console.log('Trying to open a WebSocket connection…');
    websocket = new WebSocket(gateway);
    websocket.onopen = onOpen;
    websocket.onclose = onClose;
    websocket.onmessage = onMessage;
}

function onOpen(event) {
    console.log('Connection opened');
}

function onClose(event) {
    console.log('Connection closed');
    document.getElementById("motor-state").innerHTML = "motor stopped"
    setTimeout(initWebSocket, 2000);
}

function submitForm(){
    const rbs = document.querySelectorAll('input[name="direction"]');
    cmd;
    for (const rb of rbs) {
        if (rb.checked) {
            cmd = rb.value;
            break;
        }
    }

    document.getElementById("motor-state").innerHTML = "motor spinning...";
    document.getElementById("motor-state").style.color = "blue";
    if (cmd=="CW"){
        document.getElementById("gear").classList.add("spin");
    }
    else{
        document.getElementById("gear").classList.add("spin-back");
    }
    
    var value = document.getElementById("steps").value;
    websocket.send(cmd+"&"+value);
}

function onMessage(event) {
    console.log(event.data);
    cmd = event.data;
    if (cmd=="stop"){ 
      document.getElementById("motor-state").innerHTML = "motor stopped"
      document.getElementById("motor-state").style.color = "red";
      document.getElementById("gear").classList.remove("spin", "spin-back");
    }
    else if(cmd=="CW" || cmd=="CCW"){
        document.getElementById("motor-state").innerHTML = "motor spinning...";
        document.getElementById("motor-state").style.color = "blue";
        if (cmd=="CW"){
            document.getElementById("gear").classList.add("spin");
        }
        else{
            document.getElementById("gear").classList.add("spin-back");
        }
    }
}