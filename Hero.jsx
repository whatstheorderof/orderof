import { useState } from 'react'
import { Search, TrendingUp, Clock, Star } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'

const Hero = () => {
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`
    }
  }

  const featuredCategories = [
    {
      name: 'Movies',
      icon: '🎬',
      description: 'Cinematic universes & film series',
      color: 'from-red-500 to-pink-500'
    },
    {
      name: 'Books',
      icon: '📚',
      description: 'Reading orders & series',
      color: 'from-green-500 to-emerald-500'
    },
    {
      name: 'Games',
      icon: '🎮',
      description: 'Game series & timelines',
      color: 'from-purple-500 to-violet-500'
    },
    {
      name: 'Series',
      icon: '📺',
      description: 'TV shows & episodes',
      color: 'from-blue-500 to-cyan-500'
    }
  ]

  const popularSearches = [
    'Marvel Cinematic Universe',
    'Star Wars',
    'Harry Potter',
    'The Witcher',
    'Fast & Furious'
  ]

  return (
    <section className="relative bg-gradient-to-br from-slate-50 via-white to-teal-50 py-16 lg:py-24">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-grid-slate-100 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))] -z-10"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Main Headline */}
          <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-6">
            Find the Perfect
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-blue-600">
              {' '}Order{' '}
            </span>
            for Any Series
          </h1>
          
          {/* Subtitle */}
          <p className="text-xl text-slate-600 mb-8 max-w-3xl mx-auto">
            From Star Wars viewing orders to Harry Potter reading sequences, discover the best way to experience your favorite franchises across movies, books, games, and more.
          </p>

          {/* Search Bar */}
          <div className="max-w-2xl mx-auto mb-12">
            <form onSubmit={handleSearch}>
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 h-5 w-5" />
                <Input
                  type="text"
                  placeholder="Search for any franchise..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-12 pr-4 py-4 text-lg w-full rounded-full border-2 border-slate-200 focus:border-teal-500 shadow-lg"
                />
                <Button 
                  type="submit"
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 rounded-full bg-teal-600 hover:bg-teal-700 px-6"
                >
                  Search
                </Button>
              </div>
            </form>
            
            {/* Popular Searches */}
            <div className="mt-4 flex flex-wrap justify-center gap-2">
              <span className="text-sm text-slate-500 mr-2">Popular:</span>
              {popularSearches.map((search) => (
                <button
                  key={search}
                  onClick={() => setSearchQuery(search)}
                  className="text-sm text-teal-600 hover:text-teal-700 hover:underline"
                >
                  {search}
                </button>
              ))}
            </div>
          </div>

          {/* Featured Categories */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {featuredCategories.map((category) => (
              <Card 
                key={category.name}
                className="group cursor-pointer hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border-0 bg-white/80 backdrop-blur-sm"
                onClick={() => window.location.href = `/${category.name.toLowerCase()}`}
              >
                <CardContent className="p-6 text-center">
                  <div className={`w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-r ${category.color} flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-300`}>
                    {category.icon}
                  </div>
                  <h3 className="font-semibold text-lg text-slate-900 mb-2 group-hover:text-teal-600 transition-colors">
                    {category.name}
                  </h3>
                  <p className="text-slate-600 text-sm">
                    {category.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="flex items-center justify-center mb-2">
                <TrendingUp className="h-6 w-6 text-teal-600 mr-2" />
                <span className="text-3xl font-bold text-slate-900">1000+</span>
              </div>
              <p className="text-slate-600">Franchises Covered</p>
            </div>
            
            <div className="text-center">
              <div className="flex items-center justify-center mb-2">
                <Clock className="h-6 w-6 text-teal-600 mr-2" />
                <span className="text-3xl font-bold text-slate-900">50K+</span>
              </div>
              <p className="text-slate-600">Items Organized</p>
            </div>
            
            <div className="text-center">
              <div className="flex items-center justify-center mb-2">
                <Star className="h-6 w-6 text-teal-600 mr-2" />
                <span className="text-3xl font-bold text-slate-900">100K+</span>
              </div>
              <p className="text-slate-600">Happy Users</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero

