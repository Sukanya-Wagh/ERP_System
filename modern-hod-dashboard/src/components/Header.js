import React, { useState } from 'react';
import { Menu, Bell, User, Settings, LogOut, ChevronDown } from 'lucide-react';

const Header = ({ activeModule, toggleSidebar }) => {
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);

  const getModuleTitle = (module) => {
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
    return titles[module] || 'Dashboard';
  };

  return (
    <header className="bg-cyber-card glass-strong border-b border-cyber-border">
      {/* Top Gradient Banner */}
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
              <h1 className="text-2xl font-bold text-cyber-dark font-cyber">
                Welcome, A.S.Bhatlavande
              </h1>
              <p className="text-cyber-dark/80 text-sm font-modern">
                Head of Department Dashboard - Manage your department efficiently
              </p>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-2">
            <div className="w-3 h-3 bg-neon-green rounded-full animate-pulse"></div>
            <span className="text-cyber-dark text-sm font-medium font-modern">Online</span>
          </div>
        </div>
      </div>

      {/* Navigation Header */}
      <div className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold gradient-text font-modern">
              {getModuleTitle(activeModule)}
            </h2>
            <p className="text-text-muted text-sm mt-1 font-modern">
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
            <button className="relative p-3 rounded-xl bg-cyber-surface hover:bg-cyber-border transition-colors hover-glow group">
              <Bell size={20} className="text-neon-yellow group-hover:text-neon-cyan transition-colors" />
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-error rounded-full text-xs flex items-center justify-center text-white font-bold">
                3
              </span>
            </button>

            {/* Settings */}
            <button className="p-3 rounded-xl bg-cyber-surface hover:bg-cyber-border transition-colors hover-glow group">
              <Settings size={20} className="text-text-muted group-hover:text-neon-purple transition-colors" />
            </button>

            {/* Profile Dropdown */}
            <div className="relative">
              <button 
                onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                className="flex items-center space-x-3 p-3 rounded-xl bg-cyber-surface hover:bg-cyber-border transition-colors hover-glow"
              >
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-neon-cyan to-neon-purple flex items-center justify-center">
                  <User size={16} className="text-cyber-dark" />
                </div>
                <div className="hidden md:block text-left">
                  <p className="text-sm font-medium text-text-primary font-modern">A.S.Bhatlavande</p>
                  <p className="text-xs text-text-muted">Head of Department</p>
                </div>
                <ChevronDown size={16} className={`text-text-muted transition-transform ${
                  profileDropdownOpen ? 'rotate-180' : ''
                }`} />
              </button>
              
              {/* Dropdown Menu */}
              {profileDropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-cyber-card glass-strong border border-cyber-border rounded-xl shadow-glow z-50">
                  <div className="p-2">
                    <button className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-cyber-surface transition-colors text-left">
                      <User size={16} className="text-neon-cyan" />
                      <span className="text-sm font-modern">Profile</span>
                    </button>
                    <button className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-cyber-surface transition-colors text-left">
                      <Settings size={16} className="text-neon-purple" />
                      <span className="text-sm font-modern">Settings</span>
                    </button>
                    <hr className="my-2 border-cyber-border" />
                    <button className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-error/20 transition-colors text-left text-error">
                      <LogOut size={16} />
                      <span className="text-sm font-modern">Logout</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;