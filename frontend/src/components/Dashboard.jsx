import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Dashboard() {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    const [report, setReport] = useState("")
    const [running, setRunning] = useState(false)

    useEffect(() => {
        axios.get('/api/business/snapshot')
            .then(res => { setData(res.data.data); setLoading(false) })
            .catch(() => setLoading(false))
    }, [])

    const runCEO = async () => {
        setRunning(true)
        const res = await axios.post('/api/ceo/run')
        setReport(res.data.report)
        setRunning(false)
    }

    return (
        <div className="card dashboard">
            <h2>📊 Business Dashboard</h2>
            {loading ? <p>Loading live data...</p> : (
                <div className="stats">
                    <div className="stat-box agri">
                        <span>🌾 Agri Orders</span>
                        <strong>{data?.agri_pending ?? 0}</strong>
                    </div>
                    <div className="stat-box cloth">
                        <span>👗 Low Stock Items</span>
                        <strong>{data?.low_stock_dresses ?? 0}</strong>
                    </div>
                    <div className="stat-box crm">
                        <span>📞 New CRM Leads</span>
                        <strong>{data?.new_crm_leads ?? 0}</strong>
                    </div>
                </div>
            )}
            <button onClick={runCEO} disabled={running}>
                {running ? "⏳ CEO Thinking..." : "🚀 Run CEO Strategy"}
            </button>
            {report && <div className="report"><h3>CEO Report:</h3><p>{report}</p></div>}
        </div>
    )
}
