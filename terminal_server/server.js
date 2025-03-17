const express = require("express");
const http = require("http");
const WebSocket = require("ws");
const pty = require("node-pty");

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

wss.on("connection", (ws) => {
  // Start a shell session
  const shell = pty.spawn("bash", [], {
    name: "xterm-color",
    cols: 80,
    rows: 24,
    cwd: process.env.HOME,
    env: process.env,
  });

  // Send shell output to the WebSocket client
  shell.on("data", (data) => {
    ws.send(data);
  });

  // Receive input from the client and send it to the shell
  ws.on("message", (msg) => {
    shell.write(msg);
  });

  // Cleanup when the connection closes
  ws.on("close", () => {
    shell.kill();
  });
});

server.listen(8001, () => {
  console.log("Server running on ws://localhost:8001");
});
