/* websocket Client code */

// Each API must have a specific handle function to catch the
// response from the server.
// The loopback API is implemented for testing purposes and
// as a template for other APIs

// API list. Must be in sync with the server API list
// Each API comes with a msg_id

ws = new WebSocket("ws://localhost:1302/websocket");

function send_message(id, args, _handle){
  var msg = { msg_id: id, parameters: args };
  console.log('send_message', msg)
  send(msg, _handle);
}

function handle_message(evt) {
  var msg = JSON.parse(evt.data)
  if( msg.status == "OK" )
  {
    console.log("handle_message: ", msg.response, "OK")
  }
  else if( msg.status == 'error' )
  {
    console.log("handle_messag: ERROR: ", msg.response)
  }
  console.log('hanlde_message - close socket')
  ws.close()
  console.log('handle_message - close socket')
  var response = msg.response
  console.log('handle_message - response: ', response)
  return response
}

function send(msg, _handle) {
  if( typeof(ws) == 'undefined' || (ws.readyState === undefined) || (ws.readyState > 1)) {
    console.log('send - reopen socket')
    ws = new WebSocket("ws://localhost:1302/websocket");
  } else {
    ws.onmessage = _handle
    ws.send( JSON.stringify(msg));
    // console.log("send sent:", JSON.stringify(msg));
  };
  console.log('handle: ', _handle);
  ws.onopen = function () {
    console.log(_handle)
    console.log('socket re-opened');
    ws.onmessage = _handle
    ws.send( JSON.stringify(msg));
    // console.log("send sent (re-open path):", JSON.stringify(msg));
  }
}

function loopback_handle(evt) {
  // catch the server response
  response = handle_message(evt)
  // do whatever we need with the received response
  document.getElementById('loopback').innerHTML = 'Data back='+response
};

function loopback(arg) {
  send_message(APIs.loopback, [String(arg)], loopback_handle)
};

function json_obj(jsonOBJ) {
  send_message(APIs.json_obj, [String(jsonOBJ)], json_obj_handle)
};

function json_obj_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

function tflex_prov_proto(name) {
  send_message(APIs.tflex_prov_proto, [String(name)], tflex_prov_proto_handle)
};

function tflex_prov_proto_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

function open_link(mdfile, section) {
  send_message(APIs.open_link, [String(mdfile), String(section)], open_link_handle)
};

function open_link_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

APIs = {
  loopback: 0,
  open_link: 3,
  json_obj: 4,
  tflex_prov_proto: 9,
}
