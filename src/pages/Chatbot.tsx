import React from 'react';
import Chatbot from '../../frontend/src/components/Chatbot/Chatbot';

const ChatbotPage = () => {
  // Get the backend URL - safely access environment variables in Docusaurus
  const backendUrl =
    (typeof process !== 'undefined' && process.env?.REACT_APP_API_URL) ||
    (typeof window !== 'undefined' && (window as any).env?.REACT_APP_API_URL) ||
    'http://localhost:8000';

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: "20px 0" }}>
      <h1>📘 Book Assistant</h1>
      <p>Ask questions about the Physical AI & Humanoid Robotics textbook</p>

      <div style={{
        position: "relative",
        height: "600px",
        border: "1px solid #ddd",
        borderRadius: "8px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
      }}>
        <Chatbot apiUrl={backendUrl} />
      </div>
    </div>
  );
};

export default ChatbotPage;