const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.get('/search', (req, res) => {
  const query = req.query.q;

  // Run your Playwright script with the query
  exec(`node script.js "${query}"`, (err, stdout, stderr) => {
    if (err) {
      console.error(`exec error: ${err}`);
      return res.status(500).send(stderr);
    }

    // Send back the Playwright script output
    res.send(stdout);
  });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});