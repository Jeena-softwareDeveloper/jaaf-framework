import { useState } from 'react'
import axios from 'axios'

export default function ChatBox() {
    const [messages, setMessages] = useState([
        { from: 'bot', text: 'Hello! I am Jeenora AI Support. How can I help you?' }
    ])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)

    const sendMessage = async () => {
        if (!input.trim()) return
        const userMsg = { from: 'user', text: input }
        setMessages(prev => [...prev, userMsg])
        setInput('')
        setLoading(true)

        const res = await axios.post('/api/chat', { message: input })
        const botMsg = { from: 'bot', text: res.data.reply }
        setMessages(prev => [...prev, botMsg])
        setLoading(false)
    }

    return (
        <div className="card chatbox">
            <h2>💬 Customer Support Chat</h2>
            <div className="chat-history">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`msg ${msg.from}`}>
                        <span>{msg.text}</span>
                    </div>
                ))}
                {loading && <div className="msg bot"><span>⏳ Thinking...</span></div>}
            </div>
            <div className="chat-input">
                <input
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && sendMessage()}
                    placeholder="Ask anything about Jeenora..."
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    )
}
