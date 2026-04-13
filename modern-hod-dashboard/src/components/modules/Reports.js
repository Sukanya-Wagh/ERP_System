import React from 'react';
import { FileText, Download, BarChart3 } from 'lucide-react';

const Reports = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text font-cyber">Reports & Analytics</h1>
          <p className="text-text-muted mt-1 font-modern">Generate and download comprehensive reports</p>
        </div>
        <button className="bg-gradient-to-r from-neon-teal to-neon-cyan text-cyber-dark font-bold py-3 px-6 rounded-xl cyber-button hover-glow transition-all duration-300 font-modern flex items-center space-x-2">
          <BarChart3 size={20} />
          <span>Generate Report</span>
        </button>
      </div>
      
      <div className="glass-strong rounded-2xl p-8 border border-neon-teal/30 hover-glow text-center">
        <FileText size={64} className="mx-auto text-neon-teal mb-4" />
        <h2 className="text-xl font-semibold text-neon-teal font-cyber mb-2">Reports & Analytics Module</h2>
        <p className="text-text-muted font-modern">This module will provide comprehensive reporting, data visualization, and export functionality.</p>
      </div>
    </div>
  );
};

export default Reports;