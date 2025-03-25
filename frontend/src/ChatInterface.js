import React, { useState } from 'react';
import SpeechHandler from './SpeechHandler';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async (text) => {
    const newMessages = [...messages, { sender: 'You', text }];
    setMessages(newMessages);
    
    const response = await fetch('https://your-backend.onrender.com/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: text })
    });
    const data = await response.json();
    
    setMessages([...newMessages, { sender: 'Bot', text: data.response }]);
    SpeechHandler.speak(data.response); // Google TTS
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <p key={index} className={msg.sender}>{msg.sender}: {msg.text}</p>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={() => sendMessage(input)}>Send</button>
      <button onClick={SpeechHandler.listen}>🎙️ Speak</button>
    </div>
  );
};
export default ChatInterface;
