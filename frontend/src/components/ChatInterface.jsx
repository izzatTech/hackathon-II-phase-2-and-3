/**
 * ChatInterface component for the Todo application.
 * Provides an AI chat interface for task management.
 */

import React, { useState, useEffect, useRef } from 'react';
import { useSafeAuth } from '../hooks/useSafeAuth';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentConversationId, setCurrentConversationId] = useState(null);

  const { authToken, isAuthenticated, isLoading: authIsLoading } = useSafeAuth();
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Create new conversation when component mounts
  useEffect(() => {
    if (authToken && !currentConversationId && isAuthenticated) {
      createNewConversation();
    }
  }, [authToken, isAuthenticated]);

  const createNewConversation = async () => {
    if (!authToken) return;

    try {
      const response = await fetch('/api/chat/conversations', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setCurrentConversationId(data.id);
    } catch (err) {
      setError(`Failed to create conversation: ${err.message}`);
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading || !currentConversationId || !authToken) {
      return;
    }

    const userMessage = {
      id: Date.now().toString(),
      content: inputText,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    // Add user message to the chat immediately
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/chat/conversations/${currentConversationId}/messages`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message_content: inputText
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add AI response to the chat
      const aiMessage = {
        id: data.ai_response.id,
        content: data.ai_response.content,
        sender: 'ai',
        timestamp: data.ai_response.timestamp,
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError(`Failed to send message: ${err.message}`);

      // Add error message to the chat
      const errorMessage = {
        id: `error-${Date.now()}`,
        content: `Sorry, I couldn't process your request. Error: ${err.message}`,
        sender: 'ai',
        isError: true,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (authIsLoading) {
    return (
      <div className="chat-interface">
        <div className="chat-placeholder">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="chat-interface">
        <div className="chat-placeholder">
          <p>Please log in to use the AI assistant.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>AI Task Assistant</h2>
        <button onClick={createNewConversation} className="new-chat-button">
          New Chat
        </button>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h3>Hello! I'm your AI task assistant.</h3>
            <p>You can ask me to create, list, update, or complete tasks.</p>
            <p>Try saying: "Add a new task to buy groceries"</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
            >
              <div className="message-content">
                <div className="message-text">{message.content}</div>
                <div className="message-time">{formatTime(message.timestamp)}</div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message ai">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="chat-error">
          {error}
        </div>
      )}

      <div className="chat-input-area">
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here... (e.g., 'Add a task to buy milk')"
          className="chat-input"
          rows="1"
          disabled={isLoading || !currentConversationId}
        />
        <button
          onClick={handleSendMessage}
          disabled={!inputText.trim() || isLoading || !currentConversationId}
          className="send-button"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;