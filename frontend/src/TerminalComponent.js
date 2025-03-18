import React, { useEffect, useRef } from "react";
import { Terminal } from "@xterm/xterm";
import { FitAddon } from "@xterm/addon-fit";
import { WebglAddon } from "@xterm/addon-webgl";
import "@xterm/xterm/css/xterm.css";

const TerminalComponent = () => {
  const terminalRef = useRef(null);
  const socketRef = useRef(null);
  const term = useRef(null);

  useEffect(() => {
    // Initialize WebSocket
    const socket = new WebSocket("ws://127.0.0.1:8001/ws/terminal/");
    socketRef.current = socket;

    // Create xterm.js instance
    const terminal = new Terminal({
      cursorBlink: true,
      fontSize: 14,
      theme: { background: "#000000", foreground: "#ffffff" },
    });

    // Load fit and WebGL addons
    const fitAddon = new FitAddon();
    terminal.loadAddon(fitAddon);
    
    // Attach terminal to DOM
    terminal.open(terminalRef.current);
    
    // Make sure the container has dimensions before fitting
    setTimeout(() => {
      fitAddon.fit();
      
      // Only load WebGL after terminal is properly sized
      try {
        const webglAddon = new WebglAddon();
        terminal.loadAddon(webglAddon);
      } catch (e) {
        console.warn('WebGL addon could not be loaded', e);
      }
    }, 100);

    // Handle window resize
    const handleResize = () => {
      try {
        fitAddon.fit();
      } catch (e) {
        console.warn('Error resizing terminal', e);
      }
    };
    
    window.addEventListener('resize', handleResize);

    // Handle user input
    terminal.onData((data) => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(data);
      }
    });

    // Handle incoming messages
    socket.onmessage = (event) => {
      terminal.write(event.data);
    };

    // Handle disconnect
    socket.onclose = () => {
      terminal.write("\r\nConnection closed.\r\n");
    };

    term.current = terminal;

    return () => {
      window.removeEventListener('resize', handleResize);
      socket.close();
      terminal.dispose();
    };
  }, []);

  return <div ref={terminalRef} style={{ height: "100vh", width: "100%", overflow: "hidden" }} />;
};

export default TerminalComponent;
