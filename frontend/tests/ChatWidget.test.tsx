// frontend/tests/ChatWidget.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ChatWidget from '../src/components/ChatWidget';

interface Message {
  id: number;
  conversation_id: number;
  sender: string;
  content: string;
  timestamp: string;
  citations?: { chapter: string; section: string }[];
}

describe('ChatWidget', () => {
  test('renders input textbox', () => {
    render(<ChatWidget initialMessages={[]} />);
    expect(screen.getByRole('textbox')).toBeInTheDocument();
  });

  test('allows typing in textbox', async () => {
    render(<ChatWidget initialMessages={[]} />);
    const input = screen.getByRole('textbox');
    await userEvent.type(input, 'hello');
    expect(input).toHaveValue('hello');
  });

  test('renders send button', () => {
    render(<ChatWidget initialMessages={[]} />);
    const button = screen.getByRole('button', { name: /send/i });
    expect(button).toBeInTheDocument();
  });

  test('displays messages correctly', () => {
    const messages: Message[] = [
      { id: 1, conversation_id: 1, sender: 'user', content: 'Hello, world!', timestamp: new Date().toISOString() },
      { id: 2, conversation_id: 1, sender: 'bot', content: 'Hi there!', timestamp: new Date().toISOString() },
    ];

    render(<ChatWidget initialMessages={messages} initialConversationId={1} />);
    expect(screen.getByText('Hello, world!')).toBeInTheDocument();
    expect(screen.getByText('Hi there!')).toBeInTheDocument();
  });
});
