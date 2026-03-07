import { useEffect, useState } from 'react'
import axios from 'axios'

export default function AgentStatus() {
    const [agents, setAgents] = useState([])

    useEffect(() => {
        axios.get('/api/agents/list')
            .then(res => setAgents(res.data.agents))
            .catch(err => console.error(err))
    }, [])

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent, i) => (
                <div key={i} className="glass-card p-6 flex items-start gap-4 border-l-4 border-accent hover:border-accent group">
                    <div className="bg-accent/10 p-3 rounded-2xl group-hover:scale-110 transition-transform">
                        <span className="text-2xl">🤖</span>
                    </div>
                    <div className="flex-1 min-w-0">
                        <h3 className="font-bold text-lg text-white truncate">{agent.name}</h3>
                        <p className="text-xs text-accent font-semibold uppercase tracking-wider mb-2">{agent.role}</p>
                        <p className="text-sm text-text-secondary line-clamp-2 italic opacity-80">"{agent.goal}"</p>
                        <div className="mt-4 flex items-center gap-2">
                            <span className="w-2 h-2 bg-success rounded-full shadow-[0_0_8px_#10b981]"></span>
                            <span className="text-[10px] font-bold text-success uppercase">Active</span>
                        </div>
                    </div>
                </div>
            ))}
            {agents.length === 0 && (
                <div className="col-span-full py-20 text-center opacity-30 italic">
                    No active agents registered in the neural network.
                </div>
            )}
        </div>
    )
}
