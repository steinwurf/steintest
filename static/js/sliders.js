// In this file the sliders are defined 
// this files also defines some of the behavoir of buttons etc.



// The slider for the packet size
rangeP = document.getElementById('rangeP'),
rangedivP = document.getElementById('rangedivP'),
setValue = ()=>{
    newValue = Number( (rangeP.value - rangeP.min) * 100 / (rangeP.max - rangeP.min) ),
    newPosition = 10 - (newValue * 0.2);
    rangedivP.innerHTML = `<span>${rangeP.value} </span>`;
    rangedivP.style.left = `calc(${newValue}% + (${newPosition}px))`;
};
document.addEventListener("DOMContentLoaded", setValue);
rangeP.addEventListener('input', setValue);


// The slider for frequency of packets
rangeF = document.getElementById('rangeF'),
rangedivF = document.getElementById('rangedivF'),
setValue = ()=>{
    newValue = Number( (rangeF.value - rangeF.min) * 100 / (rangeF.max - rangeF.min) ),
    newPosition = 10 - (newValue * 0.2);
    rangedivF.innerHTML = `<span>${rangeF.value}</span>`;
    rangedivF.style.left = `calc(${newValue}% + (${newPosition}px))`;
};
document.addEventListener("DOMContentLoaded", setValue);
rangeF.addEventListener('input', setValue);


// The slider for the duration of the test
rangeD = document.getElementById('rangeD'),
rangedivD = document.getElementById('rangedivD'),
setValue = ()=>{
    newValue = Number( (rangeD.value - rangeD.min) * 100 / (rangeD.max - rangeD.min) ),
    newPosition = 10 - (newValue * 0.2);
    rangedivD.innerHTML = `<span>${rangeD.value}</span>`;
    rangedivD.style.left = `calc(${newValue}% + (${newPosition}px))`;
};
document.addEventListener("DOMContentLoaded", setValue);
rangeD.addEventListener('input', setValue);



// The slider for the acceptable delay
rangeA = document.getElementById('rangeA'),
rangedivA = document.getElementById('rangedivA'),
setValue = ()=>{
    newValue = Number( (rangeA.value - rangeA.min) * 100 / (rangeA.max - rangeA.min) ),
    newPosition = 10 - (newValue * 0.2);
    rangedivA.innerHTML = `<span>${rangeA.value}</span>`;
    rangedivA.style.left = `calc(${newValue}% + (${newPosition}px))`;
};
document.addEventListener("DOMContentLoaded", setValue);
rangeA.addEventListener('input', setValue);


var DelaySlider = document.getElementById("DelaySlider");
var startbutton = document.getElementById("startbutton")

var serverPickComponent = document.getElementById("serverpick");


// every time the user picks another server, the server picker is updated and a websocket is created
serverPickComponent.oninput = function(){
    var selectedServer = serverPickComponent.value;
    webSocketConnection = createWebSocketConnection(selectedServer)
  }
// the websocket is first initilized here when the site is loaded
var webSocketConnection = createWebSocketConnection(serverPickComponent.value)

// The start button is clicked, the test is started
startbutton.onclick = startTest