
batchSize = 50
var TotalNumberOfPackets = rangeF.value * rangeD.value

async function handleAnswer(answer) {
  if (!rtcPeerConnection) {
    console.error('no peerconnection');
    return;
  }
  var remoteSessionDescription = new RTCSessionDescription(answer)
  await rtcPeerConnection.setRemoteDescription(remoteSessionDescription);
}

async function handleCandidate(data){
  if (!rtcPeerConnection) {
    console.error('no peerconnection');
    return;}


  iceCandidate = new RTCIceCandidate(data.candidate)
  console.log("remote icecandidate")
  console.log(iceCandidate)



  rtcPeerConnection.addIceCandidate(iceCandidate)
}

async function dcHandleMessage(msg){
  // chrome and firefox have different ways of handling the message therfore we need to check for both
  
  let firefoxAgent = navigator.userAgent.indexOf("Firefox") > -1;

  if(firefoxAgent){
    decodedId = await msg.data.text()
  }
  else{
    var enc = new TextDecoder("utf-8")
    var decodedId = enc.decode(msg.data)
  }

  let id = decodedId.split(" ")[0]
  var row = allData[id]
  row.recvAt = Date.now()
  row.recv = true
  row.delay = row.recvAt - row.sentAt

  if (row.delay <= rangeA.value){
    row.delayed = false
  }
  else{
    row.delayed = true
  }
}

const timer = ms => new Promise(res => setTimeout(res, ms))

async function sendPackets(batchID){
  var enc = new TextEncoder();

  for(let i = 0; i < batchSize; i++){
    // encoding the data
    // this is done to make sure that the data is the right size for the data channel
    encodedID = enc.encode(batchID + i + " ".repeat(rangeP.value - (batchID + i).toString().length))
    dataEntry = {}
    dataEntry.id = batchID + i
    dataEntry.sentAt =  Date.now()
    dataEntry.recv = false

    dataChannel.send(encodedID)



    allData.push(dataEntry)
  }
}

function onDataChannelClose(){
  console.log("data channel is closed")
}



// Callback for when the data channel was successfully opened.
async function onDataChannelOpen() {
    SleepTime = 1 / rangeF.value * batchSize
    var TotalNumberOfPackets = rangeF.value * rangeD.value

    console.log('Data channel opened!');
    dataChannel.onmessage = dcHandleMessage
    dataChannel.onclose = onDataChannelClose

    allData = []
    console.log(TotalNumberOfPackets)
    for (let i = 0; i < TotalNumberOfPackets + batchSize; i += 50){
      sendPackets(i)
      loadingBar(i, TotalNumberOfPackets)
      await timer(SleepTime * 1000)
    };
    await timer(1 * 1000) 
    document.dispatchEvent(finishedTestEvent)

  }

// Callback for when the STUN server responds with the ICE candidates.
function onIceCandidate(event) {
    console.log("ice is registered and sent")
    console.log(event.candidate)
    if (event && event.candidate) {
      webSocketConnection.send(JSON.stringify({type: 'candidate', payload: event.candidate}));
    }
  }
  
  // Callback for when the SDP offer was successfully created.
function onOfferCreated(description) {
  console.log("offer is created and sent")
  rtcPeerConnection.setLocalDescription(description); 
  webSocketConnection.send(JSON.stringify({type: 'offer', payload: description}));
}

function onConnectionStateChange(event){
  console.log(event)
}
function onIceCandidateError(event){
  console.log(event)
}

function createWebRTCConnection(){
    const config = { iceServers: 
    [
      { 
        urls: 'stun:stun1.l.google.com:19302'
      },
      {
        urls: "turn:142.93.235.90:3478?transport=tcp",
        username: "test",
        credential: "test123"
      },
    ] 
    };

    rtcPeerConnection = new RTCPeerConnection(config);
    rtcPeerConnection.onicecandidate = onIceCandidate;
    rtcPeerConnection.onicecandidateerror = onIceCandidateError


    rtcPeerConnection.addEventListener("connectionstatechange", ev => {
      console.log("the pc is:", rtcPeerConnection.connectionState)
    }, false);

    const dataChannelConfig = { ordered: false, maxRetransmits: 0 };
    dataChannel = rtcPeerConnection.createDataChannel('dc', dataChannelConfig);
    dataChannel.onopen = onDataChannelOpen;

    dataChannel.onerror = (error) => {
      OpenModal("Error while creating the data channel")
      console.log("Data Channel Error:", error);
    };

    dataChannel.onclose = function () {
      console.log("The Data Channel is Closed");
    };

    const sdpConstraints = {
      mandatory: {
        OfferToReceiveAudio: false,
        OfferToReceiveVideo: false,
      },
    };

    rtcPeerConnection.createOffer(onOfferCreated, () => {}, sdpConstraints);

}    
