import React from 'react';
import { Calendar, Check, X } from 'lucide-react';

const LeaveRequests = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text font-cyber">Leave Requests</h1>
          <p className="text-text-muted mt-1 font-modern">Review and manage faculty leave requests</p>
        </div>
      </div>
      
      <div className="glass-strong rounded-2xl p-8 border border-neon-purple/30 hover-glow text-center">
        <Calendar size={64} className="mx-auto text-neon-purple mb-4" />
        <h2 className="text-xl font-semibold text-neon-purple font-cyber mb-2">Leave Requests Module</h2>
        <p className="text-text-muted font-modern">This module will handle leave request approvals, calendar management, and notification system.</p>
      </div>
    </div>
  );
};

export default LeaveRequests;