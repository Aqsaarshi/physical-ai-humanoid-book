import React from 'react';
import ChatbotContainer from '../../frontend/src/theme/ChatbotContainer';

const LayoutWrapper = ({ children }) => {
  return (
    <ChatbotContainer>
      {children}
    </ChatbotContainer>
  );
};

export default LayoutWrapper;