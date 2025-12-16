import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';

interface Message {
  message_id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: string;
  citations: Array<{ chapter: string; section: string }>;
}

interface ChatbotProps {
  apiUrl: string;
}

const Chatbot: React.FC<ChatbotProps> = ({ apiUrl }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Scroll to bottom when messages update
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  useEffect(scrollToBottom, [messages]);

  // Detect selected text on page
  useEffect(() => {
    const handleSelection = () => {
      const text = window.getSelection()?.toString().trim();
      if (text) setSelectedText(text);
    };
    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      message_id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString(),
      citations: []
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const requestBody = {
        query: inputValue,
        context_mode: selectedText ? 'selected-text' : 'full-book',
        selected_text: selectedText
          ? { text: selectedText, source_metadata: {} }
          : null
      };

      const response = await fetch(`${apiUrl}/api/chat/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();

      const botMessage: Message = {
        message_id: data.response_id,
        content: data.content,
        sender: 'bot',
        timestamp: new Date().toISOString(),
        citations: data.citations || []
      };

      setMessages(prev => [...prev, botMessage]);
      setSelectedText(null); // Clear after sending
    } catch (error) {
      console.error('Error sending message:', error);
      let errorMessageContent = 'Sorry, I encountered an error processing your request.';

      // Check if the error is a network error or API error
      if (error instanceof Error) {
        if (error.message.includes('Failed to fetch')) {
          errorMessageContent = 'Unable to connect to the server. Please make sure the backend is running.';
        } else if (error.message.includes('429') || error.message.toLowerCase().includes('quota')) {
          errorMessageContent = 'The AI service is temporarily unavailable due to quota limits. Please try again later.';
        } else if (error.message.includes('400')) {
          errorMessageContent = 'Invalid request. Please try rephrasing your question.';
        } else if (error.message.includes('500')) {
          errorMessageContent = 'The server encountered an error. Please try again later.';
        }
      }

      const errorMessage: Message = {
        message_id: Date.now().toString(),
        content: errorMessageContent,
        sender: 'bot',
        timestamp: new Date().toISOString(),
        citations: []
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h3>Book Assistant</h3>
        {selectedText && (
          <div className="selected-text-preview">
            <strong>Using selected text:</strong> {selectedText.substring(0, 50)}...
          </div>
        )}
      </div>

      <div className="chatbot-messages">
        {messages.map(msg => (
          <div key={msg.message_id} className={`message ${msg.sender}-message`}>
            <div className="message-content">
              {msg.content}
              {msg.citations.length > 0 && (
                <div className="citations">
                  <strong>Sources:</strong>
                  <ul>
                    {msg.citations.map((c, i) => (
                      <li key={i}>
                        {c.chapter} - {c.section}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chatbot-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          placeholder={selectedText
            ? 'Ask about the selected text...'
            : 'Ask anything about the book...'}
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default Chatbot;
