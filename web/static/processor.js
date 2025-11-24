class WorkletProcessor extends AudioWorkletProcessor {
  process(inputs, outputs, parameters) {
    // websocket sent to python somehow
	const WebSocket = require('ws');
	var socket = new WebSocket("ws://127.0.0.1:8000/ws");
	console.log("eeeee");
	sockets[speaker_name][sname] = socket;
	sockets[speaker_name][mic] = mediaRecorder;
	socket.addEventListener("open", (event) => {
		socket.send(inputs);
	});
    console.log(inputs);
    return true;
  }
}

registerProcessor("worklet-processor", WorkletProcessor)