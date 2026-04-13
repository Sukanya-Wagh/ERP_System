import React from 'react';
import { AlertTriangle, Eye, MessageSquare } from 'lucide-react';

const Complaints = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text font-cyber">Complaints Management</h1>
          <p className="text-text-muted mt-1 font-modern">Monitor and resolve student complaints</p>
        </div>
      </div>
      
      <div className="glass-strong rounded-2xl p-8 border border-neon-yellow/30 hover-glow text-center">
        <AlertTriangle size={64} className="mx-auto text-neon-yellow mb-4" />
        <h2 className="text-xl font-semibold text-neon-yellow font-cyber mb-2">Complaints Management Module</h2>
        <p className="text-text-muted font-modern">This module will handle complaint tracking, resolution workflow, and status management.</p>
      </div>
    </div>
  );
};

export default Complaints;