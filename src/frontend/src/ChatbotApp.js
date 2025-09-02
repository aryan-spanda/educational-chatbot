import React, { useState } from 'react';
import { MessageCircle, BookOpen, Send, X } from 'lucide-react';
import './ChatbotApp.css'; 

export default function ChatbotApp() {
  const [selectedCourse, setSelectedCourse] = useState('');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');

  // Version info for GitOps demo - Updated for CI/CD testing
  const appVersion = "v1.2.1 - CI/CD Pipeline Test (Sept 2, 2025)";

  const courses = [
    { id: 'math101', name: 'Mathematics 101' },
    { id: 'physics201', name: 'Physics 201' },
    { id: 'chemistry150', name: 'Chemistry 150' },
    { id: 'biology110', name: 'Biology 110' },
    { id: 'english102', name: 'English Literature 102' },
    { id: 'history200', name: 'World History 200' }
  ];

  const handleCourseSelect = (courseId) => {
    setSelectedCourse(courseId);
    const course = courses.find(c => c.id === courseId);
    if (course) {
      setMessages([{
        id: Date.now(),
        text: `Hi! I'm your ${course.name} assistant. How can I help you today?`,
        isBot: true,
        timestamp: new Date()
      }]);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const newMessage = {
      id: Date.now(),
      text: inputMessage,
      isBot: false,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newMessage]);

    // Simulate bot response with indicator
    const typingMessage = {
      id: Date.now() + 0.5,
      text: 'Thinking...',
      isBot: true,
      timestamp: new Date(),
      isTyping: true
    };

    setMessages(prev => [...prev, typingMessage]);

    try {
      // Construct and send the request
      await new Promise(resolve => setTimeout(resolve, 1000));
        const response = await
        fetch('http://127.0.0.1:8000/ask/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({question : inputMessage}) //user message from state
        });
        
        // Check if the API responded successfully
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        // Get the JSON data from the response
        const data = await response.json();
        let botText = '';

        // Handle the new response structure
        if (data.error) {
          // If there's an error in the response
          botText = data.error;
        } else {
          // Collect all response data into a single formatted string
          let responseText = '';
          
          // Add final answer first (most important for users)
          if (data.answer) {
            if (Array.isArray(data.answer)) {
              responseText += data.answer.join(' ');
            } else {
              responseText += data.answer;
            }
            responseText += '\n\n';
          }
          
          // Add detailed information section
          responseText += '📚 Additional Context:\n\n';
          
          // Add filtered questions if they exist
          if (data.filtered_questions && Array.isArray(data.filtered_questions) && data.filtered_questions.length > 0) {
            responseText += '🔍 Related Questions Analyzed:\n';
            data.filtered_questions.forEach((q, index) => {
              responseText += `• ${q.q}\n`;
            });
            responseText += '\n';
          }
          
          // Add summarized chunks if they exist
          if (data.summarized_chunks && Array.isArray(data.summarized_chunks) && data.summarized_chunks.length > 0) {
            responseText += '📖 Supporting Information:\n';
            data.summarized_chunks.forEach((chunk, index) => {
              if (chunk.search_results && Array.isArray(chunk.search_results)) {
                chunk.search_results.forEach(result => {
                  // Clean up the bullet points and formatting
                  let cleanResult = result.replace(/\*/g, '•').trim();
                  responseText += `${cleanResult}\n\n`;
                });
              }
            });
          }
          
          botText = responseText || 'Sorry, I received an unexpected response format.';
        }

        // Create the bot response message
        const botResponse = {
          id: Date.now(),
          text: botText,
          isBot: true,
          timestamp: new Date()
        };

        // Update the UI
        setMessages(prev => {
          const withoutTyping = prev.filter(msg => !msg.isTyping);
          return [...withoutTyping, botResponse];
        });

    }

    catch(error) {
      // if fetch fails or response was not ok
      console.error('Error fetching response:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I could not process your request. Please try again later.',
        isBot: true,
        timestamp: new Date()
      };

      // Update the UI
        setMessages(prev => {
          const withoutTyping = prev.filter(msg => !msg.isTyping);
          return [...withoutTyping, errorMessage];
        });
    }

    setInputMessage('');
  };

  const toggleChat = () => {
    if (!selectedCourse) {
      alert('Please select a course first!');
      return;
    }
    setIsChatOpen(!isChatOpen);
  };

  const closeChat = () => {
    setIsChatOpen(false);
  };

  const resetChat = () => {
    const course = courses.find(c => c.id === selectedCourse);
    if (course) {
      setMessages([{
        id: Date.now(),
        text: `Hi! I'm your ${course.name} assistant. How can I help you today?`,
        isBot: true,
        timestamp: new Date()
      }]);
    }
  };

  return (
    <div className="chatbot-app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <BookOpen className="header-icon" />
          <h1>AI Course Assistant - Pola Edition 🚀 CI/CD Test</h1>
          <p>Select a course and start chatting with your AI assistant</p>
          <p className="pola-text">🚀 Pola GitOps Testing - ArgoCD Auto-Update Demo 🚀</p>
          <small className="version-info">{appVersion}</small>
        </div>
      </header>

      {/* Course Selection */}
      <div className="course-selection">
        <h2>Choose Your Course</h2>
        <div className="course-grid">
          {courses.map((course) => (
            <button
              key={course.id}
              onClick={() => handleCourseSelect(course.id)}
              className={`course-card ${selectedCourse === course.id ? 'selected' : ''}`}
            >
              <BookOpen size={24} />
              <span>{course.name}</span>
              {selectedCourse === course.id && <div className="selected-indicator">✓</div>}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Toggle Button */}
      {selectedCourse && (
        <button 
          onClick={toggleChat}
          className="chat-toggle-btn"
          title="Start conversation"
        >
          <MessageCircle size={24} />
        </button>
      )}

      {/* Chat Window */}
      {isChatOpen && (
        <div className="chat-overlay">
          <div className="chat-window">
            {/* Chat Header */}
            <div className="chat-header">
              <div className="chat-title">
                <MessageCircle size={20} />
                <span>{courses.find(c => c.id === selectedCourse)?.name} Assistant</span>
              </div>
              <div className="chat-controls">
                <button onClick={resetChat} className="reset-btn" title="Reset chat">
                  🔄
                </button>
                <button onClick={closeChat} className="close-btn" title="Close chat">
                  <X size={20} />
                </button>
              </div>
            </div>

            {/* Messages Area */}
            <div className="messages-container">
              {messages.length === 0 ? (
                <div className="empty-chat">
                  <MessageCircle size={48} />
                  <p>Start a conversation with your course assistant!</p>
                </div>
              ) : (
                messages.map((message) => (
                  <div
                    key={message.id}
                    className={`message ${message.isBot ? 'bot-message' : 'user-message'}`}
                  >
                    <div className="message-content">
                      <div className="message-text">
                        {message.isTyping ? (
                          <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                          </div>
                        ) : (
                          <div style={{ whiteSpace: 'pre-line' }}>
                            {message.text}
                          </div>
                        )}
                      </div>
                      <div className="message-time">
                        {message.timestamp.toLocaleTimeString([], { 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Input Area */}
            <form onSubmit={handleSendMessage} className="message-input-form">
              <div className="input-container">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Ask a question about your course..."
                  className="message-input"
                />
                <button 
                  type="submit" 
                  className="send-button"
                  disabled={!inputMessage.trim()}
                >
                  <Send size={18} />
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}