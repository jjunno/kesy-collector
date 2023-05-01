const express = require('express');
const app = express();
const router = express.Router();
const path = require('path');
const axios = require('axios');
require('dotenv').config();

// Env var
EXPRESS_PORT = process.env.EXPRESS_PORT;
HTTP_PORT = process.env.HTTP_PORT;
RECEIVER_API_URL = process.env.RECEIVER_API_URL;
RECEIVER_API_USERNAME = process.env.RECEIVER_API_USERNAME;
RECEIVER_API_PASSWORD = process.env.RECEIVER_API_PASSWORD;

// IO
const http = require('http');
const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server);

let savedSocketId = null;
let savedUuid = null;

/**
 * Client routes serving files
 */
router.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, './index.html'));
});

router.get('/io.js', function (req, res) {
  res.sendFile(
    path.join(__dirname, '../node_modules/socket.io/client-dist/socket.io.js')
  );
});

/**
 * Routes for collector python
 */
// Request location from client
router.get('/api/v1/clientLocation', (req, res) => {
  if (!req.query.uuid) {
    return res.status(400).json({ message: 'Parameter uuid is required' });
  }

  savedUuid = req.query.uuid;
  return res.send(requestClientLocation(savedSocketId));
});

app.use('/', router);

io.on('connection', (socket) => {
  console.log(`Socket ID ${socket.id} connected`);

  savedSocketId = socket.id;
  // requestClientLocation(savedSocketId);

  // Client sends the location data. Send the data to server TODO
  socket.on('clientLocation', (data) => {
    console.log('Received client location');
    console.log(data);
    sendLocationToMasterServer(data);
    return data;
  });

  socket.on('disconnect', () => {
    console.log(`Socket ID ${savedSocketId} disconnected`);
  });
});

/**
 * Request accuracy, latitude and longitude from client.
 * @param {*} socketId
 * @return {void}
 */
function requestClientLocation(socketId) {
  console.log(`Requesting location for socket ID ${socketId}`);
  io.to(socketId).emit('requestClientLocation');
}

/**
 * Send status code from sendLocationToMasterServer to client
 * @param {*} socketId
 * @param {*} status
 * @return {void}
 */
function sendMasterServerStatusToClient(socketId, status) {
  console.log(
    `Sending master server status ${status} to socket ID ${socketId}`
  );
  io.to(socketId).emit('sendMasterServerStatusToClient', status);
}

// App = API
app.listen(EXPRESS_PORT, () => {
  console.log(`API listening on port ${EXPRESS_PORT}`);
});

// HTTP
server.listen(HTTP_PORT, () => {
  console.log(`HTTP listening on port ${HTTP_PORT}`);
});

/**
 * Master server = Node.js Receiver REST API
 * @param {object} data
 * @returns
 */
async function sendLocationToMasterServer(data) {
  try {
    console.log('Sending location to the receiver server');

    let payload = data;
    payload.uuid = savedUuid;

    const response = await axios.put(RECEIVER_API_URL, payload, {
      auth: {
        username: RECEIVER_API_USERNAME,
        password: RECEIVER_API_PASSWORD,
      },
      'content-type': 'application/json',
    });

    if (response.status == 200) {
      console.log('Send success');
    }
    sendMasterServerStatusToClient(savedSocketId, response.status);
  } catch (error) {
    console.log(error);
    console.log('Error when sending location to master server');

    let status = undefined;
    if (error.response && error.response.status) status = error.response.status;
    sendMasterServerStatusToClient(savedSocketId, status);
    return null;
  }
}
