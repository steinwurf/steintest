
// When the test has finished an event is being triggered and this function is called
const finishedTestEvent = new Event("finishedTestEvent")

document.addEventListener("finishedTestEvent", e => {

  CreatePlots()
  NumberOfPackets = allData.length

  PacketLossPercentage = (NumberOfPackets - LostRecvData["Recieved"]) / NumberOfPackets * 100

  ShowTextResults(PacketLossPercentage, NumberOfDelayedPackets)

  webSocketConnection.send(JSON.stringify({type: "packetData", payload :
  {PacketData : allData,
  "PacketLossPercentage": PacketLossPercentage,
  "NumberOfPackets": NumberOfPackets,
  "ConsLostPacketData": ConsLostPacketData,
  "Frequency" : parseInt(rangeF.value),
  "Duration" : parseInt(rangeD.value),
  "AcceptableDelay" : parseInt(rangeA.value),
  "PacketSize" : parseInt(rangeP.value),
  "TimeStamp" : new Date().getTime()
  ,}}))
  
  ChangeStateOfComponents(false)

})

function ShowTextResults(PacketLossPercentage){
  document.getElementById("packetloss").innerHTML = " Total Packetloss: " + PacketLossPercentage.toFixed(1) + "%"
  document.getElementById("delaypercent").innerHTML = "Delayed Packets: " + (NumberOfDelayedPackets / LostRecvData["Recieved"] * 100).toFixed(1) + "%"
}



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
    OpenModal("Error while connecting to server (onerror)")
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

function ChangeStateOfComponents(bool){
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

  NumberOfDelayedPackets = 0

  //LostRecv Plot
  LostRecvData = {"Recieved" : 0, "Lost" : 0}

  //Consecutive Lost Packets Histogram
  ConsLostPacketData = []
  BinRecvPackets = []

  // Gathering all the data
  for(var i = 0; i < allData.length; i++){
    dataEntry = allData[i]

    // LostRecv Plot
    if (dataEntry.recv == true){
      LostRecvData["Recieved"] ++ 
    }
    if (dataEntry.recv == false){
      LostRecvData["Lost"] ++ 
    }

    // consecutive lost packets
    if(dataEntry.recv == true){
      BinRecvPackets.push(1)
    }else{
      BinRecvPackets.push(0)
    }

    // Delayed packets counter
    if(dataEntry.delayed == true){
      NumberOfDelayedPackets ++
    }

    // Delay histogram data gathering
    DelayHistData.push(dataEntry.delay)
  }

  ConsLostPacketData =  GetConsLostPacketsFromarray(BinRecvPackets)

// here it start
  IDArray = range(0, DelayHistData.length - 1)
  delayFigure = {
    name: 'Delay over time',
    y: DelayHistData,
    x: IDArray,
    type: "bar",
    marker: {},
  }

  layoutDelay = {bargap: 10, title : "Delay of packets", xaxis: {title: "ID"}, yaxis: {title: "Delay"},
                shapes: [
                  {
                      type: 'line',
                      xref: 'paper',
                      x0: 0,
                      y0: rangeA.value,
                      x1: 1,
                      y1: rangeA.value,
                      line:{
                          color: 'rgb(255, 0, 0)',
                          width: 1,
                      }
                  }
                ],
                margin: {
                  l: 40,
                  r: 40,
                  b: 50,
                  t: 40,
                  pad: 0
                },        
}

  Plotly.newPlot("firstplot", [delayFigure], layoutDelay, {displayModeBar: false})

  consFigure = {
    name: "Histogram of consecutive lost packet",
    x: ConsLostPacketData,
    type: "histogram",
  }

  consLayout = {title: "Histogram of consecutive lost packets", xaxis: {title: "Number of consecutive lost packets"}, yaxis: {title: "Count"},
                margin: {
                  l: 40,
                  r: 40,
                  b: 50,
                  t: 40,
                  pad: 0
                },  
  }
  Plotly.newPlot("secondplot", [consFigure], consLayout, {displayModeBar: false})
// here it ends
}


async function startTest(){
  ChangeStateOfComponents(true)
  
  // If the websocket is not connected, create a new one
  if (typeof rtcPeerConnection == "undefined"){
    createWebRTCConnection()
  }
  else{
    onDataChannelOpen()
  }

}

function range(start, end) {
  return Array(end - start + 1).fill().map((_, idx) => start + idx)
}

// The functionality of the loading bar
function loadingBar(currentpacketID, TotalNumberOfPackets){
  elem = document.getElementById("myBar");
  width = (currentpacketID / TotalNumberOfPackets) * 100
  if (width > 100) {
    elem.style.width = "100%";
    elem.innerHTML = "100%";
  } else {
    elem.style.width = Math.round(width) + "%";
    elem.innerHTML = Math.round(width) + "%";
  }
}