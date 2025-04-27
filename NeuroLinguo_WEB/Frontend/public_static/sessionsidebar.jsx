import React, { useEffect, useState } from 'react';
import './styles/sessionSidebar.css'; 
import axiosInstance from './utils/axiosInstance';

export default function SessionSidebar({ currentSessionId, onSelectSession, onCreateNewSession }) {
  const [sessions, setSessions] = useState([]);
  const [editingSessionId, setEditingSessionId] = useState(null);
  const [editedName, setEditedName] = useState('');

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const res = await axiosInstance.get('/analyze/chat/sessions', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setSessions(res.data.sessions || []);
    } catch (err) {
      console.error('Failed to fetch sessions', err);
    }
  };

  const handleEdit = (sessionId, currentName) => {
    setEditingSessionId(sessionId);
    setEditedName(currentName);
  };

  const handleSaveEdit = async (sessionId) => {
    try {
      await axiosInstance.post(`/analyze/chat/session/rename`, {
        sessionId,
        newName: editedName
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      fetchSessions(); // Refresh list
      setEditingSessionId(null);
    } catch (err) {
      console.error('Rename session failed', err);
    }
  };

  return (
    <div className="session-sidebar">
      <div className="session-header">
        <h3>Sessions</h3>
        <button className="new-session-btn" onClick={onCreateNewSession}>＋</button>
      </div>
      <div className="session-list">
        {sessions.map(session => (
          <div
            key={session.session_id}
            className={`session-item ${currentSessionId === session.session_id ? 'active' : ''}`}
            onClick={() => onSelectSession(session.session_id)}
          >
            {editingSessionId === session.session_id ? (
              <input
                type="text"
                value={editedName}
                onChange={(e) => setEditedName(e.target.value)}
                onBlur={() => handleSaveEdit(session.session_id)}
                autoFocus
              />
            ) : (
              <>
                <span>{session.session_name || session.first_message}</span>
                <button
                  className="edit-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleEdit(session.session_id, session.session_name || session.first_message);
                  }}
                >✏️</button>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
