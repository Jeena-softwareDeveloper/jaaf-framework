import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Dashboard() {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        axios.get('/api/business/snapshot')
            .then(res => { setData(res.data.data); setLoading(false) })
            .catch(() => setLoading(false))
    }, [])

    return (
        <div className="space-y-10">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[
                    { title: 'Agri Pending', value: data?.agri_pending ?? 0, icon: '🌾', color: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' },
                    { title: 'Low Stock', value: data?.low_stock_dresses ?? 0, icon: '👗', color: 'bg-amber-500/10 border-amber-500/20 text-amber-400' },
                    { title: 'New Leads', value: data?.new_crm_leads ?? 0, icon: '📞', color: 'bg-blue-500/10 border-blue-500/20 text-blue-400' },
                ].map((stat, i) => (
                    <div key={i} className={`glass-card p-8 flex flex-col items-center justify-center text-center space-y-4 border ${stat.color} hover:scale-[1.02]`}>
                        <span className="text-4xl">{stat.icon}</span>
                        <h3 className="text-sm font-bold uppercase tracking-widest opacity-70">{stat.title}</h3>
                        <p className="text-5xl font-extrabold">{loading ? '...' : stat.value}</p>
                    </div>
                ))}
            </div>

            <div className="glass-card p-10 bg-gradient-to-br from-bg-side to-black/40">
                <div className="flex items-center gap-4 mb-6">
                    <span className="text-3xl">🚀</span>
                    <div>
                        <h3 className="text-xl font-bold">Strategic Insight</h3>
                        <p className="text-sm text-text-secondary">AI-driven summary of current operations.</p>
                    </div>
                </div>
                <div className="bg-black/20 p-6 rounded-2xl border border-white/5 min-h-[120px] text-text-secondary italic">
                    {loading ? "Analyzing system telemetry..." : "Business operations are within normal parameters. CEO Agent is standing by for strategic orchestration."}
                </div>
            </div>
        </div>
    )
}
