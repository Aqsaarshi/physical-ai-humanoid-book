// API service for chatbot interactions
interface ChatQueryRequest {
  session_id?: string;
  query: string;
  context_mode: 'full-book' | 'selected-text';
  selected_text?: {
    text: string;
    source_metadata: any;
  };
}

interface ChatQueryResponse {
  response_id: string;
  content: string;
  citations: Array<{chapter: string, section: string}>;
}

interface ChatHistoryResponse {
  message_id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: string;
  citations: Array<{chapter: string, section: string}>;
}

class ChatbotApiService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async query(request: ChatQueryRequest): Promise<ChatQueryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/chat/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error querying chatbot:', error);
      throw error;
    }
  }

  async getHistory(sessionId: string): Promise<ChatHistoryResponse[]> {
    try {
      const response = await fetch(`${this.baseUrl}/chat/history/${sessionId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching chat history:', error);
      throw error;
    }
  }
}

export default ChatbotApiService;