import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

export default function ChatBox() {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am Jeenora AI. How can I assist you today?' }
    ])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)
    const chatEndRef = useRef(null)

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(scrollToBottom, [messages])

    const sendMessage = async () => {
        if (!input.trim() || loading) return

        const userMsg = { role: 'user', content: input }
        setMessages(prev => [...prev, userMsg])
        setInput("")
        setLoading(true)

        try {
            const res = await axios.post('/api/chat', {
                message: input
            })
            setMessages(prev => [...prev, { role: 'assistant', content: res.data.reply }])
        } catch (err) {
            setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I'm having trouble connecting right now." }])
        }
        setLoading(false)
    }

    return (
        <div className="flex flex-col h-[calc(100vh-250px)] glass-card overflow-hidden">
            <div className="p-6 border-b border-white/10 bg-white/2 flex items-center justify-between">
                <h3 className="text-lg font-bold flex items-center gap-2 text-white">
                    <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
                    Live AI Support
                </h3>
                <span className="text-xs text-text-secondary">Powered by Gemini AI</span>
            </div>

            <div className="flex-1 overflow-y-auto p-8 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
                {messages.map((m, i) => (
                    <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 duration-300`}>
                        <div className={`max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed shadow-lg
                            ${m.role === 'user'
                                ? 'bg-accent text-white rounded-tr-none'
                                : 'bg-white/5 text-text-primary border border-white/10 rounded-tl-none'}`}>
                            {m.content}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start animate-pulse">
                        <div className="bg-white/5 p-4 rounded-2xl rounded-tl-none border border-white/10 space-y-1">
                            <div className="flex gap-1">
                                <span className="w-1.5 h-1.5 bg-text-secondary rounded-full animate-bounce"></span>
                                <span className="w-1.5 h-1.5 bg-text-secondary rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                                <span className="w-1.5 h-1.5 bg-text-secondary rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={chatEndRef} />
            </div>

            <div className="p-6 bg-black/40 border-t border-white/10">
                <div className="flex gap-4">
                    <input
                        className="input-field flex-1"
                        placeholder="Type your message..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    />
                    <button
                        className="btn-primary flex items-center gap-2"
                        onClick={sendMessage}
                        disabled={loading}
                    >
                        Send 🚀
                    </button>
                </div>
            </div>
        </div>
    )
}
