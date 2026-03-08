import { useEffect, useState } from 'react'
import axios from 'axios'

export default function LLMConnect() {
    const [status, setStatus] = useState("Checking...")
    const [stats, setStats] = useState(null)

    useEffect(() => {
        axios.get('/api/health')
            .then(res => setStatus(res.data.status))
            .catch(() => setStatus("Offline"))
    }, [])

    return (
        <div className="max-w-2xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-5 duration-700">
            <div className="glass-card p-10 flex flex-col items-center text-center space-y-6">
                <div className={`w-20 h-20 rounded-full flex items-center justify-center text-3xl shadow-2xl transition-all duration-500
                    ${status === 'healthy' ? 'bg-emerald-500/20 text-emerald-400 border-2 border-emerald-500/50' : 'bg-red-500/20 text-red-400 border-2 border-red-500/50'}`}>
                    {status === 'healthy' ? '⚡' : '❌'}
                </div>
                <div>
                    <h2 className="text-2xl font-bold uppercase tracking-widest text-white">LLM Infrastructure Status</h2>
                    <p className="text-text-secondary mt-2">Checking connectivity to local Ollama & OpenAI Bridge</p>
                </div>
                <div className={`px-6 py-2 rounded-full font-bold text-sm uppercase tracking-widest border
                    ${status === 'healthy' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-300' : 'bg-red-500/10 border-red-500/20 text-red-300'}`}>
                    Connection: {status.toUpperCase()}
                </div>
            </div>

            <div className="grid grid-cols-2 gap-6">
                <div className="glass-card p-6 border-l-4 border-accent">
                    <h4 className="text-xs font-bold text-text-secondary uppercase mb-2">Endpoint URL</h4>
                    <p className="text-sm font-mono text-accent">http://localhost:11434</p>
                </div>
                <div className="glass-card p-6 border-l-4 border-cyan-500">
                    <h4 className="text-xs font-bold text-text-secondary uppercase mb-2">Primary Model</h4>
                    <p className="text-sm font-mono text-cyan-400">gpt-oss:120b-cloud</p>
                </div>
            </div>

            <p className="text-center text-xs text-text-secondary opacity-40">
                Security Tip: Ensure your Ollama server is running locally and CORS is configured correctly.
            </p>
        </div>
    )
}
