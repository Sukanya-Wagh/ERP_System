import React, { useState } from 'react';
import { AlertTriangle, Eye, MessageSquare, Clock, CheckCircle, XCircle, Filter } from 'lucide-react';

const Complaints = () => {
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [selectedPriority, setSelectedPriority] = useState('all');
  
  const complaints = [
    {
      id: 1,
      title: 'Lab Equipment Not Working',
      description: 'Several computers in Lab 3 are not functioning properly, affecting practical sessions.',
      student: 'Rahul Sharma',
      rollNo: 'CS2021001',
      category: 'Infrastructure',
      priority: 'high',
      status: 'pending',
      date: '2024-01-15',
      faculty: 'Dr. Rajesh Kumar'
    },
    {
      id: 2,
      title: 'Unclear Assignment Instructions',
      description: 'The assignment instructions for Database Systems are confusing and need clarification.',
      student: 'Priya Patel',
      rollNo: 'CS2021002',
      category: 'Academic',
      priority: 'medium',
      status: 'in-progress',
      date: '2024-01-14',
      faculty: 'Prof. Priya Sharma'
    },
    {
      id: 3,
      title: 'Attendance Marking Issue',
      description: 'My attendance was not marked properly for the last three classes.',
      student: 'Amit Kumar',
      rollNo: 'CS2021003',
      category: 'Administrative',
      priority: 'low',
      status: 'resolved',
      date: '2024-01-13',
      faculty: 'Dr. Amit Patel'
    },
    {
      id: 4,
      title: 'Library Access Problem',
      description: 'Unable to access digital library resources from home network.',
      student: 'Sneha Gupta',
      rollNo: 'CS2021004',
      category: 'Technical',
      priority: 'medium',
      status: 'pending',
      date: '2024-01-12',
      faculty: 'Prof. Sneha Gupta'
    },
    {
      id: 5,
      title: 'Exam Schedule Conflict',
      description: 'Two exams are scheduled at the same time causing conflict.',
      student: 'Ravi Singh',
      rollNo: 'CS2021005',
      category: 'Academic',
      priority: 'high',
      status: 'in-progress',
      date: '2024-01-11',
      faculty: 'Dr. Rajesh Kumar'
    }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'text-neon-yellow border-neon-yellow/30 bg-neon-yellow/10';
      case 'in-progress': return 'text-neon-cyan border-neon-cyan/30 bg-neon-cyan/10';
      case 'resolved': return 'text-neon-green border-neon-green/30 bg-neon-green/10';
      case 'rejected': return 'text-red-400 border-red-400/30 bg-red-400/10';
      default: return 'text-gray-400 border-gray-400/30 bg-gray-400/10';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'text-red-400 border-red-400/30 bg-red-400/10';
      case 'medium': return 'text-neon-yellow border-neon-yellow/30 bg-neon-yellow/10';
      case 'low': return 'text-neon-green border-neon-green/30 bg-neon-green/10';
      default: return 'text-gray-400 border-gray-400/30 bg-gray-400/10';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending': return <Clock size={16} />;
      case 'in-progress': return <MessageSquare size={16} />;
      case 'resolved': return <CheckCircle size={16} />;
      case 'rejected': return <XCircle size={16} />;
      default: return <AlertTriangle size={16} />;
    }
  };

  const filteredComplaints = complaints.filter(complaint => {
    const statusMatch = selectedStatus === 'all' || complaint.status === selectedStatus;
    const priorityMatch = selectedPriority === 'all' || complaint.priority === selectedPriority;
    return statusMatch && priorityMatch;
  });

  const getComplaintStats = () => {
    const total = complaints.length;
    const pending = complaints.filter(c => c.status === 'pending').length;
    const inProgress = complaints.filter(c => c.status === 'in-progress').length;
    const resolved = complaints.filter(c => c.status === 'resolved').length;
    
    return { total, pending, inProgress, resolved };
  };

  const stats = getComplaintStats();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold gradient-text">Complaints Management</h2>
          <p className="text-gray-400 mt-1">Monitor and resolve student complaints</p>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass rounded-xl p-4 border border-neon-yellow/30">
          <div className="text-center">
            <AlertTriangle size={24} className="text-neon-yellow mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-yellow">{stats.total}</p>
            <p className="text-sm text-gray-400">Total Complaints</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-yellow/30">
          <div className="text-center">
            <Clock size={24} className="text-neon-yellow mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-yellow">{stats.pending}</p>
            <p className="text-sm text-gray-400">Pending</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-cyan/30">
          <div className="text-center">
            <MessageSquare size={24} className="text-neon-cyan mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-cyan">{stats.inProgress}</p>
            <p className="text-sm text-gray-400">In Progress</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-green/30">
          <div className="text-center">
            <CheckCircle size={24} className="text-neon-green mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-green">{stats.resolved}</p>
            <p className="text-sm text-gray-400">Resolved</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="glass rounded-2xl p-6 border border-neon-yellow/30">
        <div className="flex items-center space-x-4 mb-4">
          <Filter size={20} className="text-neon-yellow" />
          <h3 className="text-lg font-semibold text-neon-yellow">Filters</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Status</label>
            <select 
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-yellow focus:outline-none"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="in-progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Priority</label>
            <select 
              value={selectedPriority}
              onChange={(e) => setSelectedPriority(e.target.value)}
              className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-yellow focus:outline-none"
            >
              <option value="all">All Priorities</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </div>
      </div>

      {/* Complaints List */}
      <div className="space-y-4">
        {filteredComplaints.map((complaint) => (
          <div
            key={complaint.id}
            className="glass rounded-2xl p-6 border border-neon-yellow/30 hover-glow transition-all duration-300"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-lg font-semibold text-white">{complaint.title}</h3>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium border flex items-center space-x-1 ${getStatusColor(complaint.status)}`}>
                    {getStatusIcon(complaint.status)}
                    <span>{complaint.status.replace('-', ' ').toUpperCase()}</span>
                  </span>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(complaint.priority)}`}>
                    {complaint.priority.toUpperCase()}
                  </span>
                </div>
                <p className="text-gray-300 mb-4">{complaint.description}</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-neon-cyan">Student:</span>
                    <p className="text-white">{complaint.student}</p>
                    <p className="text-gray-400">{complaint.rollNo}</p>
                  </div>
                  <div>
                    <span className="text-neon-green">Category:</span>
                    <p className="text-white">{complaint.category}</p>
                  </div>
                  <div>
                    <span className="text-neon-purple">Faculty:</span>
                    <p className="text-white">{complaint.faculty}</p>
                  </div>
                  <div>
                    <span className="text-neon-yellow">Date:</span>
                    <p className="text-white">{new Date(complaint.date).toLocaleDateString()}</p>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-2 ml-4">
                <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-cyan/20 text-neon-cyan transition-colors">
                  <Eye size={16} />
                </button>
                <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-green/20 text-neon-green transition-colors">
                  <MessageSquare size={16} />
                </button>
              </div>
            </div>

            {/* Action Buttons */}
            {complaint.status !== 'resolved' && complaint.status !== 'rejected' && (
              <div className="flex space-x-3 pt-4 border-t border-gray-600">
                <button className="px-4 py-2 bg-neon-green/20 border border-neon-green/30 rounded-lg text-neon-green hover:bg-neon-green/30 transition-colors text-sm">
                  Mark as Resolved
                </button>
                <button className="px-4 py-2 bg-neon-cyan/20 border border-neon-cyan/30 rounded-lg text-neon-cyan hover:bg-neon-cyan/30 transition-colors text-sm">
                  Update Status
                </button>
                <button className="px-4 py-2 bg-red-500/20 border border-red-500/30 rounded-lg text-red-400 hover:bg-red-500/30 transition-colors text-sm">
                  Reject
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Category Breakdown */}
      <div className="glass rounded-2xl p-6 border border-neon-purple/30">
        <h3 className="text-xl font-semibold text-neon-purple mb-6">Complaints by Category</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {['Academic', 'Infrastructure', 'Administrative', 'Technical'].map((category, index) => {
            const categoryComplaints = complaints.filter(c => c.category === category);
            const colors = ['neon-cyan', 'neon-green', 'neon-yellow', 'neon-purple'];
            const color = colors[index];
            
            return (
              <div key={category} className={`bg-cyber-light/30 rounded-xl p-4 border border-${color}/30`}>
                <div className="text-center">
                  <p className={`text-2xl font-bold text-${color}`}>{categoryComplaints.length}</p>
                  <p className="text-sm text-gray-400">{category}</p>
                  <div className="mt-2">
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div 
                        className={`bg-${color} h-2 rounded-full transition-all duration-300`}
                        style={{ width: `${(categoryComplaints.length / complaints.length) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Complaints;