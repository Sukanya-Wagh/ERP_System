import React, { useState } from 'react';
import { FileText, Download, BarChart3, PieChart, TrendingUp, Calendar, Filter, Eye } from 'lucide-react';

const Reports = () => {
  const [selectedReportType, setSelectedReportType] = useState('all');
  const [selectedPeriod, setSelectedPeriod] = useState('monthly');
  
  const reportTypes = [
    {
      id: 'faculty-performance',
      title: 'Faculty Performance Report',
      description: 'Comprehensive analysis of faculty teaching performance and student feedback',
      icon: TrendingUp,
      color: 'neon-cyan',
      lastGenerated: '2024-01-15',
      size: '2.3 MB'
    },
    {
      id: 'student-analytics',
      title: 'Student Analytics Report',
      description: 'Student performance, attendance, and academic progress analysis',
      icon: BarChart3,
      color: 'neon-green',
      lastGenerated: '2024-01-14',
      size: '1.8 MB'
    },
    {
      id: 'subject-analysis',
      title: 'Subject Analysis Report',
      description: 'Subject-wise performance metrics and curriculum effectiveness',
      icon: PieChart,
      color: 'neon-purple',
      lastGenerated: '2024-01-13',
      size: '1.5 MB'
    },
    {
      id: 'attendance-summary',
      title: 'Attendance Summary',
      description: 'Faculty and student attendance patterns and trends',
      icon: Calendar,
      color: 'neon-yellow',
      lastGenerated: '2024-01-12',
      size: '0.9 MB'
    },
    {
      id: 'complaints-analysis',
      title: 'Complaints Analysis',
      description: 'Analysis of student complaints and resolution effectiveness',
      icon: FileText,
      color: 'neon-pink',
      lastGenerated: '2024-01-11',
      size: '1.2 MB'
    },
    {
      id: 'workload-distribution',
      title: 'Workload Distribution Report',
      description: 'Faculty workload analysis and resource allocation insights',
      icon: TrendingUp,
      color: 'neon-cyan',
      lastGenerated: '2024-01-10',
      size: '1.7 MB'
    }
  ];

  const quickStats = [
    { label: 'Total Reports Generated', value: '156', color: 'neon-cyan' },
    { label: 'This Month', value: '24', color: 'neon-green' },
    { label: 'Pending Reports', value: '3', color: 'neon-yellow' },
    { label: 'Automated Reports', value: '12', color: 'neon-purple' }
  ];

  const recentReports = [
    { name: 'Monthly Faculty Performance - December 2023', date: '2024-01-15', type: 'Faculty Performance', status: 'completed' },
    { name: 'Student Analytics Q4 2023', date: '2024-01-14', type: 'Student Analytics', status: 'completed' },
    { name: 'Subject Analysis - Semester 3', date: '2024-01-13', type: 'Subject Analysis', status: 'completed' },
    { name: 'Weekly Attendance Summary', date: '2024-01-12', type: 'Attendance', status: 'processing' },
    { name: 'Complaints Resolution Report', date: '2024-01-11', type: 'Complaints', status: 'completed' }
  ];

  const filteredReports = reportTypes.filter(report => 
    selectedReportType === 'all' || report.id === selectedReportType
  );

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'text-neon-green border-neon-green/30 bg-neon-green/10';
      case 'processing': return 'text-neon-yellow border-neon-yellow/30 bg-neon-yellow/10';
      case 'failed': return 'text-red-400 border-red-400/30 bg-red-400/10';
      default: return 'text-gray-400 border-gray-400/30 bg-gray-400/10';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold gradient-text">Reports & Analytics</h2>
          <p className="text-gray-400 mt-1">Generate and download comprehensive reports</p>
        </div>
        <div className="flex items-center space-x-4">
          <button className="flex items-center space-x-2 px-4 py-3 border border-neon-cyan/30 rounded-xl text-neon-cyan hover:bg-neon-cyan/10 transition-all duration-300">
            <Calendar size={20} />
            <span>Schedule Report</span>
          </button>
          <button className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-neon-green to-neon-cyan rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300 cyber-button">
            <FileText size={20} />
            <span>Generate Custom Report</span>
          </button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {quickStats.map((stat, index) => (
          <div key={index} className={`glass rounded-xl p-4 border border-${stat.color}/30`}>
            <div className="text-center">
              <p className={`text-2xl font-bold text-${stat.color}`}>{stat.value}</p>
              <p className="text-sm text-gray-400">{stat.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="glass rounded-2xl p-6 border border-neon-green/30">
        <div className="flex items-center space-x-4 mb-4">
          <Filter size={20} className="text-neon-green" />
          <h3 className="text-lg font-semibold text-neon-green">Report Filters</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Report Type</label>
            <select 
              value={selectedReportType}
              onChange={(e) => setSelectedReportType(e.target.value)}
              className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none"
            >
              <option value="all">All Report Types</option>
              <option value="faculty-performance">Faculty Performance</option>
              <option value="student-analytics">Student Analytics</option>
              <option value="subject-analysis">Subject Analysis</option>
              <option value="attendance-summary">Attendance Summary</option>
              <option value="complaints-analysis">Complaints Analysis</option>
              <option value="workload-distribution">Workload Distribution</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Time Period</label>
            <select 
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none"
            >
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
              <option value="quarterly">Quarterly</option>
              <option value="yearly">Yearly</option>
              <option value="custom">Custom Range</option>
            </select>
          </div>
        </div>
      </div>

      {/* Available Reports */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredReports.map((report) => {
          const Icon = report.icon;
          return (
            <div
              key={report.id}
              className={`glass rounded-2xl p-6 border border-${report.color}/30 hover-glow transition-all duration-300`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-4">
                  <div className={`w-12 h-12 rounded-full bg-${report.color}/20 border border-${report.color}/30 flex items-center justify-center`}>
                    <Icon size={24} className={`text-${report.color}`} />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">{report.title}</h3>
                    <p className={`text-${report.color} text-sm`}>Last generated: {new Date(report.lastGenerated).toLocaleDateString()}</p>
                  </div>
                </div>
              </div>

              <p className="text-gray-300 text-sm mb-4">{report.description}</p>

              <div className="flex items-center justify-between text-sm text-gray-400 mb-4">
                <span>File size: {report.size}</span>
                <span>Format: PDF, Excel</span>
              </div>

              <div className="flex space-x-3">
                <button className={`flex-1 flex items-center justify-center space-x-2 py-3 bg-${report.color}/20 border border-${report.color}/30 rounded-xl text-${report.color} hover:bg-${report.color}/30 transition-all duration-300`}>
                  <BarChart3 size={16} />
                  <span>Generate</span>
                </button>
                <button className="px-4 py-3 bg-cyber-light border border-gray-600 rounded-xl text-gray-300 hover:bg-cyber-gray transition-colors">
                  <Download size={16} />
                </button>
                <button className="px-4 py-3 bg-cyber-light border border-gray-600 rounded-xl text-gray-300 hover:bg-cyber-gray transition-colors">
                  <Eye size={16} />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Reports */}
      <div className="glass rounded-2xl p-6 border border-neon-purple/30">
        <h3 className="text-xl font-semibold text-neon-purple mb-6">Recent Reports</h3>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-600">
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Report Name</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Type</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Generated</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Status</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {recentReports.map((report, index) => (
                <tr key={index} className="border-b border-gray-700 hover:bg-cyber-light/50 transition-colors">
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-3">
                      <FileText size={16} className="text-neon-cyan" />
                      <span className="text-white font-medium">{report.name}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-gray-300">{report.type}</td>
                  <td className="py-4 px-4 text-gray-300">
                    {new Date(report.date).toLocaleDateString()}
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(report.status)}`}>
                      {report.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-2">
                      {report.status === 'completed' && (
                        <>
                          <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-green/20 text-neon-green transition-colors">
                            <Download size={16} />
                          </button>
                          <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-cyan/20 text-neon-cyan transition-colors">
                            <Eye size={16} />
                          </button>
                        </>
                      )}
                      {report.status === 'processing' && (
                        <div className="flex items-center space-x-2 text-neon-yellow">
                          <div className="w-4 h-4 border-2 border-neon-yellow border-t-transparent rounded-full animate-spin"></div>
                          <span className="text-xs">Processing...</span>
                        </div>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Report Analytics */}
      <div className="glass rounded-2xl p-6 border border-neon-cyan/30">
        <h3 className="text-xl font-semibold text-neon-cyan mb-6">Report Generation Analytics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-cyber-light/30 rounded-xl p-4 border border-gray-600">
            <h4 className="font-semibold text-white mb-3">Most Generated Reports</h4>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Faculty Performance:</span>
                <span className="text-neon-cyan">45</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Student Analytics:</span>
                <span className="text-neon-green">38</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Attendance Summary:</span>
                <span className="text-neon-yellow">32</span>
              </div>
            </div>
          </div>
          
          <div className="bg-cyber-light/30 rounded-xl p-4 border border-gray-600">
            <h4 className="font-semibold text-white mb-3">Generation Frequency</h4>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Daily:</span>
                <span className="text-neon-purple">12</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Weekly:</span>
                <span className="text-neon-cyan">28</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Monthly:</span>
                <span className="text-neon-green">116</span>
              </div>
            </div>
          </div>
          
          <div className="bg-cyber-light/30 rounded-xl p-4 border border-gray-600">
            <h4 className="font-semibold text-white mb-3">Success Rate</h4>
            <div className="text-center">
              <p className="text-3xl font-bold text-neon-green mb-2">98.7%</p>
              <p className="text-sm text-gray-400">Reports generated successfully</p>
              <div className="w-full bg-gray-700 rounded-full h-2 mt-3">
                <div className="bg-neon-green h-2 rounded-full" style={{ width: '98.7%' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;