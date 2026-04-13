import React from 'react';
import { 
  LayoutDashboard, 
  Megaphone, 
  Users, 
  BookOpen, 
  UserCheck, 
  ClipboardList, 
  AlertTriangle, 
  Calendar, 
  FileText,
  Menu,
  X
} from 'lucide-react';

const Sidebar = ({ activeSection, setActiveSection, collapsed, setCollapsed }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, color: 'text-neon-cyan' },
    { id: 'announcements', label: 'Announcements', icon: Megaphone, color: 'text-neon-purple' },
    { id: 'manage-staff', label: 'Manage Staff', icon: Users, color: 'text-neon-green' },
    { id: 'subjects', label: 'Subjects', icon: BookOpen, color: 'text-neon-yellow' },
    { id: 'assign-subjects', label: 'Assign Subjects', icon: UserCheck, color: 'text-neon-pink' },
    { id: 'test-marks', label: 'Test Marks', icon: ClipboardList, color: 'text-neon-cyan' },
    { id: 'complaints', label: 'Complaints', icon: AlertTriangle, color: 'text-neon-yellow' },
    { id: 'leave-requests', label: 'Leave Requests', icon: Calendar, color: 'text-neon-purple' },
    { id: 'reports', label: 'Reports', icon: FileText, color: 'text-neon-green' },
  ];

  return (
    <>
      {/* Mobile overlay */}
      {!collapsed && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setCollapsed(true)}
        />
      )}
      
      <div className={`
        fixed lg:relative z-50 h-full transition-all duration-300 ease-in-out
        ${collapsed ? '-translate-x-full lg:translate-x-0 lg:w-20' : 'translate-x-0 w-80 lg:w-80'}
        bg-gradient-to-b from-cyber-gray via-cyber-dark to-cyber-gray
        border-r border-neon-cyan/30 shadow-neon-cyan/20 shadow-2xl
      `}>
        {/* Header */}
        <div className="p-6 border-b border-neon-cyan/30">
          <div className="flex items-center justify-between">
            {!collapsed && (
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-cyan to-neon-purple flex items-center justify-center">
                  <span className="text-black font-bold text-lg">H</span>
                </div>
                <div>
                  <h1 className="text-xl font-bold gradient-text">HOD</h1>
                  <p className="text-xs text-gray-400">Dashboard</p>
                </div>
              </div>
            )}
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="p-2 rounded-lg hover:bg-cyber-light transition-colors lg:hidden"
            >
              {collapsed ? <Menu size={20} /> : <X size={20} />}
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2 overflow-y-auto h-full pb-20">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeSection === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveSection(item.id);
                  if (window.innerWidth < 1024) {
                    setCollapsed(true);
                  }
                }}
                className={`
                  w-full flex items-center space-x-4 p-4 rounded-xl transition-all duration-300
                  hover:bg-cyber-light hover:shadow-glow group cyber-button
                  ${isActive 
                    ? `bg-cyber-light border border-current shadow-glow ${item.color}` 
                    : 'text-gray-300 hover:text-white'
                  }
                  ${collapsed ? 'justify-center' : 'justify-start'}
                `}
              >
                <Icon 
                  size={24} 
                  className={`
                    ${isActive ? item.color : 'group-hover:text-neon-cyan'}
                    ${isActive ? 'neon-glow' : ''}
                    transition-all duration-300
                  `}
                />
                {!collapsed && (
                  <span className={`
                    font-medium transition-all duration-300
                    ${isActive ? 'text-white' : 'group-hover:text-white'}
                  `}>
                    {item.label}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Footer */}
        {!collapsed && (
          <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-neon-cyan/30 bg-cyber-gray">
            <div className="text-center">
              <p className="text-xs text-gray-400">Department Management</p>
              <p className="text-xs text-neon-cyan">System v2.0</p>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default Sidebar;