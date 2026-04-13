import React from 'react';
import { BookOpen, Plus, Edit, Trash2 } from 'lucide-react';

const Subjects = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text font-cyber">Subject Management</h1>
          <p className="text-text-muted mt-1 font-modern">Manage subjects and curriculum</p>
        </div>
        <button className="bg-gradient-to-r from-neon-yellow to-neon-green text-cyber-dark font-bold py-3 px-6 rounded-xl cyber-button hover-glow transition-all duration-300 font-modern flex items-center space-x-2">
          <Plus size={20} />
          <span>Add Subject</span>
        </button>
      </div>
      
      <div className="glass-strong rounded-2xl p-8 border border-neon-yellow/30 hover-glow text-center">
        <BookOpen size={64} className="mx-auto text-neon-yellow mb-4" />
        <h2 className="text-xl font-semibold text-neon-yellow font-cyber mb-2">Subject Management Module</h2>
        <p className="text-text-muted font-modern">This module will contain subject CRUD operations, curriculum management, and subject assignment features.</p>
      </div>
    </div>
  );
};

export default Subjects;