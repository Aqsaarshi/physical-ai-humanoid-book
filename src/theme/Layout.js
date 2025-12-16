import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatbotContainer from '@site/frontend/src/theme/ChatbotContainer';

export default function Layout(props) {
  return (
    <OriginalLayout {...props}>
      <ChatbotContainer>
        {props.children}
      </ChatbotContainer>
    </OriginalLayout>
  );
}