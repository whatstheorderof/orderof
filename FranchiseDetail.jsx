import { useState, useEffect } from 'react'
import { ArrowLeft, Calendar, Star, Users, Clock } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import ItemCard from './ItemCard'

const FranchiseDetail = ({ franchiseId, onBack }) => {
  const [franchise, setFranchise] = useState(null)
  const [orders, setOrders] = useState([])
  const [activeOrder, setActiveOrder] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (franchiseId) {
      fetchFranchiseDetails()
    }
  }, [franchiseId])

  const fetchFranchiseDetails = async () => {
    try {
      setLoading(true)
      
      // Fetch franchise and orders
      const ordersResponse = await fetch(`/api/franchises/${franchiseId}/orders`)
      const ordersData = await ordersResponse.json()
      
      setFranchise(ordersData.franchise)
      setOrders(ordersData.orders || [])
      
      // Set default active order (release order if available)
      const defaultOrder = ordersData.orders?.find(order => order.order_type === 'release') || ordersData.orders?.[0]
      setActiveOrder(defaultOrder)
      
    } catch (error) {
      console.error('Error fetching franchise details:', error)
    } finally {
      setLoading(false)
    }
  }

  const categoryColors = {
    movies: 'bg-red-100 text-red-800',
    series: 'bg-blue-100 text-blue-800',
    books: 'bg-green-100 text-green-800',
    games: 'bg-purple-100 text-purple-800',
    anime: 'bg-pink-100 text-pink-800',
    music: 'bg-yellow-100 text-yellow-800',
    cars: 'bg-gray-100 text-gray-800'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-slate-200 rounded w-1/4 mb-4"></div>
            <div className="h-64 bg-slate-200 rounded mb-8"></div>
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-32 bg-slate-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!franchise) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Franchise not found</h2>
          <Button onClick={onBack}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Go Back
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Button 
            variant="ghost" 
            onClick={onBack}
            className="text-white hover:bg-white/10 mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Home
          </Button>
          
          <div className="flex flex-col md:flex-row gap-8">
            {/* Franchise Image */}
            <div className="w-48 h-72 bg-gradient-to-br from-slate-600 to-slate-800 rounded-lg flex items-center justify-center flex-shrink-0">
              {franchise.image_url ? (
                <img
                  src={franchise.image_url}
                  alt={franchise.name}
                  className="w-full h-full object-cover rounded-lg"
                />
              ) : (
                <div className="text-6xl">📁</div>
              )}
            </div>
            
            {/* Franchise Info */}
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-4">
                <Badge className={`${categoryColors[franchise.category]} border-0`}>
                  {franchise.category}
                </Badge>
                {franchise.popularity_score > 0 && (
                  <div className="flex items-center gap-1 bg-white/10 px-2 py-1 rounded-full">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span className="text-sm">{franchise.popularity_score}</span>
                  </div>
                )}
              </div>
              
              <h1 className="text-4xl font-bold mb-4">{franchise.name}</h1>
              
              {franchise.description && (
                <p className="text-xl text-slate-300 mb-6 leading-relaxed">
                  {franchise.description}
                </p>
              )}
              
              <div className="flex flex-wrap gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  <span>Added {new Date(franchise.created_at).getFullYear()}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4" />
                  <span>{orders.reduce((total, order) => total + (order.items?.length || 0), 0)} Items</span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  <span>{orders.length} Order{orders.length !== 1 ? 's' : ''}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {orders.length === 0 ? (
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">No orders available</h2>
            <p className="text-slate-600">This franchise doesn't have any viewing orders yet.</p>
          </div>
        ) : (
          <Tabs value={activeOrder?.order_type || 'release'} onValueChange={(value) => {
            const order = orders.find(o => o.order_type === value)
            setActiveOrder(order)
          }}>
            <TabsList className="grid w-full grid-cols-3 lg:w-auto lg:grid-cols-none lg:flex">
              {orders.map((order) => (
                <TabsTrigger key={order.id} value={order.order_type} className="capitalize">
                  {order.order_type.replace('_', ' ')} Order
                </TabsTrigger>
              ))}
            </TabsList>
            
            {orders.map((order) => (
              <TabsContent key={order.id} value={order.order_type} className="mt-8">
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-slate-900 mb-2">
                    {order.name || `${order.order_type.replace('_', ' ')} Order`}
                  </h2>
                  {order.description && (
                    <p className="text-slate-600">{order.description}</p>
                  )}
                </div>
                
                <div className="space-y-4">
                  {order.items?.map((item) => (
                    <ItemCard
                      key={item.id}
                      item={item}
                      position={item.position}
                      showPosition={true}
                    />
                  ))}
                </div>
              </TabsContent>
            ))}
          </Tabs>
        )}
      </div>
    </div>
  )
}

export default FranchiseDetail

