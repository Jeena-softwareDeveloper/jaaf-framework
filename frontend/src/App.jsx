import { useState } from 'react'
import Dashboard from './components/Dashboard'
import AgentStatus from './components/AgentStatus'
import ChatBox from './components/ChatBox'
import LLMConnect from './components/LLMConnect'
import CEOAgent from './components/CEOAgent'
import './index.css'

function App() {
    const [activeTab, setActiveTab] = useState('dashboard')

    return (
        <div className="flex h-screen w-screen bg-bg-main text-text-primary">
            {/* 🧭 Modern Sidebar */}
            <aside className="w-[280px] bg-bg-side border-r border-white/10 flex flex-col p-6 transition-all duration-300">
                <div className="flex items-center gap-3 mb-12 px-2">
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-accent bg-clip-text text-transparent">
                        JAAF AI
                    </h1>
                </div>
                <nav className="flex flex-col gap-2">
                    {[
                        { id: 'dashboard', label: 'Dashboard', icon: '📊' },
                        { id: 'ceo', label: 'Agent Master', icon: '👑' },
                        { id: 'chat', label: 'Live Support', icon: '💬' },
                        { id: 'settings', label: 'LLM Status', icon: '⚙️' },
                    ].map((item) => (
                        <div
                            key={item.id}
                            className={`flex items-center gap-4 px-4 py-3.5 rounded-xl cursor-pointer transition-all duration-200 font-medium group
                                ${activeTab === item.id
                                    ? 'bg-accent/15 text-white border-l-4 border-accent shadow-lg shadow-accent/5'
                                    : 'text-text-secondary hover:bg-white/5 hover:text-accent hover:translate-x-1'}`}
                            onClick={() => setActiveTab(item.id)}
                        >
                            <span className="text-xl group-hover:scale-110 transition-transform">{item.icon}</span>
                            <span className="whitespace-nowrap">{item.label}</span>
                        </div>
                    ))}
                </nav>
            </aside>

            {/* 🖥️ Main Dashboard Area */}
            <main className="flex-1 p-10 overflow-y-auto scroll-smooth">
                <header className="flex justify-between items-center mb-10">
                    <h2 className="text-3xl font-bold tracking-tight">
                        {activeTab === 'ceo' ? 'Agent Master Control' : activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} View
                    </h2>
                    <div className="flex items-center gap-2 bg-success/10 text-success px-4 py-2 rounded-full border border-success/20">
                        <span className="w-2 h-2 bg-success rounded-full animate-pulse"></span>
                        <span className="text-sm font-semibold">System Live</span>
                    </div>
                </header>

                <section className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                    {activeTab === 'dashboard' && <Dashboard />}
                    {activeTab === 'ceo' && <CEOAgent />}
                    {activeTab === 'chat' && (
                        <div className="w-full">
                            <ChatBox />
                        </div>
                    )}
                    {activeTab === 'settings' && (
                        <div className="w-full">
                            <LLMConnect />
                        </div>
                    )}
                </section>
            </main>
        </div>
    )
}

export default App
