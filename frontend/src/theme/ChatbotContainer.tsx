import React, { useState } from 'react';
import Chatbot from '../components/Chatbot/Chatbot';
import TextSelection from '../components/Chatbot/TextSelection';

interface ChatbotContainerProps {
  children?: React.ReactNode;
  apiUrl?: string;
}

const ChatbotContainer: React.FC<ChatbotContainerProps> = ({ children, apiUrl = 'http://localhost:8000' }) => {
  // Fix: allow null initially or convert null to empty string
  const [selectedText, setSelectedText] = useState<string>('');
  const [isOpen, setIsOpen] = useState(false);

  const handleTextSelected = (text: string) => {
    setSelectedText(text);
  };

  const updateSelectedText = (text: string | null) => {
    // Null safe update
    setSelectedText(text || '');
  };

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="chatbot-container-wrapper">
      {children}

      {/* Floating chatbot button */}
      <button
        className="chatbot-toggle-button"
        onClick={toggleChatbot}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 1000,
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '50%',
          width: '60px',
          height: '60px',
          fontSize: '24px',
          cursor: 'pointer',
          boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
        }}
      >
        💬
      </button>

      {/* Chatbot panel - only show when open */}
      {isOpen && (
        <div
          className="chatbot-panel"
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '20px',
            zIndex: 1000,
            width: '400px',
            height: '500px',
            backgroundColor: 'white',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          <div
            style={{
              padding: '10px',
              borderBottom: '1px solid #eee',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <h3 style={{ margin: 0 }}>Book Assistant</h3>
            <button
              onClick={toggleChatbot}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '18px',
                cursor: 'pointer',
                color: '#666'
              }}
            >
              ×
            </button>
          </div>
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <TextSelection onTextSelected={handleTextSelected} />
            <Chatbot
              apiUrl={apiUrl ||
                (typeof window !== 'undefined' && (window as any).env?.REACT_APP_API_URL) ||
                (typeof process !== 'undefined' && process.env?.REACT_APP_API_URL) ||
                'http://localhost:8000'}
              initialSelectedText={selectedText}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatbotContainer;
