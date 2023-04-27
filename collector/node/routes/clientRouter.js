const express = require('express');
const clientRouter = express.Router();
const path = require('path');

clientRouter.use((req, res, next) => {
  console.log('Time: ', Date.now());
  next();
});

clientRouter.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../../client/index.html'));
});

clientRouter.get('/ws.js', function (req, res) {
  res.sendFile(path.join(__dirname, '../../client/ws.js'));
});

module.exports = { clientRouter };
