
var FrequencySlider = document.getElementById("FrequencySlider");
var PacketSizeSlider = document.getElementById("PacketSizeSlider");
var DurationSlider = document.getElementById("DurationSlider");
var DelaySlider = document.getElementById("DelaySlider");
var startbutton = document.getElementById("startbutton")



var packetsizeoutput = document.getElementById("packetsizespan");
var frequencyoutput = document.getElementById("frequencyspan");
var durationoutput = document.getElementById("durationspan");
var delayoutput = document.getElementById("delayspan");
var serverPickComponent = document.getElementById("serverpick");


// Controlling the frequency slider and displaying its value
FrequencySliderValue = FrequencySlider.value
frequencyoutput.innerHTML = FrequencySliderValue; 

FrequencySlider.oninput = function() {
    frequencyoutput.innerHTML = this.value;
}

// Controlling the packatsize slider and displaying its value
PacketSizeSliderValue = PacketSizeSlider.value
packetsizeoutput.innerHTML = PacketSizeSliderValue; 

PacketSizeSlider.oninput = function() {
    packetsizeoutput.innerHTML = this.value;
}

// Controlling the duration slider and displaying its value
DurationSliderValue = DurationSlider.value
durationoutput.innerHTML = DurationSliderValue; 

DurationSlider.oninput = function() {
    durationoutput.innerHTML = this.value;
}

// Controlling the delay slider and displaying its value
DelaySliderValue = DelaySlider.value
delayoutput.innerHTML = DelaySliderValue; 

DelaySlider.oninput = function() {
    delayoutput.innerHTML = this.value;
}


serverPickComponent.oninput = function(){
  var selectedServer = serverPickComponent.value;

  webSocketConnection = createWebSocketConnection(selectedServer)
}

var webSocketConnection = createWebSocketConnection(serverPickComponent.value)

function createWebSocketConnection(selectedServer){
  if (typeof webSocketConnection !== "undefined"){
    webSocketConnection.close()
  }

  let Connection = new WebSocket(selectedServer)
  console.log("Attempting to connect to server via websocket")

  Connection.onopen = () => {
    console.log("Succesfully connected to via websocket")
  }

  Connection.onclose = (event) => {
    console.log("Websocket clossed", event)
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
  DelaySlider.disabled = bool
  DurationSlider.disabled = bool
  FrequencySlider.disabled = bool
  PacketSizeSlider.disabled = bool
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
    type: "bar",
    xaxis: 'x3',
    yaxis: 'y3',
  }

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
  DisableComponents(true)
  
  if (typeof rtcPeerConnection == "undefined"){
    createWebRTCConnection()
  }
  else{
    onDataChannelOpen()
  }

  await timer(DurationSlider.value * 1000)

  CreatePlots()

  DisableComponents(false)
  

}

startbutton.onclick = startTest
