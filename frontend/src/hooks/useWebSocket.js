import { useState, useEffect, useRef } from 'react';

// Define the WebSocket URL based on the backend server location
const WEBSOCKET_URL = 'wss://ethcobackend.onrender.com/ws/';

export const useWebSocket = (clientId) => {
  // State to hold the last message received from the WebSocket
  const [lastMessage, setLastMessage] = useState(null);
  // Ref to hold the WebSocket instance
  const ws = useRef(null);

  useEffect(() => {
    // Do not connect if there is no clientId
    if (!clientId) {
      return;
    }

    // Initialize the WebSocket connection
    const socket = new WebSocket(`${WEBSOCKET_URL}${clientId}`);
    ws.current = socket;

    socket.onopen = () => {
      console.log('WebSocket connected');
      // You could send an initial message here if needed
      setLastMessage({ type: 'connection_status', data: 'connected' });
    };

    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        console.log('Received message:', message);
        setLastMessage(message); // Update state with the new message
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setLastMessage({ type: 'connection_status', data: 'error' });
    };

    socket.onclose = () => {
      console.log('WebSocket disconnected');
      setLastMessage({ type: 'connection_status', data: 'disconnected' });
    };

    // Cleanup function to close the connection when the component unmounts
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [clientId]); // Re-run the effect if the clientId changes

  // The hook returns the last message, allowing components to react to it
  return lastMessage;
};
