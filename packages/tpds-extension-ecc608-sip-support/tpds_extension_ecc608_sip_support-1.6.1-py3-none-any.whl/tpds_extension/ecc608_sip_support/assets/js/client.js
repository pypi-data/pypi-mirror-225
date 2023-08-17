/* websocket Client code */

// Each API must have a specific handle function to catch the
// response from the server.
// The loopback API is implemented for testing purposes and
// as a template for other APIs

// API list. Must be in sync with the server API list
// Each API comes with a msg_id

function loopback_handle(evt) {
  // catch the server response
  response = handle_message(evt)
  // do whatever we need with the received response
  document.getElementById('loopback').innerHTML = 'Data back='+response
};

function loopback(arg) {
  send_message(APIs.loopback, [String(arg)], loopback_handle)
};

function get_mplab_path() {
  send_message(APIs.get_mplab_path, null, mplab_path_handle)
}

function mplab_path_handle(evt) {
  response = handle_message(evt)
  document.getElementById('mplab').innerHTML = 'Path='+response
}

function open_notebook(path) {
  send_message(APIs.open_notebook, path, open_notebook_handle)
};

function open_notebook_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

function json_obj(jsonOBJ) {
  send_message(APIs.json_obj, [String(jsonOBJ)], json_obj_handle)
};

function json_obj_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

function tflex_ecc204_json(jsonOBJ) {
  send_message(APIs.tflex_ecc204_json, [String(jsonOBJ)], tflex_ecc204_json_handle)
};

function tflex_ecc204_json_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

function tflex_ecc204_proto_prov(name) {
  send_message(APIs.tflex_ecc204_proto_prov, [String(name)], tflex_ecc204_proto_prov_handle)
};

function tflex_ecc204_proto_prov_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

function active_board(name) {
  send_message(APIs.active_board, [String(name)], active_board_handle)
};

function active_board_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

function get_ta_jsonstr(name) {
  send_message(APIs.get_ta_jsonstr, [String(name)], get_ta_jsonstr_handle)
};

function get_ta_jsonstr_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

function open_ta_app(name) {
  send_message(APIs.open_ta_app, [String(name)], open_ta_app_handle)
};

function open_ta_app_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

function ta_gen_xml(id, bool_val) {
  send_message(APIs.ta_gen_xml, [String(id), bool_val], ta_gen_xml_handle)
};

function ta_gen_xml_handle(evt) {
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

function ta_prov_proto(name) {
    send_message(APIs.ta_prov_proto, [String(name)], ta_prov_proto_handle)
};

function ta_prov_proto_handle(evt) {
    response = handle_message(evt)
    console.log(response)
};

function open_configurator_page(product_name, default_page) {
  send_message(APIs.open_configurator_page, [String(product_name), String(default_page)], open_configurator_page_handle)
};

function open_configurator_page_handle(evt) {
  response = handle_message(evt)
  console.log(response)
  if((response != '') && (response!="OK"))
    window.open(response);
};

function open_link(mdfile, section) {
  send_message(APIs.open_link, [String(mdfile), String(section)], open_link_handle)
};

function open_link_handle(evt) {
  response = handle_message(evt)
  console.log(response)
};

ws = new WebSocket("ws://localhost:1302/websocket");
APIs = {
  loopback: 0,
  get_mplab_path: 1,
  open_notebook: 2,
  open_link: 3,
  json_obj: 4,
  active_board: 5,
  get_ta_jsonstr: 6,
  open_ta_app: 7,
  ta_gen_xml: 8,
  tflex_prov_proto: 9,
  ta_prov_proto: 10,
  open_configurator_page: 15,
  custom_configuration: 16,
  open_default_browser: 17,
  tflex_ecc204_json: 20,
  tflex_ecc204_proto_prov: 21
}
function send_message(id, args, _handle){
  var msg = { msg_id: id, parameters: args };
  console.log('send_message', msg)
  send(msg, _handle);
}

function refresh_ta_config_page(list_json_attr) {
  update_handles(list_json_attr);
}
function handle_message(evt) {
  var msg = JSON.parse(evt.data)
  if( msg.status == "OK" )
  {
    console.log("handle_message: ", msg.response, "OK")
  }
  else if (msg.status == "ta_jsonstr")
  {
    refresh_ta_config_page(msg.response);
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
