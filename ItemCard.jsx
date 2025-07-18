import { Calendar, Clock, Star, ExternalLink } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import AffiliateButton from './AffiliateButton'

const ItemCard = ({ item, position, showPosition = true }) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown'
    try {
      return new Date(dateString).getFullYear()
    } catch {
      return 'Unknown'
    }
  }

  const getRatingColor = (rating) => {
    if (!rating) return 'text-slate-500'
    if (rating >= 8) return 'text-green-600'
    if (rating >= 6) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <Card className="group hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
      <CardContent className="p-0">
        <div className="flex">
          {/* Position Number */}
          {showPosition && (
            <div className="flex-shrink-0 w-16 bg-gradient-to-br from-teal-500 to-blue-600 flex items-center justify-center">
              <span className="text-2xl font-bold text-white">
                {position}
              </span>
            </div>
          )}

          {/* Image */}
          <div className="relative w-24 h-36 bg-gradient-to-br from-slate-100 to-slate-200 flex-shrink-0">
            {item.image_url ? (
              <img
                src={item.image_url}
                alt={item.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-2xl">
                📄
              </div>
            )}
            
            {/* Optional Badge */}
            {item.is_optional && (
              <div className="absolute top-2 left-2">
                <Badge variant="secondary" className="text-xs">
                  Optional
                </Badge>
              </div>
            )}
          </div>

          {/* Content */}
          <div className="flex-1 p-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-semibold text-lg text-slate-900 line-clamp-2 group-hover:text-teal-600 transition-colors">
                {item.title}
              </h3>
              
              {/* Rating */}
              {item.api_metadata?.vote_average && (
                <div className="flex items-center gap-1 ml-2">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  <span className={`text-sm font-medium ${getRatingColor(item.api_metadata.vote_average)}`}>
                    {item.api_metadata.vote_average.toFixed(1)}
                  </span>
                </div>
              )}
            </div>
            
            {item.description && (
              <p className="text-slate-600 text-sm mb-3 line-clamp-2">
                {item.description}
              </p>
            )}

            {/* Notes */}
            {item.notes && (
              <div className="mb-3 p-2 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                <p className="text-sm text-blue-800">
                  <strong>Note:</strong> {item.notes}
                </p>
              </div>
            )}

            {/* Metadata */}
            <div className="flex items-center gap-4 text-xs text-slate-500 mb-3">
              <div className="flex items-center gap-1">
                <Calendar className="h-3 w-3" />
                {formatDate(item.release_date)}
              </div>
              
              {item.api_metadata?.runtime && (
                <div className="flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  {item.api_metadata.runtime}m
                </div>
              )}
            </div>

            {/* Affiliate Links */}
            {item.affiliate_links && item.affiliate_links.length > 0 && (
              <div className="border-t pt-3">
                <div className="flex flex-wrap gap-2">
                  {item.affiliate_links.map((link) => (
                    <AffiliateButton
                      key={link.id}
                      link={link}
                      size="sm"
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default ItemCard

