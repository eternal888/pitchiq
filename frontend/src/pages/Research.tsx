import { useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

interface ResearchResult {
  contact_name: string
  contact_title: string
  hotel_name: string
  fit_score: number
  pain_points: string[]
  value_props: string[]
  email_subject: string
  email_body: string
  linkedin_message: string
  quality_approved: boolean
  send_time: string
  follow_up_sequence: string[]
}

function Research() {
  const [form, setForm] = useState({
    contact_name: '',
    contact_title: '',
    hotel_name: '',
    hotel_location: '',
    linkedin_url: '',
    email: ''
  })

  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ResearchResult | null>(null)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/research`, form)
      setResult(response.data)
    } catch (err) {
      setError('Something went wrong. Make sure the API is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-2">Research a Contact</h2>
      <p className="text-gray-400 mb-8">Enter hotel contact details to generate personalized outreach.</p>

      {/* Form */}
      <div className="space-y-4 mb-6">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Contact Name</label>
            <input
              type="text"
              placeholder="John Smith"
              value={form.contact_name}
              onChange={e => setForm({...form, contact_name: e.target.value})}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-gray-500"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Title</label>
            <input
              type="text"
              placeholder="General Manager"
              value={form.contact_title}
              onChange={e => setForm({...form, contact_title: e.target.value})}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-gray-500"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Hotel Name</label>
            <input
              type="text"
              placeholder="Marriott Biscayne Bay"
              value={form.hotel_name}
              onChange={e => setForm({...form, hotel_name: e.target.value})}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-gray-500"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Location</label>
            <input
              type="text"
              placeholder="Miami, FL"
              value={form.hotel_location}
              onChange={e => setForm({...form, hotel_location: e.target.value})}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-gray-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">Email</label>
          <input
            type="email"
            placeholder="john@marriott.com"
            value={form.email}
            onChange={e => setForm({...form, email: e.target.value})}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-gray-500"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">LinkedIn URL (optional)</label>
          <input
            type="text"
            placeholder="https://linkedin.com/in/..."
            value={form.linkedin_url}
            onChange={e => setForm({...form, linkedin_url: e.target.value})}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-gray-500"
          />
        </div>

        <button
          onClick={handleSubmit}
          disabled={loading || !form.contact_name || !form.hotel_name}
          className="w-full bg-white text-black font-medium py-3 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Researching...' : 'Research Contact'}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-6 text-red-400">
          {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="space-y-4">
          
          {/* Score */}
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold">{result.contact_name} — {result.contact_title}</h3>
              <span className="text-2xl font-bold text-green-400">{result.fit_score}/100</span>
            </div>
            <p className="text-sm text-gray-400">{result.hotel_name}</p>
          </div>

          {/* Email */}
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <h3 className="font-semibold mb-3">Email</h3>
            <p className="text-sm text-gray-400 mb-2">Subject: {result.email_subject}</p>
            <p className="text-sm text-gray-300 whitespace-pre-line">{result.email_body}</p>
          </div>

          {/* LinkedIn */}
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <h3 className="font-semibold mb-3">LinkedIn Message</h3>
            <p className="text-sm text-gray-300">{result.linkedin_message}</p>
          </div>

          {/* Schedule */}
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <h3 className="font-semibold mb-3">Schedule</h3>
            <p className="text-sm text-gray-400">Send: {result.send_time}</p>
            <div className="mt-2 space-y-1">
              {result.follow_up_sequence.map((f, i) => (
                <p key={i} className="text-sm text-gray-500">{f}</p>
              ))}
            </div>
          </div>

        </div>
      )}
    </div>
  )
}

export default Research