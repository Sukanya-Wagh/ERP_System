import React from 'react';
import { Menu, Bell, User, Settings, LogOut } from 'lucide-react';

const Header = ({ activeSection, toggleSidebar }) => {
  const getSectionTitle = (section) => {
    const titles = {
      'dashboard': 'Dashboard Overview',
      'announcements': 'Announcements Management',
      'manage-staff': 'Staff Management',
      'subjects': 'Subject Management',
      'assign-subjects': 'Subject Assignment',
      'test-marks': 'Test Marks Management',
      'complaints': 'Complaints Management',
      'leave-requests': 'Leave Requests',
      'reports': 'Reports & Analytics'
    };
    return titles[section] || 'Dashboard';
  };

  return (
    <header className="bg-gradient-to-r from-cyber-gray via-cyber-dark to-cyber-gray border-b border-neon-purple/30 shadow-lg">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-neon-purple via-neon-cyan to-neon-purple p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleSidebar}
              className="lg:hidden p-2 rounded-lg bg-black/20 hover:bg-black/40 transition-colors"
            >
              <Menu size={20} className="text-white" />
            </button>
            <div>
              <h1 className="text-2xl font-bold text-black">Welcome, A.S.Bhatlavande</h1>
              <p className="text-black/80 text-sm">Head of Department Dashboard - Manage your department efficiently</p>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-black text-sm font-medium">Online</span>
          </div>
        </div>
      </div>

      {/* Navigation Header */}
      <div className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold gradient-text">{getSectionTitle(activeSection)}</h2>
            <p className="text-gray-400 text-sm mt-1">
              {new Date().toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* Notifications */}
            <button className="relative p-3 rounded-xl bg-cyber-light hover:bg-cyber-gray transition-colors hover-glow group">
              <Bell size={20} className="text-neon-yellow group-hover:text-neon-cyan transition-colors" />
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs flex items-center justify-center text-white">
                3
              </span>
            </button>

            {/* Settings */}
            <button className="p-3 rounded-xl bg-cyber-light hover:bg-cyber-gray transition-colors hover-glow group">
              <Settings size={20} className="text-gray-400 group-hover:text-neon-purple transition-colors" />
            </button>

            {/* Profile Dropdown */}
            <div className="relative group">
              <button className="flex items-center space-x-3 p-3 rounded-xl bg-cyber-light hover:bg-cyber-gray transition-colors hover-glow">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-neon-cyan to-neon-purple flex items-center justify-center">
                  <User size={16} className="text-black" />
                </div>
                <div className="hidden md:block text-left">
                  <p className="text-sm font-medium text-white">A.S.Bhatlavande</p>
                  <p className="text-xs text-gray-400">Head of Department</p>
                </div>
              </button>
              
              {/* Dropdown Menu */}
              <div className="absolute right-0 mt-2 w-48 bg-cyber-gray border border-neon-cyan/30 rounded-xl shadow-neon-cyan/20 shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                <div className="p-2">
                  <button className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-cyber-light transition-colors text-left">
                    <User size={16} className="text-neon-cyan" />
                    <span className="text-sm">Profile</span>
                  </button>
                  <button className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-cyber-light transition-colors text-left">
                    <Settings size={16} className="text-neon-purple" />
                    <span className="text-sm">Settings</span>
                  </button>
                  <hr className="my-2 border-gray-600" />
                  <button className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-red-500/20 transition-colors text-left text-red-400">
                    <LogOut size={16} />
                    <span className="text-sm">Logout</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;