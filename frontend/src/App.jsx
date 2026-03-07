import Dashboard from './components/Dashboard'
import AgentStatus from './components/AgentStatus'
import ChatBox from './components/ChatBox'
import LLMConnect from './components/LLMConnect'
import './App.css'

function App() {
    return (
        <div className="app-container">
            <header className="header">
                <h1>🧠 Jeenora AI Agent Framework</h1>
                <p>24/7 Business Intelligence Dashboard</p>
            </header>

            <div className="grid">
                <LLMConnect />
                <AgentStatus />
                <Dashboard />
                <ChatBox />
            </div>
        </div>
    )
}

export default App
