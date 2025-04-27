import { useEffect } from 'react';
import React, { useState }from 'react';
import AnalyzeChatArea from './components/analyzeChatArea.jsx';
import './styles/analyzePage.css'; // We'll create this next
import axiosInstance from './utils/axiosInstance';
import SessionSidebar from './sessionsidebar.jsx';
import { v4 as uuidv4 } from 'uuid';


export default function AnalyzePage() {
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [sidebarVisible, setSidebarVisible] = useState(true); // 🔁 toggle state
  // Fetch history 
  useEffect(() => {
    async function fetchSessions() {
      try {
        const res = await axiosInstance.get('/api/analyzer/chat/sessions', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setSessions(res.data.sessions);
      } catch (error) {
        console.error('Error fetching sessions:', error);
      }
    }
    fetchSessions();
  }, []);
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        console.log('Fetching history for session:', sessionId); // Debugging line
        const res = await axiosInstance.get(`/analyze/history/${sessionId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        console.log(res.data.messages); // Check the response structure
        setMessages(res.data.messages);
      } catch (error) {
        console.error('Error fetching analyzer history:', error);
      }
    };
    if (sessionId) fetchHistory();
    }, [sessionId]);
  useEffect(() => {
    setSessionId(uuidv4());
  }, []);
    // Handle session switching
    const handleSelectSession = async (sessionId) => {
      try {
        const res = await axiosInstance.get(`/api/analyzer/chat/history/${sessionId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setActiveSessionId(sessionId);
        setMessages(res.data.messages);
      } catch (error) {
        console.error('Error loading session messages:', error);
      }
    };
    const handleCreateSession = () => {
      setActiveSessionId(null);
      setMessages([]);
    };
  const handleFileUpload = async(file) => {
    setMessages((prev) => [
      ...prev,
      { text: `📄 Uploaded: ${file.name}`, sender: 'user' },
    ]);
    const formData = new FormData();
    formData.append('pdf', file);
    formData.append('session_id', sessionId);
    setIsLoading(true);
    try {
      const res = await axiosInstance.post('/analyze/upload', formData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      setMessages((prev) => [
        ...prev,
        { text: res.data.response || 'PDF analyzed successfully!', sender: 'bot' },
      ]);
    } catch (error) {
      console.error('PDF upload error:', error);
      setMessages((prev) => [
        ...prev,
        { text: '❌ Failed to analyze PDF.', sender: 'bot' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };
  const handleAnalyzeInput = async () => {
    if (!userInput.trim()) return;
    const isURL = /^https?:\/\/\S+$/i.test(userInput.trim());
    setMessages((prev) => [...prev, { text: userInput, sender: 'user' }]);
    setIsLoading(true);
    try {
      const res = await axiosInstance.post('/api/analyze', {
        input: userInput,
        type: isURL ? 'url' : 'text', // pass type to backend
        session_id: sessionId
      });
      setMessages((prev) => [...prev, { text: res.data.response, sender: 'bot' }]);
    } catch (err) {
      console.error('Analyze error:', err);
      setMessages((prev) => [
        ...prev,
        { text: 'Something went wrong analyzing your input.', sender: 'bot' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };
  const handleSendMessage = async(msg,sender) => {
    const timestamp = new Date().toISOString();
    const new_message = { text: msg, sender,timestamp };
    setMessages((prev) => [...prev, new_message]);
    if (sender === 'user') {
      setUserInput(msg);
      try {
        await axiosInstance.post('/analyze/save', {
          text: msg,
          sender,
          session_id: sessionId, // make sure sessionId is tracked in component state
          timestamp,
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
      } catch (err) {
        console.error('Error saving chat:', err);
      }
    }
  };
  return (
    <div className="analyze-page">
    {/* Sidebar */}
    <button
        className="toggle-sidebar-btn"
        onClick={() => setSidebarVisible(!sidebarVisible)}
      >        {sidebarVisible ? "❌" : "📂"}
    </button>
    <div className={`analyze-sidebar ${sidebarVisible ? "visible" : "hidden"}`}>
      <div className="analyze-content">
        <SessionSidebar
          sessions={sessions}
          onSelectSession={handleSelectSession}
          onCreateSession={handleCreateSession}
          activeSessionId={activeSessionId}
        />
      </div>
    </div>

    {/* Main Chat Area */}
    <div className="analyze-main-content">
      {messages.length === 0 ? (
        <div className="analyze-header">
          <h2>Analyze PDF or Web Link</h2>
          <p>Paste a link or upload a PDF and ask questions!</p>
        </div>
      ) : null}

      <AnalyzeChatArea
        onSendMessage={handleSendMessage}
        messages={messages}
        onFileUpload={handleFileUpload}
      />
      {isLoading && <div className="analyze-loading">Analyzing...</div>}
    </div>
  </div>
  );
}
