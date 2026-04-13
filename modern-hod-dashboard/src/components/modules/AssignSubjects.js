import React from 'react';
import { UserCheck, Users, BookOpen } from 'lucide-react';

const AssignSubjects = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text font-cyber">Subject Assignment</h1>
          <p className="text-text-muted mt-1 font-modern">Assign subjects to faculty members</p>
        </div>
      </div>
      
      <div className="glass-strong rounded-2xl p-8 border border-neon-pink/30 hover-glow text-center">
        <UserCheck size={64} className="mx-auto text-neon-pink mb-4" />
        <h2 className="text-xl font-semibold text-neon-pink font-cyber mb-2">Subject Assignment Module</h2>
        <p className="text-text-muted font-modern">This module will handle faculty-subject assignments, workload distribution, and scheduling.</p>
      </div>
    </div>
  );
};

export default AssignSubjects;