import { ExternalLink, ShoppingCart, Music, Gamepad2, Car } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

const AffiliateButton = ({ link, size = 'sm', className = '' }) => {
  const platformConfig = {
    amazon_uk: {
      name: 'Amazon UK',
      icon: ShoppingCart,
      color: 'bg-orange-500 hover:bg-orange-600',
      textColor: 'text-white'
    },
    amazon_us: {
      name: 'Amazon US',
      icon: ShoppingCart,
      color: 'bg-orange-600 hover:bg-orange-700',
      textColor: 'text-white'
    },
    spotify: {
      name: 'Spotify',
      icon: Music,
      color: 'bg-green-500 hover:bg-green-600',
      textColor: 'text-white'
    },
    itunes: {
      name: 'iTunes',
      icon: Music,
      color: 'bg-gray-800 hover:bg-gray-900',
      textColor: 'text-white'
    },
    steam: {
      name: 'Steam',
      icon: Gamepad2,
      color: 'bg-blue-600 hover:bg-blue-700',
      textColor: 'text-white'
    },
    other: {
      name: 'Buy Now',
      icon: ExternalLink,
      color: 'bg-slate-600 hover:bg-slate-700',
      textColor: 'text-white'
    }
  }

  const config = platformConfig[link.platform] || platformConfig.other
  const Icon = config.icon

  const handleClick = () => {
    // Track affiliate click for analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', 'affiliate_click', {
        platform: link.platform,
        item_id: link.item_id,
        price: link.price,
        currency: link.currency
      })
    }
    
    // Open affiliate link in new tab
    window.open(link.url, '_blank', 'noopener,noreferrer')
  }

  return (
    <div className={`flex flex-col gap-1 ${className}`}>
      <Button
        onClick={handleClick}
        size={size}
        className={`${config.color} ${config.textColor} flex items-center gap-2 transition-all duration-200 hover:scale-105`}
      >
        <Icon className="h-4 w-4" />
        {config.name}
        <ExternalLink className="h-3 w-3" />
      </Button>
      
      {link.price && (
        <div className="text-center">
          <Badge variant="secondary" className="text-xs">
            {link.currency === 'USD' ? '$' : link.currency === 'GBP' ? '£' : ''}
            {link.price}
          </Badge>
        </div>
      )}
    </div>
  )
}

export default AffiliateButton

