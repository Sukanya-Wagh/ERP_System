import React from 'react';
import { Users, BookOpen, AlertTriangle, Megaphone, TrendingUp, Calendar, FileText, Award } from 'lucide-react';

const Dashboard = () => {
  const stats = [
    { 
      id: 1, 
      title: 'Faculty Members', 
      value: '7', 
      icon: Users, 
      color: 'text-neon-cyan',
      bgColor: 'from-neon-cyan to-neon-teal',
      change: '+2 this month'
    },
    { 
      id: 2, 
      title: 'Total Subjects', 
      value: '12', 
      icon: BookOpen, 
      color: 'text-neon-green',
      bgColor: 'from-neon-green to-neon-teal',
      change: '+1 new subject'
    },
    { 
      id: 3, 
      title: 'Pending Complaints', 
      value: '5', 
      icon: AlertTriangle, 
      color: 'text-neon-yellow',
      bgColor: 'from-neon-yellow to-warning',
      change: '-3 resolved'
    },
    { 
      id: 4, 
      title: 'Active Announcements', 
      value: '7', 
      icon: Megaphone, 
      color: 'text-neon-purple',
      bgColor: 'from-neon-purple to-neon-pink',
      change: '+2 this week'
    }
  ];

  const recentActivities = [
    { id: 1, action: 'New faculty member added', user: 'A.A.Jadhav', time: '2 hours ago', type: 'success' },
    { id: 2, action: 'Test marks updated', user: 'System', time: '4 hours ago', type: 'info' },
    { id: 3, action: 'Complaint resolved', user: 'M.B.Patil', time: '6 hours ago', type: 'success' },
    { id: 4, action: 'New announcement posted', user: 'HOD', time: '1 day ago', type: 'info' },
    { id: 5, action: 'Leave request approved', user: 'K.Mahajan', time: '2 days ago', type: 'warning' },
  ];

  const quickActions = [
    { title: 'Add Staff', icon: Users, color: 'neon-cyan', module: 'manage-staff' },
    { title: 'Post Announcement', icon: Megaphone, color: 'neon-purple', module: 'announcements' },
    { title: 'Manage Subjects', icon: BookOpen, color: 'neon-green', module: 'subjects' },
    { title: 'View Reports', icon: FileText, color: 'neon-yellow', module: 'reports' },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Welcome Section */}
      <div className="glass-strong rounded-2xl p-6 border border-neon-cyan/30 hover-glow">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold gradient-text font-cyber mb-2">
              Welcome back, A.S.Bhatlavande
            </h1>
            <p className="text-text-muted font-modern">
              Here's what's happening in your department today
            </p>
          </div>
          <div className="hidden md:block">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-neon-cyan to-neon-purple flex items-center justify-center">
              <Award size={32} className="text-cyber-dark" />
            </div>
          </div>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div
              key={stat.id}
              className={`glass-strong rounded-2xl p-6 border border-${stat.color.replace('text-', '')}/30 hover-glow card-hover animate-delay-${(index + 1) * 100}`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.bgColor} flex items-center justify-center`}>
                  <Icon size={24} className="text-cyber-dark" />
                </div>
                <TrendingUp size={20} className={stat.color} />
              </div>
              <div>
                <p className="text-text-muted text-sm font-medium font-modern mb-1">{stat.title}</p>
                <p className={`text-3xl font-bold ${stat.color} font-cyber mb-2`}>{stat.value}</p>
                <p className="text-xs text-text-muted font-modern">{stat.change}</p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions */}
        <div className="glass-strong rounded-2xl p-6 border border-neon-purple/30 hover-glow card-hover animate-delay-500">
          <h2 className="text-xl font-semibold text-neon-purple font-cyber mb-6">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-4">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              return (
                <button
                  key={index}
                  className={`p-4 rounded-xl glass border border-${action.color}/30 hover:border-${action.color} transition-all duration-300 hover-scale group`}
                >
                  <Icon size={24} className={`text-${action.color} mb-2 group-hover:scale-110 transition-transform`} />
                  <p className={`text-sm font-medium text-${action.color} font-modern`}>{action.title}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* Recent Activities */}
        <div className="glass-strong rounded-2xl p-6 border border-neon-teal/30 hover-glow card-hover animate-delay-600">
          <h2 className="text-xl font-semibold text-neon-teal font-cyber mb-6">Recent Activities</h2>
          <div className="space-y-4">
            {recentActivities.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-cyber-surface transition-colors">
                <div className={`w-2 h-2 rounded-full mt-2 ${
                  activity.type === 'success' ? 'bg-neon-green' :
                  activity.type === 'warning' ? 'bg-neon-yellow' : 'bg-neon-cyan'
                }`}></div>
                <div className="flex-1">
                  <p className="text-text-primary font-medium font-modern text-sm">{activity.action}</p>
                  <p className="text-text-muted text-xs font-modern">by {activity.user} • {activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Performance Overview */}
      <div className="glass-strong rounded-2xl p-6 border border-neon-yellow/30 hover-glow card-hover animate-delay-700">
        <h2 className="text-xl font-semibold text-neon-yellow font-cyber mb-6">Department Performance</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-neon-green to-success mx-auto mb-3 flex items-center justify-center">
              <TrendingUp size={24} className="text-cyber-dark" />
            </div>
            <p className="text-2xl font-bold text-neon-green font-cyber">92%</p>
            <p className="text-text-muted text-sm font-modern">Average Performance</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-neon-cyan to-info mx-auto mb-3 flex items-center justify-center">
              <Calendar size={24} className="text-cyber-dark" />
            </div>
            <p className="text-2xl font-bold text-neon-cyan font-cyber">98%</p>
            <p className="text-text-muted text-sm font-modern">Attendance Rate</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-neon-purple to-neon-pink mx-auto mb-3 flex items-center justify-center">
              <Award size={24} className="text-cyber-dark" />
            </div>
            <p className="text-2xl font-bold text-neon-purple font-cyber">4.8</p>
            <p className="text-text-muted text-sm font-modern">Satisfaction Score</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;