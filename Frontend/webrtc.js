
batchSize = 50


async function handleAnswer(answer) {
  if (!rtcPeerConnection) {
    console.error('no peerconnection');
    return;
  }
  var remoteSessionDescription = new RTCSessionDescription(answer)
  await rtcPeerConnection.setRemoteDescription(remoteSessionDescription);
  console.log("made connection")
}

async function handleCandidate(data){
  if (!rtcPeerConnection) {
    console.error('no peerconnection');
    return;}
  rtcPeerConnection.addIceCandidate(data.candidate)
    console.log("added remote icecandidate")
}

async function dcHandleMessage(msg){
  var enc = new TextDecoder("utf-8")
  var row = allData[enc.decode(msg.data)]
  row.recvAt = Date.now()
  row.recv = true
  row.delay = row.recvAt - row.sentAt


  if (row.delay <= DelaySlider.value){
    row.delayed = false
  }
  else{
    row.delayed = true
  }
  console.log(row)
}

const timer = ms => new Promise(res => setTimeout(res, ms))

async function sendPackets(batchID){
  for(let i = 0; i < batchSize; i++){
    dataEntry = {}
    dataEntry.id = batchID + i
    dataEntry.sentAt =  Date.now()
    dataEntry.recv = false

    dataChannel.send(String(batchID + i))
    allData.push(dataEntry)
  }
}



// Callback for when the data channel was successfully opened.
async function onDataChannelOpen() {
    var TotalNumberOfPackets = FrequencySlider.value * DurationSlider.value
    SleepTime = 1 / FrequencySlider.value * batchSize

    console.log('Data channel opened!');
    dataChannel.onmessage = dcHandleMessage

    allData = []
    console.log(TotalNumberOfPackets)
    for (let i = 0; i < TotalNumberOfPackets; i += 50){
      sendPackets(i)
      await timer(SleepTime * 1000)
    };
  }
// Callback for when the STUN server responds with the ICE candidates.
function onIceCandidate(event) {
    if (event && event.candidate) {
      webSocketConnection.send(JSON.stringify({type: 'candidate', payload: event.candidate}));
    }
  }
  
  // Callback for when the SDP offer was successfully created.
  function onOfferCreated(description) {
    rtcPeerConnection.setLocalDescription(description);
    webSocketConnection.send(JSON.stringify({type: 'offer', payload: description}));
  }


function createWebRTCConnection(){
    const config = { iceServers: [{ url: 'stun:stun.l.google.com:19302' }] };
    rtcPeerConnection = new RTCPeerConnection(config);
    const dataChannelConfig = { ordered: false, maxRetransmits: 0 };
    dataChannel = rtcPeerConnection.createDataChannel('dc', dataChannelConfig);
    dataChannel.onopen = onDataChannelOpen;
    const sdpConstraints = {
      mandatory: {
        OfferToReceiveAudio: false,
        OfferToReceiveVideo: false,
      },
    };
    rtcPeerConnection.onicecandidate = onIceCandidate;
    rtcPeerConnection.createOffer(onOfferCreated, () => {}, sdpConstraints);
}    