import React from 'react';
import { Users, BookOpen, AlertTriangle, Megaphone, Plus, Eye, Settings, BarChart3 } from 'lucide-react';

const DashboardOverview = () => {
  const stats = [
    { 
      id: 1, 
      title: 'Faculty Members', 
      value: '4', 
      icon: Users, 
      color: 'text-neon-cyan',
      bgColor: 'bg-neon-cyan/10',
      borderColor: 'border-neon-cyan/30'
    },
    { 
      id: 2, 
      title: 'Total Subjects', 
      value: '12', 
      icon: BookOpen, 
      color: 'text-neon-green',
      bgColor: 'bg-neon-green/10',
      borderColor: 'border-neon-green/30'
    },
    { 
      id: 3, 
      title: 'Pending Complaints', 
      value: '8', 
      icon: AlertTriangle, 
      color: 'text-neon-yellow',
      bgColor: 'bg-neon-yellow/10',
      borderColor: 'border-neon-yellow/30'
    },
    { 
      id: 4, 
      title: 'Active Announcements', 
      value: '7', 
      icon: Megaphone, 
      color: 'text-neon-purple',
      bgColor: 'bg-neon-purple/10',
      borderColor: 'border-neon-purple/30'
    }
  ];

  const actionCards = [
    {
      title: 'Staff Management',
      description: 'Manage Faculty',
      subtitle: 'Add, edit, or remove faculty from your department',
      icon: Users,
      color: 'text-neon-cyan',
      borderColor: 'border-neon-cyan/30',
      actions: [
        { label: 'Add Staff', icon: Plus },
        { label: 'View All Staff', icon: Eye }
      ]
    },
    {
      title: 'Announcements',
      description: 'Faculty Announcements',
      subtitle: 'Create and manage announcements for faculty members',
      icon: Megaphone,
      color: 'text-neon-purple',
      borderColor: 'border-neon-purple/30',
      actions: [
        { label: 'New Announcement', icon: Plus }
      ]
    },
    {
      title: 'Subject Management',
      description: 'Subjects & Assignment',
      subtitle: 'Manage subjects and assign them to faculty members',
      icon: BookOpen,
      color: 'text-neon-green',
      borderColor: 'border-neon-green/30',
      actions: [
        { label: 'Manage Subjects', icon: Settings },
        { label: 'Assign Faculty', icon: Users }
      ]
    },
    {
      title: 'Class Test Management',
      description: 'Manage Test Marks',
      subtitle: 'Oversee and manage class test marks for all subjects',
      icon: BarChart3,
      color: 'text-neon-yellow',
      borderColor: 'border-neon-yellow/30',
      actions: [
        { label: 'Manage Test Marks', icon: Settings }
      ]
    },
    {
      title: 'Assign Workload',
      description: 'Distribute workload among faculty members',
      subtitle: 'Efficiently assign workload among faculty members',
      icon: Users,
      color: 'text-neon-cyan',
      borderColor: 'border-neon-cyan/30',
      actions: [
        { label: 'Assign Workload', icon: Settings }
      ]
    },
    {
      title: 'Manage Model Answers',
      description: 'Model answer files for all subjects',
      subtitle: 'Upload and manage model answer files for all subjects',
      icon: BookOpen,
      color: 'text-neon-purple',
      borderColor: 'border-neon-purple/30',
      actions: [
        { label: 'Manage Model Answers', icon: Settings }
      ]
    }
  ];

  return (
    <div className="space-y-8">
      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div
              key={stat.id}
              className={`
                glass rounded-2xl p-6 border ${stat.borderColor} hover-glow
                transition-all duration-300 hover:scale-105
              `}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm font-medium">{stat.title}</p>
                  <p className={`text-3xl font-bold ${stat.color} mt-2`}>{stat.value}</p>
                </div>
                <div className={`p-4 rounded-xl ${stat.bgColor}`}>
                  <Icon size={32} className={stat.color} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Action Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {actionCards.map((card, index) => {
          const Icon = card.icon;
          return (
            <div
              key={index}
              className={`
                glass rounded-2xl p-6 border ${card.borderColor} hover-glow
                transition-all duration-300 hover:scale-105
              `}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <Icon size={24} className={card.color} />
                  <div>
                    <h3 className={`font-semibold ${card.color}`}>{card.title}</h3>
                    <p className="text-sm text-gray-400">{card.description}</p>
                  </div>
                </div>
              </div>
              
              <p className="text-gray-300 text-sm mb-6">{card.subtitle}</p>
              
              <div className="space-y-2">
                {card.actions.map((action, actionIndex) => {
                  const ActionIcon = action.icon;
                  return (
                    <button
                      key={actionIndex}
                      className={`
                        w-full flex items-center justify-center space-x-2 p-3 
                        rounded-xl border ${card.borderColor} hover:bg-cyber-light 
                        transition-all duration-300 cyber-button hover-glow
                        ${card.color}
                      `}
                    >
                      <ActionIcon size={16} />
                      <span className="font-medium">{action.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Actions Footer */}
      <div className="glass rounded-2xl p-6 border border-neon-cyan/30">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-neon-cyan mb-2">View & Generate</h3>
            <p className="text-gray-400 text-sm">Access reports and analytics</p>
          </div>
          <button className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-neon-cyan to-neon-purple rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300 cyber-button">
            <BarChart3 size={20} />
            <span>Generate Reports</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardOverview;