import { useState, useEffect } from 'react'
import Header from './components/Header'
import Hero from './components/Hero'
import CategorySection from './components/CategorySection'
import Footer from './components/Footer'
import FranchiseDetail from './components/FranchiseDetail'
import './App.css'

function App() {
  const [popularFranchises, setPopularFranchises] = useState([])
  const [loading, setLoading] = useState(true)
  const [currentView, setCurrentView] = useState('home')
  const [selectedFranchiseId, setSelectedFranchiseId] = useState(null)

  useEffect(() => {
    fetchPopularFranchises()
  }, [])

  const fetchPopularFranchises = async () => {
    try {
      const response = await fetch('/api/franchises?limit=8')
      const data = await response.json()
      setPopularFranchises(data.franchises || [])
    } catch (error) {
      console.error('Error fetching popular franchises:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFranchiseClick = (franchiseId) => {
    setSelectedFranchiseId(franchiseId)
    setCurrentView('franchise-detail')
  }

  const handleBackToHome = () => {
    setCurrentView('home')
    setSelectedFranchiseId(null)
  }

  const categories = [
    { key: 'movies', title: 'Popular Movies', icon: '🎬' },
    { key: 'series', title: 'TV Series', icon: '📺' },
    { key: 'books', title: 'Book Series', icon: '📚' },
    { key: 'games', title: 'Game Franchises', icon: '🎮' },
    { key: 'anime', title: 'Anime Series', icon: '🎌' },
    { key: 'music', title: 'Music Artists', icon: '🎵' }
  ]

  if (currentView === 'franchise-detail') {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <FranchiseDetail 
          franchiseId={selectedFranchiseId} 
          onBack={handleBackToHome}
        />
        <Footer />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main>
        <Hero />
        
        {/* Popular Section */}
        {!loading && popularFranchises.length > 0 && (
          <section className="py-12 bg-slate-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-slate-900 mb-4">
                  🔥 Trending Now
                </h2>
                <p className="text-slate-600 max-w-2xl mx-auto">
                  Discover the most popular franchises and their perfect viewing orders
                </p>
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {popularFranchises.map((franchise) => (
                  <div 
                    key={franchise.id} 
                    className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-4 cursor-pointer"
                    onClick={() => handleFranchiseClick(franchise.id)}
                  >
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-teal-400 to-blue-500 rounded-lg flex items-center justify-center text-white font-bold">
                        {franchise.name.charAt(0)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-slate-900 truncate">
                          {franchise.name}
                        </h3>
                        <p className="text-sm text-slate-500 capitalize">
                          {franchise.category}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        {/* Category Sections */}
        {categories.map((category) => (
          <CategorySection
            key={category.key}
            category={category.key}
            title={category.title}
            icon={category.icon}
            onFranchiseClick={handleFranchiseClick}
          />
        ))}

        {/* Call to Action */}
        <section className="py-16 bg-gradient-to-r from-teal-600 to-blue-600">
          <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-white mb-4">
              Can't Find Your Favorite Franchise?
            </h2>
            <p className="text-xl text-teal-100 mb-8">
              Help us grow our database by suggesting new franchises and their orders
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-teal-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
                Submit a Franchise
              </button>
              <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-teal-600 transition-colors">
                Join Our Community
              </button>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}

export default App
