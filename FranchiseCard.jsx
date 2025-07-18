import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { Star, Calendar, List } from 'lucide-react'

const FranchiseCard = ({ franchise, onClick }) => {
  const categoryColors = {
    movies: 'bg-red-100 text-red-800',
    series: 'bg-blue-100 text-blue-800',
    books: 'bg-green-100 text-green-800',
    games: 'bg-purple-100 text-purple-800',
    anime: 'bg-pink-100 text-pink-800',
    music: 'bg-yellow-100 text-yellow-800',
    cars: 'bg-gray-100 text-gray-800'
  }

  const categoryIcons = {
    movies: '🎬',
    series: '📺',
    books: '📚',
    games: '🎮',
    anime: '🎌',
    music: '🎵',
    cars: '🚗'
  }

  return (
    <Card 
      className="group cursor-pointer hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
      onClick={() => onClick && onClick(franchise)}
    >
      <CardContent className="p-0">
        {/* Image */}
        <div className="relative h-48 bg-gradient-to-br from-slate-100 to-slate-200 rounded-t-lg overflow-hidden">
          {franchise.image_url ? (
            <img
              src={franchise.image_url}
              alt={franchise.name}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-6xl">
              {categoryIcons[franchise.category] || '📁'}
            </div>
          )}
          
          {/* Category Badge */}
          <div className="absolute top-3 left-3">
            <Badge className={`${categoryColors[franchise.category]} border-0`}>
              {franchise.category}
            </Badge>
          </div>

          {/* Popularity Score */}
          {franchise.popularity_score > 0 && (
            <div className="absolute top-3 right-3 bg-black/70 text-white px-2 py-1 rounded-full text-xs flex items-center gap-1">
              <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
              {franchise.popularity_score}
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-4">
          <h3 className="font-semibold text-lg text-slate-900 mb-2 line-clamp-2 group-hover:text-teal-600 transition-colors">
            {franchise.name}
          </h3>
          
          {franchise.description && (
            <p className="text-slate-600 text-sm mb-3 line-clamp-2">
              {franchise.description}
            </p>
          )}

          {/* Metadata */}
          <div className="flex items-center justify-between text-xs text-slate-500">
            <div className="flex items-center gap-1">
              <Calendar className="h-3 w-3" />
              {franchise.created_at ? new Date(franchise.created_at).getFullYear() : 'N/A'}
            </div>
            
            <div className="flex items-center gap-1">
              <List className="h-3 w-3" />
              View Orders
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default FranchiseCard

