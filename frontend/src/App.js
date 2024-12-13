// src/App.js

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState('');
  const [showAbout, setShowAbout] = useState(false);
  const [showTeam, setShowTeam] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const result = await axios.post('http://localhost:5001/chat', { query });
      setMessages([...messages, { type: 'user', text: query }, { type: 'bot', text: result.data.response }]);
      setQuery('');
      setError('');
    } catch (err) {
      console.error('Error details:', err.response || err.message);
      setError('Error occurred while fetching response.');
      setMessages([...messages, { type: 'user', text: query }]);
    }
  };

  const handleOpenAbout = () => setShowAbout(true);
  const handleCloseAbout = () => setShowAbout(false);
  const handleOpenTeam = () => setShowTeam(true);
  const handleCloseTeam = () => setShowTeam(false);

  return (
    <div className="App">
      <header className="App-header">
        <h1>US Visa Chatbot - CS205 Final Project</h1>
        <div className="header-buttons">
          <button className="about-button" onClick={handleOpenAbout}>About</button>
          <button className="about-button" onClick={handleOpenTeam}>Team</button>
        </div>
      </header>
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.type}`}>
              {msg.text}
            </div>
          ))}
          {error && (
            <div className="message error">
              <p>{error}</p>
            </div>
          )}
        </div>
        <form className="input-form" onSubmit={handleSubmit}>
          <input
            id="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your message here..."
          />
          <button type="submit">Send</button>
        </form>
      </div>

      {/* About Modal */}
      {showAbout && (
        <div className="modal-overlay" onClick={handleCloseAbout}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>About</h2>
            <p>This chatbot is designed to assist users with USCIS-related queries.</p>
            <button className="modal-close-button" onClick={handleCloseAbout}>Close</button>
          </div>
        </div>
      )}

      {/* Team Modal */}
      {showTeam && (
        <div className="modal-overlay" onClick={handleCloseTeam}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Meet the Team</h2>
            <div className="team-cards">
              <div className="team-card">
                <h3>Vidit Naik</h3>
                <div className="team-links">
                  <a href="https://www.linkedin.com/in/viditnaik" target="_blank" rel="noopener noreferrer" className="icon-link">
                    <i className="fab fa-linkedin"></i> 
                  </a>
                  <a href="mailto:viditnaik@example.com" className="icon-link">
                    <i className="fas fa-envelope"></i> 
                  </a>
                  <a href="https://github.com/viditnaik" target="_blank" rel="noopener noreferrer" className="icon-link">
                    <i className="fab fa-github"></i> 
                  </a>
                </div>
              </div>
              <div className="team-card">
                <h3>Sai Sreekar Sarvepalli</h3>
                <div className="team-links">
                  <a href="https://www.linkedin.com/in/shauryajobanputra" target="_blank" rel="noopener noreferrer" className="icon-link">
                    <i className="fab fa-linkedin"></i> 
                  </a>
                  <a href="mailto:shauryajobanputra@example.com" className="icon-link">
                    <i className="fas fa-envelope"></i> 
                  </a>
                  <a href="https://github.com/shauryajobanputra" target="_blank" rel="noopener noreferrer" className="icon-link">
                    <i className="fab fa-github"></i> 
                  </a>
                </div>
              </div>
              <div className="team-card">
                <h3>Aum Jasani</h3>
                <div className="team-links">
                  <a href="https://www.linkedin.com/in/prathamgupta" target="_blank" rel="noopener noreferrer" className="icon-link">
                    <i className="fab fa-linkedin"></i> 
                  </a>
                  <a href="mailto:prathamgupta@example.com" className="icon-link">
                    <i className="fas fa-envelope"></i>
                  </a>
                  <a href="https://github.com/prathamgupta" target="_blank" rel="noopener noreferrer" className="icon-link">
                    <i className="fab fa-github"></i> 
                  </a>
                </div>
              </div>
            </div>
            <button className="modal-close-button" onClick={handleCloseTeam}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
