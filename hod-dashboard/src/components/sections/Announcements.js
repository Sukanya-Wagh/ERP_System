import React, { useState } from 'react';
import { Plus, Edit, Trash2, Eye, Calendar, User } from 'lucide-react';

const Announcements = () => {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [announcements] = useState([
    {
      id: 1,
      title: 'Faculty Meeting - Monthly Review',
      content: 'All faculty members are requested to attend the monthly review meeting scheduled for tomorrow.',
      date: '2024-01-15',
      author: 'A.S.Bhatlavande',
      priority: 'high',
      status: 'active'
    },
    {
      id: 2,
      title: 'New Academic Guidelines',
      content: 'Updated academic guidelines have been released. Please review the new policies.',
      date: '2024-01-14',
      author: 'A.S.Bhatlavande',
      priority: 'medium',
      status: 'active'
    },
    {
      id: 3,
      title: 'Semester End Preparations',
      content: 'Please prepare all semester end documentation and submit by the deadline.',
      date: '2024-01-13',
      author: 'A.S.Bhatlavande',
      priority: 'low',
      status: 'active'
    }
  ]);

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'text-red-400 border-red-400/30 bg-red-400/10';
      case 'medium': return 'text-yellow-400 border-yellow-400/30 bg-yellow-400/10';
      case 'low': return 'text-green-400 border-green-400/30 bg-green-400/10';
      default: return 'text-gray-400 border-gray-400/30 bg-gray-400/10';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold gradient-text">Announcements Management</h2>
          <p className="text-gray-400 mt-1">Create and manage faculty announcements</p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-neon-purple to-neon-cyan rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300 cyber-button"
        >
          <Plus size={20} />
          <span>New Announcement</span>
        </button>
      </div>

      {/* Create Form Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="glass rounded-2xl p-6 border border-neon-purple/30 w-full max-w-2xl">
            <h3 className="text-xl font-bold text-neon-purple mb-6">Create New Announcement</h3>
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Title</label>
                <input
                  type="text"
                  className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-purple focus:outline-none"
                  placeholder="Enter announcement title"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Content</label>
                <textarea
                  rows="4"
                  className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-purple focus:outline-none resize-none"
                  placeholder="Enter announcement content"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Priority</label>
                  <select className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-purple focus:outline-none">
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Status</label>
                  <select className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-purple focus:outline-none">
                    <option value="active">Active</option>
                    <option value="draft">Draft</option>
                  </select>
                </div>
              </div>
              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  className="flex-1 py-3 bg-gradient-to-r from-neon-purple to-neon-cyan rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300"
                >
                  Create Announcement
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="px-6 py-3 border border-gray-600 rounded-xl text-gray-300 hover:bg-cyber-light transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Announcements List */}
      <div className="space-y-4">
        {announcements.map((announcement) => (
          <div
            key={announcement.id}
            className="glass rounded-2xl p-6 border border-neon-purple/30 hover-glow transition-all duration-300"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-lg font-semibold text-white">{announcement.title}</h3>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(announcement.priority)}`}>
                    {announcement.priority.toUpperCase()}
                  </span>
                </div>
                <p className="text-gray-300 mb-4">{announcement.content}</p>
                <div className="flex items-center space-x-6 text-sm text-gray-400">
                  <div className="flex items-center space-x-2">
                    <Calendar size={16} />
                    <span>{new Date(announcement.date).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <User size={16} />
                    <span>{announcement.author}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-2 ml-4">
                <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-cyan/20 text-neon-cyan transition-colors">
                  <Eye size={16} />
                </button>
                <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-yellow/20 text-neon-yellow transition-colors">
                  <Edit size={16} />
                </button>
                <button className="p-2 rounded-lg bg-cyber-light hover:bg-red-500/20 text-red-400 transition-colors">
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Stats Footer */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass rounded-xl p-4 border border-neon-green/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-green">7</p>
            <p className="text-sm text-gray-400">Active Announcements</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-yellow/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-yellow">2</p>
            <p className="text-sm text-gray-400">Draft Announcements</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-purple/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-purple">15</p>
            <p className="text-sm text-gray-400">Total This Month</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Announcements;