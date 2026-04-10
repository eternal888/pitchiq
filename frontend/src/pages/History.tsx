import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

interface HistoryRecord {
  id: number
  contact_name: string
  contact_title: string
  hotel_name: string
  fit_score: number
  email_subject: string
  quality_approved: boolean
  approval_status: string
  created_at: string
}

function History() {
  const [records, setRecords] = useState<HistoryRecord[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axios.get(`${API_URL}/history`)
        setRecords(response.data)
      } catch (err) {
        console.error('Failed to fetch history')
      } finally {
        setLoading(false)
      }
    }
    fetchHistory()
  }, [])

  const getStatusColor = (status: string) => {
    if (status === 'approved') return 'text-green-400'
    if (status === 'rejected') return 'text-red-400'
    return 'text-yellow-400'
  }

  if (loading) {
    return (
      <div>
        <h2 className="text-2xl font-bold mb-6">History</h2>
        <p className="text-gray-400">Loading...</p>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Research History</h2>
      <p className="text-gray-400 mb-8">{records.length} total researches</p>

      {records.length === 0 ? (
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-8 text-center">
          <p className="text-gray-400">No research history yet</p>
        </div>
      ) : (
        <div className="space-y-3">
          {records.map(record => (
            <div key={record.id} className="bg-gray-900 border border-gray-800 rounded-lg p-4 flex items-center justify-between">
              <div>
                <p className="font-medium">{record.contact_name} — {record.contact_title}</p>
                <p className="text-sm text-gray-400">{record.hotel_name}</p>
                <p className="text-xs text-gray-500 mt-1">{record.email_subject}</p>
              </div>
              <div className="text-right">
                <p className="text-green-400 font-bold">{record.fit_score}/100</p>
                <p className={`text-xs mt-1 ${getStatusColor(record.approval_status)}`}>
                  {record.approval_status}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(record.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default History