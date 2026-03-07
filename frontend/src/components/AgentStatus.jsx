import { useEffect, useState } from 'react'
import axios from 'axios'

export default function AgentStatus() {
    const [agents, setAgents] = useState([])

    useEffect(() => {
        axios.get('/api/agents/status')
            .then(res => setAgents(res.data.agents))
    }, [])

    return (
        <div className="card agent-status">
            <h2>🤖 Agent Status</h2>
            <div className="agent-list">
                {agents.map((agent, idx) => (
                    <div key={idx} className="agent-item">
                        <span className="agent-dot active"></span>
                        <div>
                            <strong>{agent.name}</strong>
                            <small>{agent.role}</small>
                        </div>
                        <span className="badge">{agent.status}</span>
                    </div>
                ))}
            </div>
        </div>
    )
}
