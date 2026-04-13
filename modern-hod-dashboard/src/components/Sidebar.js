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
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

const Sidebar = ({ activeModule, setActiveModule, collapsed, setCollapsed }) => {
  const menuItems = [
    { 
      id: 'dashboard', 
      label: 'Dashboard', 
      icon: LayoutDashboard, 
      color: 'text-neon-cyan',
      hoverColor: 'hover:text-neon-cyan'
    },
    { 
      id: 'announcements', 
      label: 'Announcements', 
      icon: Megaphone, 
      color: 'text-neon-purple',
      hoverColor: 'hover:text-neon-purple'
    },
    { 
      id: 'manage-staff', 
      label: 'Manage Staff', 
      icon: Users, 
      color: 'text-neon-teal',
      hoverColor: 'hover:text-neon-teal'
    },
    { 
      id: 'subjects', 
      label: 'Subjects', 
      icon: BookOpen, 
      color: 'text-neon-yellow',
      hoverColor: 'hover:text-neon-yellow'
    },
    { 
      id: 'assign-subjects', 
      label: 'Assign Subjects', 
      icon: UserCheck, 
      color: 'text-neon-pink',
      hoverColor: 'hover:text-neon-pink'
    },
    { 
      id: 'test-marks', 
      label: 'Test Marks', 
      icon: ClipboardList, 
      color: 'text-neon-cyan',
      hoverColor: 'hover:text-neon-cyan'
    },
    { 
      id: 'complaints', 
      label: 'Complaints', 
      icon: AlertTriangle, 
      color: 'text-neon-yellow',
      hoverColor: 'hover:text-neon-yellow'
    },
    { 
      id: 'leave-requests', 
      label: 'Leave Requests', 
      icon: Calendar, 
      color: 'text-neon-purple',
      hoverColor: 'hover:text-neon-purple'
    },
    { 
      id: 'reports', 
      label: 'Reports', 
      icon: FileText, 
      color: 'text-neon-teal',
      hoverColor: 'hover:text-neon-teal'
    },
  ];

  return (
    <div className={`fixed left-0 top-0 h-full bg-cyber-card glass-strong border-r border-cyber-border transition-all duration-300 z-50 ${
      collapsed ? 'w-16' : 'w-64'
    }`}>
      {/* Header */}
      <div className="p-4 border-b border-cyber-border">
        <div className="flex items-center justify-between">
          {!collapsed && (
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-cyan to-neon-purple flex items-center justify-center">
                <span className="text-cyber-dark font-bold text-lg font-cyber">H</span>
              </div>
              <div>
                <h1 className="text-lg font-bold gradient-text font-cyber">HOD PANEL</h1>
                <p className="text-xs text-text-muted">Faculty Management</p>
              </div>
            </div>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-2 rounded-lg hover:bg-cyber-surface transition-colors text-text-secondary hover:text-neon-cyan"
          >
            {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4 space-y-2 overflow-y-auto h-full pb-20">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeModule === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => setActiveModule(item.id)}
              className={`
                w-full flex items-center space-x-4 p-3 rounded-xl transition-all duration-300
                hover:bg-cyber-surface cyber-button group
                ${isActive 
                  ? `sidebar-active ${item.color}` 
                  : `text-text-secondary ${item.hoverColor}`
                }
                ${collapsed ? 'justify-center' : 'justify-start'}
              `}
              title={collapsed ? item.label : ''}
            >
              <Icon 
                size={20} 
                className={`
                  ${isActive ? item.color : 'group-hover:text-current'}
                  ${isActive ? 'neon-glow' : ''}
                  transition-all duration-300
                `}
              />
              {!collapsed && (
                <span className={`
                  font-medium transition-all duration-300 font-modern
                  ${isActive ? 'text-current' : 'group-hover:text-current'}
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
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-cyber-border bg-cyber-card">
          <div className="text-center">
            <p className="text-xs text-text-muted">Faculty Workload System</p>
            <p className="text-xs text-neon-cyan font-cyber">v2.0 CYBER</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;