import { Github, Twitter, Mail, Heart } from 'lucide-react'

const Footer = () => {
  const categories = [
    { name: 'Books', path: '/books' },
    { name: 'Movies', path: '/movies' },
    { name: 'Series', path: '/series' },
    { name: 'Anime', path: '/anime' },
    { name: 'Games', path: '/games' },
    { name: 'Music', path: '/music' },
    { name: 'Cars', path: '/cars' }
  ]

  const company = [
    { name: 'About Us', path: '/about' },
    { name: 'Contact', path: '/contact' },
    { name: 'Privacy Policy', path: '/privacy' },
    { name: 'Terms of Service', path: '/terms' }
  ]

  const resources = [
    { name: 'API Documentation', path: '/api-docs' },
    { name: 'Submit Franchise', path: '/submit' },
    { name: 'Help Center', path: '/help' },
    { name: 'Community', path: '/community' }
  ]

  return (
    <footer className="bg-slate-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="lg:col-span-1">
            <div className="flex items-center mb-4">
              <div className="text-2xl font-bold">
                Order<span className="text-teal-400">Of</span>
              </div>
            </div>
            <p className="text-slate-400 mb-6 max-w-sm">
              The ultimate guide to experiencing your favorite franchises in the perfect order. From movies to books, games to series.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-slate-400 hover:text-white transition-colors">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors">
                <Github className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors">
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Categories */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Categories</h3>
            <ul className="space-y-2">
              {categories.map((category) => (
                <li key={category.name}>
                  <a
                    href={category.path}
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    {category.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              {company.map((item) => (
                <li key={item.name}>
                  <a
                    href={item.path}
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              {resources.map((item) => (
                <li key={item.name}>
                  <a
                    href={item.path}
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-slate-800 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-slate-400 text-sm">
              © 2025 OrderOf.org. All rights reserved.
            </p>
            <p className="text-slate-400 text-sm flex items-center mt-4 md:mt-0">
              Made with <Heart className="h-4 w-4 text-red-500 mx-1" /> for franchise fans everywhere
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer

