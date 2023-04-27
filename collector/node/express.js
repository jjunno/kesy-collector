const express = require('express');
const app = express();
const port = 3000;
const WebSocket = require('ws');

app.get('/', (req, res) => {
  res.send('Hello World!');
});

const { testRouter } = require('./routes/testRouter');
const { clientRouter } = require('./routes/clientRouter');

app.use('/api/test', testRouter);
app.use('/client', clientRouter);

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

/**
 * WS SERVER
 */
const wsApp = app.listen(8080, () => {
  console.log(`Example app listening on port ${8080}`);
});

const wsServer = new WebSocket.Server({
  noServer: true,
}); // a websocket server

wsServer.on('connection', function (ws) {
  // what should a websocket do on connection
  ws.on('message', function (msg) {
    // what to do on message event
    console.log(msg.toString());
    wsServer.clients.forEach(function each(client) {
      if (client.readyState === WebSocket.OPEN) {
        // check if client is ready
        client.send(msg.toString());
      }
    });
  });
});

wsApp.on('upgrade', async function upgrade(request, socket, head) {
  //handling upgrade(http to websocekt) event

  // accepts half requests and rejects half. Reload browser page in case of rejection

  if (Math.random() > 0.5) {
    return socket.end('HTTP/1.1 401 Unauthorized\r\n', 'ascii'); //proper connection close in case of rejection
  }

  //emit connection when request accepted
  wsServer.handleUpgrade(request, socket, head, function done(ws) {
    wsServer.emit('connection', ws, request);
  });
});
