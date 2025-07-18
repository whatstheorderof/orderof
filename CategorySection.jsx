import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import FranchiseCard from './FranchiseCard'

const CategorySection = ({ category, title, icon, onFranchiseClick }) => {
  const [franchises, setFranchises] = useState([])
  const [loading, setLoading] = useState(true)
  const [scrollPosition, setScrollPosition] = useState(0)

  useEffect(() => {
    fetchCategoryFranchises()
  }, [category])

  const fetchCategoryFranchises = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/categories/${category}/franchises?limit=10`)
      const data = await response.json()
      setFranchises(data.franchises || [])
    } catch (error) {
      console.error('Error fetching franchises:', error)
      setFranchises([])
    } finally {
      setLoading(false)
    }
  }

  const scroll = (direction) => {
    const container = document.getElementById(`scroll-${category}`)
    const scrollAmount = 320 // Width of card + gap
    const newPosition = direction === 'left' 
      ? Math.max(0, scrollPosition - scrollAmount)
      : scrollPosition + scrollAmount
    
    container.scrollTo({
      left: newPosition,
      behavior: 'smooth'
    })
    setScrollPosition(newPosition)
  }

  const handleFranchiseClick = (franchise) => {
    // Navigate to franchise detail page
    if (onFranchiseClick) {
      onFranchiseClick(franchise.id)
    } else {
      window.location.href = `/franchise/${franchise.slug}`
    }
  }

  if (loading) {
    return (
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
              <span className="text-3xl">{icon}</span>
              {title}
            </h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="bg-slate-200 h-48 rounded-t-lg"></div>
                <div className="p-4 space-y-2">
                  <div className="bg-slate-200 h-4 rounded"></div>
                  <div className="bg-slate-200 h-3 rounded w-3/4"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    )
  }

  if (franchises.length === 0) {
    return null
  }

  return (
    <section className="py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
            <span className="text-3xl">{icon}</span>
            {title}
          </h2>
          
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => scroll('left')}
              disabled={scrollPosition === 0}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => scroll('right')}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="ml-2">
              View All <ArrowRight className="h-4 w-4 ml-1" />
            </Button>
          </div>
        </div>

        {/* Scrollable Cards Container */}
        <div className="relative">
          <div
            id={`scroll-${category}`}
            className="flex gap-6 overflow-x-auto scrollbar-hide pb-4"
            style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
          >
            {franchises.map((franchise) => (
              <div key={franchise.id} className="flex-none w-80">
                <FranchiseCard 
                  franchise={franchise} 
                  onClick={handleFranchiseClick}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default CategorySection

