const express = require('express');
const testRouter = express.Router();

testRouter.use((req, res, next) => {
  console.log('Time: ', Date.now());
  next();
});
// define the home page route
testRouter.get('/', (req, res) => {
  // res.send('Birds home page');
  return res.sendStatus(200);
});
// define the about route
testRouter.get('/about', (req, res) => {
  res.send('About birds');
});
module.exports = { testRouter };
