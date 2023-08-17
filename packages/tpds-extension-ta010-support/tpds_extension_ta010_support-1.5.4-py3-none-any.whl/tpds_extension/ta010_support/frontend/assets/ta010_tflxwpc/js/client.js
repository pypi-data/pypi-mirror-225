
function ta010_tflxwpc_json(jsonOBJ) {
  // console.log([String(jsonOBJ)]);
  fetch("http://localhost:5001/ta010/generate_tflxwpc_xml",
    {
      method: "POST",
      body: String(jsonOBJ),

      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function (res) { return res.json(); })
    .then(function (data) {
      if (data.status !== "ABORT") {
        alert(
          "Response: " +
          data.response +
          "\n\nStatus Message:\n" +
          data.status.replace(/(<([^>]+)>)/gi, "")
        );
      }
    })
};

function ta010_tflxwpc_proto_prov(jsonOBJ) {
  // console.log([String(jsonOBJ)]);
  fetch("http://localhost:5001/ta010/provision_tflxwpc_device",
    {
      method: "POST",
      body: String(jsonOBJ),

      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function (res) { return res.json(); })
    .then(function (data) {
      alert('Response: ' + data.response +
        '\n\nStatus Message:\n' + data.status.replace(/(<([^>]+)>)/ig, ""))
    })
};

// check validity for monotonic counter value
const input_counter = document.querySelector('#counterVal');
input_counter.addEventListener('change', (e) => {
  if (!e.target.checkValidity()) {
    e.target.value = ''
  }
  counter_val = document.getElementById("counterVal").value ? document.getElementById("counterVal").value : 10000;
  document.getElementById('limitedUseHMAC').title = 'Connect HMAC Key to Monotonic Counter for ' + counter_val + ' counts';
});

// check validity for device address
const input_address = document.querySelector('#deviceAddress');
input_address.addEventListener('change', (e) => {
  if (!e.target.checkValidity()) {
    e.target.value = ''
  }
  if (e.target.value) {
    const value = parseInt(e.target.value, 16);
    if (value < 1 || value > 127) {
      e.target.value = ''
    }
  }
});