import React, { useState } from 'react';
import { Calendar, Check, X, Clock, User, FileText, Filter } from 'lucide-react';

const LeaveRequests = () => {
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  
  const leaveRequests = [
    {
      id: 1,
      faculty: 'Dr. Rajesh Kumar',
      type: 'Medical Leave',
      startDate: '2024-01-20',
      endDate: '2024-01-22',
      days: 3,
      reason: 'Medical treatment and recovery',
      status: 'pending',
      appliedDate: '2024-01-15',
      documents: true
    },
    {
      id: 2,
      faculty: 'Prof. Priya Sharma',
      type: 'Personal Leave',
      startDate: '2024-01-25',
      endDate: '2024-01-26',
      days: 2,
      reason: 'Family function attendance',
      status: 'approved',
      appliedDate: '2024-01-12',
      documents: false
    },
    {
      id: 3,
      faculty: 'Dr. Amit Patel',
      type: 'Conference',
      startDate: '2024-02-01',
      endDate: '2024-02-03',
      days: 3,
      reason: 'Attending International AI Conference',
      status: 'pending',
      appliedDate: '2024-01-10',
      documents: true
    },
    {
      id: 4,
      faculty: 'Prof. Sneha Gupta',
      type: 'Emergency Leave',
      startDate: '2024-01-18',
      endDate: '2024-01-19',
      days: 2,
      reason: 'Family emergency',
      status: 'approved',
      appliedDate: '2024-01-17',
      documents: false
    },
    {
      id: 5,
      faculty: 'Dr. Rajesh Kumar',
      type: 'Casual Leave',
      startDate: '2024-01-30',
      endDate: '2024-01-30',
      days: 1,
      reason: 'Personal work',
      status: 'rejected',
      appliedDate: '2024-01-14',
      documents: false,
      rejectionReason: 'Important class scheduled'
    }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'text-neon-yellow border-neon-yellow/30 bg-neon-yellow/10';
      case 'approved': return 'text-neon-green border-neon-green/30 bg-neon-green/10';
      case 'rejected': return 'text-red-400 border-red-400/30 bg-red-400/10';
      default: return 'text-gray-400 border-gray-400/30 bg-gray-400/10';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'Medical Leave': return 'text-red-400 border-red-400/30 bg-red-400/10';
      case 'Personal Leave': return 'text-neon-cyan border-neon-cyan/30 bg-neon-cyan/10';
      case 'Conference': return 'text-neon-purple border-neon-purple/30 bg-neon-purple/10';
      case 'Emergency Leave': return 'text-neon-yellow border-neon-yellow/30 bg-neon-yellow/10';
      case 'Casual Leave': return 'text-neon-green border-neon-green/30 bg-neon-green/10';
      default: return 'text-gray-400 border-gray-400/30 bg-gray-400/10';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending': return <Clock size={16} />;
      case 'approved': return <Check size={16} />;
      case 'rejected': return <X size={16} />;
      default: return <Clock size={16} />;
    }
  };

  const filteredRequests = leaveRequests.filter(request => {
    const statusMatch = selectedStatus === 'all' || request.status === selectedStatus;
    const typeMatch = selectedType === 'all' || request.type === selectedType;
    return statusMatch && typeMatch;
  });

  const getLeaveStats = () => {
    const total = leaveRequests.length;
    const pending = leaveRequests.filter(r => r.status === 'pending').length;
    const approved = leaveRequests.filter(r => r.status === 'approved').length;
    const rejected = leaveRequests.filter(r => r.status === 'rejected').length;
    
    return { total, pending, approved, rejected };
  };

  const stats = getLeaveStats();

  const handleApprove = (id) => {
    console.log('Approving leave request:', id);
  };

  const handleReject = (id) => {
    console.log('Rejecting leave request:', id);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold gradient-text">Leave Requests</h2>
          <p className="text-gray-400 mt-1">Review and manage faculty leave requests</p>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass rounded-xl p-4 border border-neon-purple/30">
          <div className="text-center">
            <Calendar size={24} className="text-neon-purple mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-purple">{stats.total}</p>
            <p className="text-sm text-gray-400">Total Requests</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-yellow/30">
          <div className="text-center">
            <Clock size={24} className="text-neon-yellow mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-yellow">{stats.pending}</p>
            <p className="text-sm text-gray-400">Pending</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-green/30">
          <div className="text-center">
            <Check size={24} className="text-neon-green mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-green">{stats.approved}</p>
            <p className="text-sm text-gray-400">Approved</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-red-400/30">
          <div className="text-center">
            <X size={24} className="text-red-400 mx-auto mb-2" />
            <p className="text-2xl font-bold text-red-400">{stats.rejected}</p>
            <p className="text-sm text-gray-400">Rejected</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="glass rounded-2xl p-6 border border-neon-purple/30">
        <div className="flex items-center space-x-4 mb-4">
          <Filter size={20} className="text-neon-purple" />
          <h3 className="text-lg font-semibold text-neon-purple">Filters</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Status</label>
            <select 
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-purple focus:outline-none"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Leave Type</label>
            <select 
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-purple focus:outline-none"
            >
              <option value="all">All Types</option>
              <option value="Medical Leave">Medical Leave</option>
              <option value="Personal Leave">Personal Leave</option>
              <option value="Conference">Conference</option>
              <option value="Emergency Leave">Emergency Leave</option>
              <option value="Casual Leave">Casual Leave</option>
            </select>
          </div>
        </div>
      </div>

      {/* Leave Requests List */}
      <div className="space-y-4">
        {filteredRequests.map((request) => (
          <div
            key={request.id}
            className="glass rounded-2xl p-6 border border-neon-purple/30 hover-glow transition-all duration-300"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-neon-purple to-neon-cyan flex items-center justify-center">
                  <User size={24} className="text-black" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">{request.faculty}</h3>
                  <div className="flex items-center space-x-3 mt-1">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getTypeColor(request.type)}`}>
                      {request.type}
                    </span>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border flex items-center space-x-1 ${getStatusColor(request.status)}`}>
                      {getStatusIcon(request.status)}
                      <span>{request.status.toUpperCase()}</span>
                    </span>
                  </div>
                </div>
              </div>
              
              {request.documents && (
                <div className="flex items-center space-x-2 text-neon-cyan">
                  <FileText size={16} />
                  <span className="text-xs">Documents Attached</span>
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4 text-sm">
              <div>
                <span className="text-neon-cyan">Start Date:</span>
                <p className="text-white">{new Date(request.startDate).toLocaleDateString()}</p>
              </div>
              <div>
                <span className="text-neon-green">End Date:</span>
                <p className="text-white">{new Date(request.endDate).toLocaleDateString()}</p>
              </div>
              <div>
                <span className="text-neon-yellow">Duration:</span>
                <p className="text-white">{request.days} day{request.days > 1 ? 's' : ''}</p>
              </div>
              <div>
                <span className="text-neon-purple">Applied:</span>
                <p className="text-white">{new Date(request.appliedDate).toLocaleDateString()}</p>
              </div>
            </div>

            <div className="mb-4">
              <span className="text-neon-pink">Reason:</span>
              <p className="text-gray-300 mt-1">{request.reason}</p>
            </div>

            {request.status === 'rejected' && request.rejectionReason && (
              <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                <span className="text-red-400">Rejection Reason:</span>
                <p className="text-red-300 mt-1">{request.rejectionReason}</p>
              </div>
            )}

            {/* Action Buttons */}
            {request.status === 'pending' && (
              <div className="flex space-x-3 pt-4 border-t border-gray-600">
                <button 
                  onClick={() => handleApprove(request.id)}
                  className="flex items-center space-x-2 px-4 py-2 bg-neon-green/20 border border-neon-green/30 rounded-lg text-neon-green hover:bg-neon-green/30 transition-colors"
                >
                  <Check size={16} />
                  <span>Approve</span>
                </button>
                <button 
                  onClick={() => handleReject(request.id)}
                  className="flex items-center space-x-2 px-4 py-2 bg-red-500/20 border border-red-500/30 rounded-lg text-red-400 hover:bg-red-500/30 transition-colors"
                >
                  <X size={16} />
                  <span>Reject</span>
                </button>
                {request.documents && (
                  <button className="flex items-center space-x-2 px-4 py-2 bg-neon-cyan/20 border border-neon-cyan/30 rounded-lg text-neon-cyan hover:bg-neon-cyan/30 transition-colors">
                    <FileText size={16} />
                    <span>View Documents</span>
                  </button>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Leave Type Breakdown */}
      <div className="glass rounded-2xl p-6 border border-neon-cyan/30">
        <h3 className="text-xl font-semibold text-neon-cyan mb-6">Leave Requests by Type</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {['Medical Leave', 'Personal Leave', 'Conference', 'Emergency Leave', 'Casual Leave'].map((type, index) => {
            const typeRequests = leaveRequests.filter(r => r.type === type);
            const colors = ['red-400', 'neon-cyan', 'neon-purple', 'neon-yellow', 'neon-green'];
            const color = colors[index];
            
            return (
              <div key={type} className={`bg-cyber-light/30 rounded-xl p-4 border border-${color}/30`}>
                <div className="text-center">
                  <p className={`text-2xl font-bold text-${color}`}>{typeRequests.length}</p>
                  <p className="text-xs text-gray-400">{type}</p>
                  <div className="mt-2">
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div 
                        className={`bg-${color} h-2 rounded-full transition-all duration-300`}
                        style={{ width: `${typeRequests.length > 0 ? (typeRequests.length / leaveRequests.length) * 100 : 0}%` }}
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

export default LeaveRequests;