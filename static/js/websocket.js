var DelaySlider = document.getElementById("DelaySlider");
var startbutton = document.getElementById("startbutton")

var serverPickComponent = document.getElementById("serverpick");

const finishedTestEvent = new Event("finishedTestEvent")

document.addEventListener("finishedTestEvent", e => {
  webSocketConnection.send(JSON.stringify({type: "packetData", payload :allData})) 
  CreatePlots()
  DisableComponents(false)


})



serverPickComponent.oninput = function(){
  var selectedServer = serverPickComponent.value;

  webSocketConnection = createWebSocketConnection(selectedServer)
}

var webSocketConnection = createWebSocketConnection(serverPickComponent.value)

function createWebSocketConnection(selectedServer){
  if (typeof webSocketConnection !== "undefined"){
    webSocketConnection.close()
  }

  var Connection = new WebSocket(selectedServer)
  console.log("Attempting to connect to server via websocket")

  Connection.onopen = () => {
    console.log("Succesfully connected to via websocket")
  }

  Connection.onclose = (event) => {
    console.log("Websocket closed", event)
  }

  Connection.onerror = (error) => {
    console.log("Websocket error: ", error)
  }

  //Recving data from the server through the web socket
  Connection.onmessage = function(event){
    var data = JSON.parse(event.data)

    switch (data.type){
      case "answer":
        handleAnswer(data)
        break;
      
      case "candidate":
        handleCandidate(data)
    }
  }
  return Connection 
}

function DisableComponents(bool){
  startbutton.disabled = bool
  rangeD.disabled = bool
  rangeF.disabled = bool
  rangeP.disabled = bool
  rangeA.disabled = bool
}

function GetConsLostPacketsFromarray(arr){
  count = 0
  resultArr = []
  for(let i = 0; i < arr.length; i ++){

      if(arr[i] == 0){
          count += 1
          
          if(i == arr.length -1){
              resultArr.push(count)
          }
          continue
      }
      else{
          if(count != 0){
              resultArr.push(count)
          }
          count = 0
      }
  }
  return resultArr
}


function CreatePlots(){
  // Delay histogram 
  DelayHistData = []

  //Something
  IDArray = []

  //LostRecv Plot
  LostRecvData = [0, 0]
  labels = ["Recieved", "Lost"]

  //Consecutive Lost Packets Histogram
  ConsLostPacketData = []
  BinRecvPackets = []

  // Layout 
  var layout = {
    grid: {rows: 2, columns: 2, pattern: 'independent'},
  };


  // Gathering all the data
  for(var i = 0; i < allData.length; i++){
    dataEntry = allData[i]

    // LostRecv Plot
    if (dataEntry.recv == true){
      LostRecvData[0] ++ 
    }
    if (dataEntry.recv == false){
      LostRecvData[1] ++ 
    }

    // Delay histogram data gathering
    DelayHistData.push(dataEntry.delay)


    // Id gathering
    if(dataEntry.recv == true){
      IDArray.push(dataEntry.id)
    }

    // consecutive lost packets
    if(dataEntry.recv == true){
      BinRecvPackets.push(1)
    }else{
      BinRecvPackets.push(0)
    }
  }

  ConsLostPacketData =  GetConsLostPacketsFromarray(BinRecvPackets)

  console.log(BinRecvPackets)
  console.log(ConsLostPacketData)


  var trace1 = {
      name: 'Number of lost and recieved packets',
      y: LostRecvData,
      x: labels,
      type: 'bar',
    };

  var trace2 = {
    name: "Histogram of delays",
    x: DelayHistData,
    type: "histogram",
    xaxis: 'x2',
    yaxis: 'y2',
  }

  var trace3 = {
    name: 'Delay over time',
    y: DelayHistData,
    x: IDArray,
    marker: {},
    type: "bar",
    xaxis: 'x3',
    yaxis: 'y3',
  }

  trace3.marker.color = trace3.y.map(function (v) {
    return v < rangeA.value ? '#009CFF' : 'white'
  });



  var trace4 = {
    name: "Histogram of consecutive lost packet",
    x: ConsLostPacketData,
    type: "histogram",
    xaxis: 'x4',
    yaxis: 'y4',
    nbinsx: 10
  }

  var data = [trace1, trace2, trace3, trace4];
  Plotly.newPlot('plotdiv', data, layout);
}


async function startTest(){
  move()
  DisableComponents(true)
  
  if (typeof rtcPeerConnection == "undefined"){
    createWebRTCConnection()
  }
  else{
    onDataChannelOpen()
  }

}

startbutton.onclick = startTest


// Loading bar test
var i = 0;
function move(currentpacketid) {
    function frame() {
      if (width >= 100) {
        i = 0;
      } else {
        width++;
        elem.style.width = width + "%";
        elem.innerHTML = width + "%";
      }
    }
}

function loadingBar(currentpacketID, TotalNumberOfPackets){
  elem = document.getElementById("myBar");
  width = (currentpacketID / TotalNumberOfPackets) * 100
  console.log(currentpacketID)
  if (width > 100) {
    elem.style.width = "100%";
    elem.innerHTML = "100%";
  } else {
    elem.style.width = Math.round(width) + "%";
    elem.innerHTML = Math.round(width) + "%";
  }
}