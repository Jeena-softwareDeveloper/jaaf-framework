import { useEffect, useState } from 'react'
import axios from 'axios'

export default function CEOAgent() {
    const [agents, setAgents] = useState([])
    const [selectedAgent, setSelectedAgent] = useState(null)
    const [report, setReport] = useState("")
    const [running, setRunning] = useState(false)
    const [saving, setSaving] = useState(false)
    const [message, setMessage] = useState("")
    const [logMessage, setLogMessage] = useState("Ready.")
    const [agentStatuses, setAgentStatuses] = useState({})

    const roleTemplates = {
        "CEO": {
            goal: "Ensure overall profit, business growth, and departmental synergy across all Jeenora sectors.",
            backstory: "You are the Digital CEO of Jeenora. You coordinate between the COO, CTO, and other department heads to make data-driven strategic decisions."
        },
        "COO": {
            goal: "Optimize operational efficiency, logistics, and supply chain management for maximum productivity.",
            backstory: "Reporting directly to the CEO, you are the operations mastermind ensuring every department functions like clockwork."
        },
        "CTO": {
            goal: "Define and execute the technology roadmap, ensuring system stability and leading technical innovation.",
            backstory: "You lead the engineering teams and report to the CEO. You ensure JAAF AI remains at the cutting edge of industry technology."
        },
        "CFO": {
            goal: "Maintain financial health, manage budgets, and mitigate financial risks to ensure long-term sustainability.",
            backstory: "As the chief financial architect reporting to the CEO, you handle the complex economics of Jeenora's multi-sector business."
        },
        "CMO": {
            goal: "Drive brand awareness, customer acquisition, and market positioning across all digital and offline channels.",
            backstory: "Reporting to the CEO, you lead the marketing agents to create compelling narratives for Jeenora's products."
        },
        "Software Architect": {
            goal: "Design robust, scalable, and secure system architectures for the JAAF framework.",
            backstory: "Reporting to the CTO and CEO, you ensure the technical foundation is strong enough to support millions of transactions."
        },
        "Full Stack Developer": {
            goal: "Build and maintain end-to-end features for the Jeenora dashboard and core services.",
            backstory: "A versatile engineer in the tech department. You report to the CTO and CEO to deliver seamless user experiences."
        },
        "Agri Manager": {
            goal: "Optimize crop yields, seed distribution, and farmer relations in the Jeenora Agri sector.",
            backstory: "The ground commander of the agriculture department. You report operational stats directly to the CEO for strategic planning."
        },
        "Fashion Scout": {
            goal: "Identify trending fashion designs and maintain optimal stock levels in the clothing warehouse.",
            backstory: "A trend-spotter with an eye for quality. You report inventory levels and market fashion trends to the CEO."
        },
        "CRM Lead": {
            goal: "Maximize customer retention and convert new business leads into loyal Jeenora partners.",
            backstory: "Expert in relationship building. You bridge the gap between sales and technology, reporting high-value leads to the CEO."
        },
        "SEO Specialist": {
            goal: "Dominant online visibility and search engine rankings for Jeenora's web properties.",
            backstory: "A digital growth hacker. You analyze search patterns and report market intelligence directly to the CEO."
        },
        "Support Agent": {
            goal: "Provide instant, empathetic, and accurate resolutions to all customer queries.",
            backstory: "The voice of Jeenora. You manage front-line communications and flag critical issues to the CEO."
        }
    }

    const handleRoleChange = (role) => {
        if (role === 'ALL_CORE') {
            setSelectedAgent({
                ...selectedAgent,
                role: 'ALL_CORE',
                name: 'System Core Initialization',
                goal: 'Auto-generate and configure all essential Jeenora AI Agents.',
                backstory: 'System will initialize: CEO, Agri Manager, Fashion Scout, CRM Lead, SEO Specialist, and Support Agent with the selected LLM and Temperature.',
                target_url: '',
                git_repo: ''
            });
            return;
        }

        const template = roleTemplates[role] || { goal: '', backstory: '' };
        setSelectedAgent({
            ...selectedAgent,
            role: role,
            goal: template.goal,
            backstory: template.backstory,
            name: selectedAgent.name === 'System Core Initialization' ? `Jeenora ${role}` : (selectedAgent.name || `Jeenora ${role}`),
            target_url: selectedAgent.target_url || '',
            git_repo: selectedAgent.git_repo || ''
        });
    }

    useEffect(() => {
        fetchAgents()
    }, [])

    const fetchAgents = async () => {
        try {
            const res = await axios.get('/api/agents/list')
            if (res.data.success) {
                setAgents(res.data.agents)
                if (res.data.agents.length > 0 && !selectedAgent) {
                    setSelectedAgent(res.data.agents[0])
                }
            }
        } catch (err) {
            console.error("Failed to fetch agents", err)
        }
    }

    const handleSave = async () => {
        setSaving(true)
        setMessage("")

        if (selectedAgent.role === 'ALL_CORE') {
            try {
                const coreRoles = ["CEO", "Agri Manager", "Fashion Scout", "CRM Lead", "SEO Specialist", "Support Agent"];
                for (let r of coreRoles) {
                    const template = roleTemplates[r];
                    const newAgent = {
                        name: `Jeenora ${r}`,
                        role: r,
                        goal: template.goal,
                        backstory: template.backstory,
                        model: selectedAgent.model || 'gpt-oss:120b-cloud',
                        temperature: selectedAgent.temperature || 0.7
                    };
                    await axios.post('/api/agents/save', newAgent);
                }
                setMessage("✅ All Core System Agents generated successfully!");
                await fetchAgents();
                setTimeout(() => setMessage(""), 3000);
            } catch (err) {
                setMessage("❌ Failed to generate core system agents.");
            }
            setSaving(false);
            return;
        }

        try {
            const res = await axios.post('/api/agents/save', selectedAgent)
            if (res.data.success) {
                setMessage("✅ Agent saved successfully!")
                await fetchAgents()
                setTimeout(() => setMessage(""), 3000)
            }
        } catch (err) {
            setMessage("❌ Failed to save agent.")
        }
        setSaving(false)
    }

    const handleDelete = async () => {
        if (!selectedAgent?.id) return
        if (!window.confirm("Are you sure you want to delete this agent?")) return

        try {
            const res = await axios.delete(`/api/agents/${selectedAgent.id}`)
            if (res.data.success) {
                setSelectedAgent(null)
                await fetchAgents()
            }
        } catch (err) {
            console.error("Delete failed", err)
        }
    }

    const runMasterStrategy = () => {
        setRunning(true)
        setReport("")
        setLogMessage("Connecting to Master Controller...")

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const socket = new WebSocket(`${protocol}//${window.location.hostname}:8000/ws/ceo`);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.status === "starting") setLogMessage(data.message);
            else if (data.agent) setAgentStatuses(prev => ({ ...prev, [data.agent]: data.status }));
            else if (data.status === "thinking") setLogMessage(data.message);
            else if (data.status === "complete") {
                simulateStreaming(data.report);
                setLogMessage("✅ Strategy cycle complete.");
                setRunning(false);
            } else if (data.status === "error") {
                setLogMessage("❌ Error: " + data.message);
                setRunning(false);
            }
        };
    };

    const simulateStreaming = async (text) => {
        let currentText = ""
        const words = text.split(" ")
        for (let i = 0; i < words.length; i++) {
            currentText += words[i] + " "
            setReport(currentText)
            await new Promise(resolve => setTimeout(resolve, 20))
        }
    }

    return (
        <div className="flex gap-6 h-[calc(100vh-180px)] animate-in fade-in zoom-in-95 duration-500">
            {/* 📁 Left Sidebar: Agent List */}
            <div className="flex flex-col w-[320px] bg-bg-side border border-white/10 rounded-[24px] overflow-hidden shadow-2xl">
                <div className="p-6 bg-white/2 border-bottom border-white/10 flex justify-between items-center">
                    <h3 className="text-lg font-semibold tracking-tight text-white">Agents List</h3>
                    <button
                        className="bg-emerald-500 hover:bg-emerald-600 text-white px-3 py-1.5 rounded-lg text-sm font-medium transition-all active:scale-95"
                        onClick={handleAddNew}
                    >
                        + Add New
                    </button>
                </div>
                <div className="flex-1 overflow-y-auto p-3 space-y-2">
                    {agents.map(a => (
                        <div
                            key={a.id}
                            className={`flex items-center gap-4 p-4 rounded-xl cursor-pointer transition-all duration-300 border
                                ${selectedAgent?.id === a.id
                                    ? 'bg-accent/10 border-accent/50 shadow-inner'
                                    : 'border-transparent hover:bg-white/5 active:scale-[0.98]'}`}
                            onClick={() => setSelectedAgent(a)}
                        >
                            <span className="text-2xl drop-shadow-glow">🤖</span>
                            <div className="flex-1 min-w-0">
                                <strong className="block text-sm font-semibold truncate text-white">{a.name}</strong>
                                <small className="text-xs text-text-secondary truncate block italic opacity-70">{a.role}</small>
                            </div>
                        </div>
                    ))}
                    {agents.length === 0 && (
                        <p className="text-center py-10 text-text-secondary opacity-50 italic">No agents found.</p>
                    )}
                </div>
            </div>

            {/* ⚙️ Right Content: Configuration & Controls */}
            <div className="flex-1 bg-bg-side border border-white/10 rounded-[24px] overflow-y-auto p-10 shadow-2xl custom-scrollbar relative">
                {selectedAgent ? (
                    <div className="space-y-10">
                        <div className="flex justify-between items-center">
                            <h2 className="text-2xl font-bold tracking-tighter text-white uppercase italic">
                                {selectedAgent.id ? 'Edit Agent' : 'Create New Agent'}
                            </h2>
                            <div className="flex gap-3">
                                {selectedAgent.id && (
                                    <button
                                        className="bg-red-500/80 hover:bg-red-600 text-white px-4 py-2 rounded-xl transition-all font-medium active:scale-95"
                                        onClick={handleDelete}
                                    >
                                        🗑️ Delete
                                    </button>
                                )}
                                <button
                                    className="btn-primary"
                                    onClick={handleSave}
                                    disabled={saving}
                                >
                                    {saving ? "⏳ Saving..." : "💾 Save Agent"}
                                </button>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-text-secondary uppercase tracking-[0.1em] ml-1">Agent Name</label>
                                <input
                                    className="input-field w-full"
                                    type="text"
                                    value={selectedAgent.name}
                                    onChange={(e) => setSelectedAgent({ ...selectedAgent, name: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-text-secondary uppercase tracking-[0.1em] ml-1">Role</label>
                                <select
                                    className="input-field w-full appearance-none cursor-pointer"
                                    value={selectedAgent.role}
                                    onChange={(e) => handleRoleChange(e.target.value)}
                                >
                                    <option value="">Select a Role...</option>
                                    <option value="ALL_CORE" className="text-emerald-400 bg-[#0d0d1a] font-bold">🌟 AUTO-GENERATE CORE AGENTS SET</option>
                                    <optgroup label="Core Leadership">
                                        <option value="CEO">👑 CEO (Master Controller)</option>
                                        <option value="COO">⚙️ COO (Operations Chief)</option>
                                        <option value="CTO">💻 CTO (Technology Chief)</option>
                                        <option value="CFO">💰 CFO (Finance Chief)</option>
                                        <option value="CMO">📢 CMO (Marketing Chief)</option>
                                    </optgroup>
                                    <optgroup label="Tech & Development">
                                        <option value="Software Architect">🏗️ Software Architect</option>
                                        <option value="Full Stack Developer">🌐 Full Stack Developer</option>
                                        <option value="Frontend Developer">🎨 Frontend Developer</option>
                                        <option value="Backend Developer">🖥️ Backend Developer</option>
                                        <option value="Mobile App Developer">📱 Mobile Developer</option>
                                        <option value="DevOps Engineer">🚀 DevOps Engineer</option>
                                        <option value="AI/ML Engineer">🧠 AI/ML Specialist</option>
                                        <option value="Data Scientist">📊 Data Scientist</option>
                                        <option value="QA Engineer">🧪 QA / Test Engineer</option>
                                    </optgroup>
                                    <optgroup label="Management & Product">
                                        <option value="Product Manager">🎯 Product Manager</option>
                                        <option value="Project Manager">📅 Project Manager</option>
                                        <option value="HR Manager">👥 HR Manager</option>
                                        <option value="Finance Manager">🏦 Finance Manager</option>
                                        <option value="Operations Manager">🏢 Operations Manager</option>
                                    </optgroup>
                                    <optgroup label="Jeenora Specialized">
                                        <option value="Agri Manager">🌾 Agri / Farmer Manager</option>
                                        <option value="Fashion Scout">👗 Fashion / Dress Manager</option>
                                        <option value="CRM Lead">📞 CRM Specialist</option>
                                        <option value="SEO Specialist">🔍 SEO Agent</option>
                                        <option value="Support Agent">💬 Customer Support</option>
                                    </optgroup>
                                    <optgroup label="Marketing & Sales">
                                        <option value="Content Strategist">✍️ Content Strategist</option>
                                        <option value="Social Media Manager">📱 Social Media Manager</option>
                                        <option value="Sales Representative">🤝 Sales Representative</option>
                                        <option value="Growth Hacker">📈 Growth Hacker</option>
                                    </optgroup>
                                    <optgroup label="Finance & Admin">
                                        <option value="Accountant">💴 Accountant</option>
                                        <option value="Financial Analyst">📈 Financial Analyst</option>
                                        <option value="Legal Counsel">⚖️ Legal Counsel</option>
                                        <option value="Admin Assistant">📧 Admin Assistant</option>
                                    </optgroup>
                                </select>
                            </div>
                            {selectedAgent.role && (
                                <div className="col-span-2 bg-white/5 border border-white/10 p-5 rounded-2xl relative overflow-hidden group">
                                    <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-accent to-emerald-500"></div>
                                    <h4 className="text-xs font-bold text-accent mb-3 uppercase tracking-widest flex items-center gap-2">
                                        <span className="text-lg">📋</span> System Directives Auto-Loaded
                                    </h4>
                                    <div className="space-y-2">
                                        <p className="text-sm text-text-secondary leading-relaxed">
                                            <strong className="text-white tracking-wide">Goal:</strong> {selectedAgent.goal}
                                        </p>
                                        <p className="text-sm text-text-secondary leading-relaxed">
                                            <strong className="text-white tracking-wide">Backstory:</strong> {selectedAgent.backstory}
                                        </p>
                                    </div>
                                </div>
                            )}
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-text-secondary uppercase tracking-[0.1em] ml-1">Deep Analyze Website</label>
                                <div className="relative group">
                                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-lg group-focus-within:text-accent transition-colors">🌐</span>
                                    <input
                                        className="input-field w-full pl-12"
                                        placeholder="https://your-site.com"
                                        value={selectedAgent.target_url || ""}
                                        onChange={(e) => setSelectedAgent({ ...selectedAgent, target_url: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-text-secondary uppercase tracking-[0.1em] ml-1">Git Repository (Auto-Update)</label>
                                <div className="relative group">
                                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-lg group-focus-within:text-accent transition-colors">🔗</span>
                                    <input
                                        className="input-field w-full pl-12"
                                        placeholder="https://github.com/user/repo"
                                        value={selectedAgent.git_repo || ""}
                                        onChange={(e) => setSelectedAgent({ ...selectedAgent, git_repo: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-text-secondary uppercase tracking-[0.1em] ml-1">LLM Model</label>
                                <select
                                    className="input-field w-full appearance-none cursor-pointer"
                                    value={selectedAgent.model}
                                    onChange={(e) => setSelectedAgent({ ...selectedAgent, model: e.target.value })}
                                >
                                    <option value="gpt-oss:120b-cloud">gpt-oss:120b-cloud</option>
                                    <option value="llama3.1:8b">llama3.1:8b</option>
                                    <option value="tinyllama">tinyllama</option>
                                </select>
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-text-secondary uppercase tracking-[0.1em] ml-1 flex justify-between">
                                    <span>Temperature</span>
                                    <span className="text-accent">{selectedAgent.temperature}</span>
                                </label>
                                <input
                                    className="w-full accent-accent h-2 bg-white/5 rounded-lg border-none"
                                    type="range" min="0" max="1" step="0.1"
                                    value={selectedAgent.temperature}
                                    onChange={(e) => setSelectedAgent({ ...selectedAgent, temperature: parseFloat(e.target.value) })}
                                />
                            </div>
                        </div>
                        {message && (
                            <p className={`text-sm p-4 rounded-xl border ${message.includes('✅') ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-red-500/10 border-red-500/30 text-red-400'} animate-bounce`}>
                                {message}
                            </p>
                        )}

                        <div className="mt-12 bg-gradient-to-br from-indigo-900/40 to-slate-900/60 p-8 rounded-[24px] border border-white/5 space-y-6">
                            <div className="flex justify-between items-center">
                                <h3 className="text-lg font-bold text-purple-300 tracking-wider">👑 MASTER CONTROLLER</h3>
                                <button
                                    className="btn-primary flex items-center gap-2"
                                    onClick={runMasterStrategy}
                                    disabled={running}
                                >
                                    {running ? "⏳ Processing..." : (
                                        <>
                                            <span className="text-xl">▶️</span> Run Global Strategy
                                        </>
                                    )}
                                </button>
                            </div>
                            <div className="text-xs font-mono text-cyan-400/70 p-3 bg-black/40 rounded-lg border-l-4 border-accent shadow-inner">
                                <span className="animate-pulse">●</span> LOG: {logMessage}
                            </div>
                            <div className="bg-black/80 p-6 rounded-2xl font-mono text-cyan-50 border border-white/5 min-h-[200px] leading-relaxed relative scrollbar-thin overflow-y-auto max-h-[400px]">
                                {report || "System ready for global orchestration..."}
                                {running && <span className="inline-block w-2 h-5 bg-cyan-400 ml-1 animate-pulse align-middle"></span>}
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
                        <span className="text-6xl opacity-10">🤖</span>
                        <p className="text-text-secondary opacity-40 italic">Select an agent to configure or create a new one.</p>
                    </div>
                )}
            </div>
        </div>
    )
}
