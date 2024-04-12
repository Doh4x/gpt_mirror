const axios = require("axios");
const express = require("express");
const app = express();
const eventsource = require("eventsource");
const es = new eventsource(process.env.SSE_ENDPOINT);

es.onmessage = function(event) {
  console.log(JSON.parse(event.data).e)
  axios({
    method:'post',
    url: process.env.DESTINATION_URL,
    data: JSON.parse(event.data).e
  })
}

app.use(express.static("public"));

app.get("/wakeup", function(request, response) {
  console.log("i'm awake");
  response.send("i'm awake")
});

const listener = app.listen(process.env.PORT, function() {
  console.log("I'm waking up on port " + listener.address().port);
});