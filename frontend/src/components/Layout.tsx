import { Outlet, Link, useLocation } from 'react-router-dom'

function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      
      {/* Navbar */}
      <nav className="border-b border-gray-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          
          {/* Logo */}
          <h1 className="text-xl font-bold text-white">PitchIQ</h1>
          
          {/* Navigation Links */}
          <div className="flex gap-6">
            <Link
              to="/"
              className={location.pathname === '/' 
                ? 'text-white font-medium' 
                : 'text-gray-400 hover:text-white'}
            >
              Research
            </Link>
            <Link
              to="/pending"
              className={location.pathname === '/pending' 
                ? 'text-white font-medium' 
                : 'text-gray-400 hover:text-white'}
            >
              Pending
            </Link>
            <Link
              to="/history"
              className={location.pathname === '/history' 
                ? 'text-white font-medium' 
                : 'text-gray-400 hover:text-white'}
            >
              History
            </Link>
          </div>
        </div>
      </nav>

      {/* Page Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        <Outlet />
      </main>

    </div>
  )
}

export default Layout