import { useState } from 'react'

export default function LLMConnect() {
    const [model, setModel] = useState('llama3.1:8b')
    const [status, setStatus] = useState('Connected')

    const models = ['llama3.1:8b', 'gpt-oss:120b-cloud', 'deepseek-r1']

    return (
        <div className="card llm-connect">
            <h2>🔗 LLM Connection</h2>
            <div className="llm-info">
                <div className="llm-row">
                    <label>Active Model:</label>
                    <select value={model} onChange={e => setModel(e.target.value)}>
                        {models.map(m => <option key={m}>{m}</option>)}
                    </select>
                </div>
                <div className="llm-row">
                    <label>Backend:</label>
                    <span className="badge green">Ollama (Local)</span>
                </div>
                <div className="llm-row">
                    <label>Status:</label>
                    <span className="badge green">🟢 {status}</span>
                </div>
                <div className="llm-row">
                    <label>API Cost:</label>
                    <span className="badge">💰 Free</span>
                </div>
            </div>
        </div>
    )
}
