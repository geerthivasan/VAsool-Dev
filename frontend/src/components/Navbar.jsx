import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from './ui/button';
import { Leaf } from 'lucide-react';

const Navbar = () => {
  const navigate = useNavigate();
  const isAuthenticated = localStorage.getItem('isAuthenticated');

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    navigate('/');
  };

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
              <Leaf className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">vasool</span>
          </Link>

          <div className="hidden md:flex items-center space-x-8">
            <button
              onClick={() => scrollToSection('solution')}
              className="text-gray-700 hover:text-green-600 transition-colors"
            >
              Solution
            </button>
            <button
              onClick={() => scrollToSection('technology')}
              className="text-gray-700 hover:text-green-600 transition-colors"
            >
              Technology
            </button>
            <button
              onClick={() => scrollToSection('team')}
              className="text-gray-700 hover:text-green-600 transition-colors"
            >
              Team
            </button>
          </div>

          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Button onClick={() => navigate('/dashboard')} variant="outline">
                  Dashboard
                </Button>
                <Button onClick={handleLogout} className="bg-green-600 hover:bg-green-700">
                  Logout
                </Button>
              </>
            ) : (
              <Button onClick={() => navigate('/login')} className="bg-green-600 hover:bg-green-700">
                Login
              </Button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;