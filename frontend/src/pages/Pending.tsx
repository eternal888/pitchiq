import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

interface PendingRecord {
  id: number
  contact_name: string
  contact_title: string
  hotel_name: string
  fit_score: number
  email_subject: string
  email_body: string
  linkedin_message: string
  approval_status: string
  created_at: string
}

function Pending() {
  const [records, setRecords] = useState<PendingRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState<number | null>(null)

  const fetchPending = async () => {
    try {
      const response = await axios.get(`${API_URL}/pending`)
      setRecords(response.data)
    } catch (err) {
      console.error('Failed to fetch pending')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPending()
  }, [])

  const handleApprove = async (id: number) => {
    setActionLoading(id)
    try {
      await axios.post(`${API_URL}/approve/${id}`)
      fetchPending()
    } catch (err) {
      console.error('Failed to approve')
    } finally {
      setActionLoading(null)
    }
  }

  const handleReject = async (id: number) => {
    setActionLoading(id)
    try {
      await axios.post(`${API_URL}/reject/${id}`)
      fetchPending()
    } catch (err) {
      console.error('Failed to reject')
    } finally {
      setActionLoading(null)
    }
  }

  if (loading) {
    return (
      <div>
        <h2 className="text-2xl font-bold mb-6">Pending Approval</h2>
        <p className="text-gray-400">Loading...</p>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Pending Approval</h2>
      <p className="text-gray-400 mb-8">{records.length} email{records.length !== 1 ? 's' : ''} waiting for review</p>

      {records.length === 0 ? (
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-8 text-center">
          <p className="text-gray-400">No emails pending approval</p>
        </div>
      ) : (
        <div className="space-y-6">
          {records.map(record => (
            <div key={record.id} className="bg-gray-900 border border-gray-800 rounded-lg p-6">
              
              {/* Header */}
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="font-semibold">{record.contact_name} — {record.contact_title}</h3>
                  <p className="text-sm text-gray-400">{record.hotel_name}</p>
                </div>
                <span className="text-green-400 font-bold">{record.fit_score}/100</span>
              </div>

              {/* Email */}
              <div className="mb-4">
                <p className="text-sm text-gray-400 mb-1">Subject: {record.email_subject}</p>
                <p className="text-sm text-gray-300 whitespace-pre-line">{record.email_body}</p>
              </div>

              {/* LinkedIn */}
              <div className="mb-6 p-3 bg-gray-800 rounded-lg">
                <p className="text-xs text-gray-400 mb-1">LinkedIn Message</p>
                <p className="text-sm text-gray-300">{record.linkedin_message}</p>
              </div>

              {/* Actions */}
              <div className="flex gap-3">
                <button
                  onClick={() => handleApprove(record.id)}
                  disabled={actionLoading === record.id}
                  className="flex-1 bg-white text-black font-medium py-2 rounded-lg hover:bg-gray-200 disabled:opacity-50 transition-colors"
                >
                  {actionLoading === record.id ? 'Sending...' : 'Approve & Send'}
                </button>
                <button
                  onClick={() => handleReject(record.id)}
                  disabled={actionLoading === record.id}
                  className="flex-1 bg-gray-800 text-white font-medium py-2 rounded-lg hover:bg-gray-700 disabled:opacity-50 transition-colors"
                >
                  Reject
                </button>
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Pending