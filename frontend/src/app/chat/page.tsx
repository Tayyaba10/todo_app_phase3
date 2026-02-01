'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/lib/auth/auth-context';
import { apiService } from '@/lib/services/api';
import Link from 'next/link';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'agent';
  timestamp: Date;
}

export default function ChatPage() {
  const { user, isAuthenticated } = useAuth();
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // const handleSubmit = async (e: React.FormEvent) => {
  //   e.preventDefault();
  //   if (!inputValue.trim() || isLoading || !user?.id) return;

  //   // Add user message to UI immediately
  //   const userMessage: Message = {
  //     id: Date.now().toString(),
  //     content: inputValue,
  //     sender: 'user',
  //     timestamp: new Date(),
  //   };

  //   setMessages(prev => [...prev, userMessage]);
  //   setInputValue('');
  //   setIsLoading(true);

  //   try {
  //     // Validate that we have a user ID before sending
  //     if (!user?.id) {
  //       throw new Error('User not authenticated properly. Please log in to use the chat.');
  //     }

  //     // Send message to backend API using the service
  //     const response = await apiService.sendMessage(user.id, inputValue);

  //     const { response: agentResponse, conversation_id } = response;

  //     // Add agent response to UI
  //     const agentMessage: Message = {
  //       id: Date.now().toString(),
  //       content: agentResponse,
  //       sender: 'agent',
  //       timestamp: new Date(),
  //     };

  //     setMessages(prev => [...prev, agentMessage]);
  //   } catch (error) {
  //     console.error('Error sending message:', error);

  //     // Add error message to UI
  //     const errorMessage: Message = {
  //       id: Date.now().toString(),
  //       content: error instanceof Error ? error.message : 'Sorry, I encountered an error processing your request. Please try again.',
  //       sender: 'agent',
  //       timestamp: new Date(),
  //     };

  //     setMessages(prev => [...prev, errorMessage]);
  //   } finally {
  //     setIsLoading(false);
  //   }
  // };
  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  if (!inputValue.trim() || isLoading || !user?.sub) return;

  // Add user message to UI immediately
  const userMessage: Message = {
    id: Date.now().toString(),
    content: inputValue,
    sender: 'user',
    timestamp: new Date(),
  };

  setMessages(prev => [...prev, userMessage]);
  const messageToSend = inputValue;
  setInputValue('');
  setIsLoading(true);

  try {
    // Validate that we have a user ID before sending
    if (!user?.sub) {
      throw new Error('User not authenticated properly. Please log in to use the chat.');
    }

    // Send message to backend API using the service
    const response = await apiService.sendMessage(user.sub, messageToSend);
    const { response: agentResponse, conversation_id } = response;

    // Add agent response to UI
    const agentMessage: Message = {
      id: Date.now().toString(),
      content: agentResponse,
      sender: 'agent',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, agentMessage]);
  } catch (error) {
    console.error('Error sending message:', error);

    // Add error message to UI
    const errorMessage: Message = {
      id: Date.now().toString(),
      content: error instanceof Error ? error.message : 'Sorry, I encountered an error processing your request. Please try again.',
      sender: 'agent',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, errorMessage]);
  } finally {
    setIsLoading(false);
  }
};

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Please log in to access the chat interface</h1>
          <Link href="/login" className="text-blue-600 hover:text-blue-800 underline">
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">AI Todo Assistant</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">Welcome, {user?.name || user?.email}</span>
            <Link
              href="/api/auth/logout"
              className="text-sm text-red-600 hover:text-red-800"
            >
              Logout
            </Link>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow">
          <div className="border-b p-4">
            <h2 className="text-xl font-semibold text-gray-900">AI Todo Assistant</h2>
            <p className="text-sm text-gray-600">Manage your tasks with natural language</p>
          </div>

          <div className="h-[500px] flex flex-col">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <h3 className="text-lg font-semibold mb-2">Welcome to your AI Todo Assistant!</h3>
                  <p className="text-gray-600 mb-4">
                    I can help you manage your tasks using natural language. Try saying things like:
                  </p>
                  <ul className="list-disc list-inside text-left text-gray-600 max-w-md">
                    <li>Add a task: Buy groceries</li>
                    <li>Show my tasks</li>
                    <li>Complete the meeting prep task</li>
                    <li>Delete my old task</li>
                  </ul>
                </div>
              ) : (
                <div className="space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                          message.sender === 'user'
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200 text-gray-800'
                        }`}
                      >
                        <div className="whitespace-pre-wrap">{message.content}</div>
                        <div className={`text-xs mt-1 ${message.sender === 'user' ? 'text-blue-200' : 'text-gray-500'}`}>
                          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-gray-200 text-gray-800 max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
                        <div className="flex space-x-2">
                          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              )}
            </div>

            {/* Input */}
            <div className="border-t p-4">
              <form onSubmit={handleSubmit} className="flex gap-2">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type your message here..."
                  className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                  disabled={isLoading || !inputValue.trim()}
                >
                  Send
                </button>
              </form>
              <p className="text-xs text-gray-500 mt-2">
                Example: "Create a task to finish the report", "Show my tasks", "Mark the shopping task as complete"
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
