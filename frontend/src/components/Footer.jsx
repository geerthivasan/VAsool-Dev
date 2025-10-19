import React from 'react';
import { Leaf } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
              <Leaf className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">vasool</span>
          </div>

          <div className="flex items-center space-x-6 text-sm text-gray-600">
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="hover:text-green-600 transition-colors">
              LinkedIn
            </a>
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="hover:text-green-600 transition-colors">
              Twitter
            </a>
            <a href="mailto:ajith0016@gmail.com" className="hover:text-green-600 transition-colors">
              Email
            </a>
            <span>+91 9790304826</span>
          </div>

          <div className="text-sm text-gray-500 mt-4 md:mt-0">
            Revolutionizing Credit Collections with AI
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;