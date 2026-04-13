import React, { useState } from 'react';
import { Plus, Edit, Trash2, Megaphone, Calendar, User } from 'lucide-react';

const Announcements = () => {
  const [announcements, setAnnouncements] = useState([
    {
      id: 1,
      title: 'Faculty Meeting - Monthly Review',
      content: 'All faculty members are requested to attend the monthly review meeting scheduled for tomorrow at 10:00 AM in the conference room.',
      date: '2024-01-15',
      author: 'A.S.Bhatlavande',
      priority: 'high',
      status: 'active'
    },
    {
      id: 2,
      title: 'New Academic Guidelines',
      content: 'Updated academic guidelines have been released. Please review the new policies and implement them in your respective subjects.',
      date: '2024-01-14',
      author: 'A.S.Bhatlavande',
      priority: 'medium',
      status: 'active'
    },
    {
      id: 3,
      title: 'Semester End Preparations',
      content: 'Please prepare all semester end documentation and submit by the deadline. Ensure all test marks are updated.',
      date: '2024-01-13',
      author: 'A.S.Bhatlavande',
      priority: 'low',
      status: 'active'
    }
  ]);

  const [newAnnouncement, setNewAnnouncement] = useState({
    title: '',
    content: '',
    priority: 'medium'
  });

  const [showForm, setShowForm] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleAddAnnouncement = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    setTimeout(() => {
      const announcement = {
        id: announcements.length + 1,
        ...newAnnouncement,
        date: new Date().toISOString().split('T')[0],
        author: 'A.S.Bhatlavande',
        status: 'active'
      };
      setAnnouncements([announcement, ...announcements]);
      setNewAnnouncement({ title: '', content: '', priority: 'medium' });
      setShowForm(false);
      setIsLoading(false);
    }, 1000);
  };

  const handleDeleteAnnouncement = (id) => {
    setAnnouncements(announcements.filter(ann => ann.id !== id));
  };

  const getPriorityBadgeClass = (priority) => {
    switch (priority) {
      case 'high': return 'badge bg-error/20 text-error border-error/40';
      case 'medium': return 'badge badge-warning';
      case 'low': return 'badge badge-success';
      default: return 'badge badge-primary';
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text font-cyber">Announcements Management</h1>
          <p className="text-text-muted mt-1 font-modern">Create and manage faculty announcements</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-gradient-to-r from-neon-purple to-neon-pink text-cyber-dark font-bold py-3 px-6 rounded-xl cyber-button hover-glow transition-all duration-300 font-modern flex items-center space-x-2"
        >
          <Plus size={20} />
          <span>New Announcement</span>
        </button>
      </div>

      {/* Create Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="glass-strong rounded-2xl p-6 border border-neon-purple/30 w-full max-w-2xl">
            <h3 className="text-xl font-bold text-neon-purple font-cyber mb-6">Create New Announcement</h3>
            <form onSubmit={handleAddAnnouncement} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Title</label>
                <input
                  type="text"
                  value={newAnnouncement.title}
                  onChange={(e) => setNewAnnouncement({...newAnnouncement, title: e.target.value})}
                  className="w-full p-3 rounded-xl cyber-input font-modern"
                  placeholder="Enter announcement title"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Content</label>
                <textarea
                  rows="4"
                  value={newAnnouncement.content}
                  onChange={(e) => setNewAnnouncement({...newAnnouncement, content: e.target.value})}
                  className="w-full p-3 rounded-xl cyber-input font-modern resize-none"
                  placeholder="Enter announcement content"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Priority</label>
                <select
                  value={newAnnouncement.priority}
                  onChange={(e) => setNewAnnouncement({...newAnnouncement, priority: e.target.value})}
                  className="w-full p-3 rounded-xl cyber-input font-modern"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="flex-1 py-3 bg-gradient-to-r from-neon-purple to-neon-pink text-cyber-dark font-bold rounded-xl cyber-button hover-glow transition-all duration-300 font-modern"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="loading-spinner"></div>
                      <span>Creating...</span>
                    </div>
                  ) : (
                    'Create Announcement'
                  )}
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="px-6 py-3 border border-cyber-border rounded-xl text-text-secondary hover:bg-cyber-surface transition-colors font-modern"
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
        {announcements.map((announcement, index) => (
          <div
            key={announcement.id}
            className={`glass-strong rounded-2xl p-6 border border-neon-purple/30 hover-glow card-hover animate-delay-${(index + 1) * 100}`}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-lg font-semibold text-text-primary font-modern">{announcement.title}</h3>
                  <span className={getPriorityBadgeClass(announcement.priority)}>
                    {announcement.priority.toUpperCase()}
                  </span>
                </div>
                <p className="text-text-secondary mb-4 font-modern">{announcement.content}</p>
                <div className="flex items-center space-x-6 text-sm text-text-muted">
                  <div className="flex items-center space-x-2">
                    <Calendar size={16} />
                    <span className="font-modern">{new Date(announcement.date).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <User size={16} />
                    <span className="font-modern">{announcement.author}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-2 ml-4">
                <button className="p-2 rounded-lg bg-cyber-surface hover:bg-neon-yellow/20 text-neon-yellow transition-colors">
                  <Edit size={16} />
                </button>
                <button 
                  onClick={() => handleDeleteAnnouncement(announcement.id)}
                  className="p-2 rounded-lg bg-cyber-surface hover:bg-error/20 text-error transition-colors"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Stats Footer */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-strong rounded-xl p-4 border border-neon-green/30 text-center">
          <p className="text-2xl font-bold text-neon-green font-cyber">7</p>
          <p className="text-sm text-text-muted font-modern">Active Announcements</p>
        </div>
        <div className="glass-strong rounded-xl p-4 border border-neon-yellow/30 text-center">
          <p className="text-2xl font-bold text-neon-yellow font-cyber">2</p>
          <p className="text-sm text-text-muted font-modern">Draft Announcements</p>
        </div>
        <div className="glass-strong rounded-xl p-4 border border-neon-purple/30 text-center">
          <p className="text-2xl font-bold text-neon-purple font-cyber">15</p>
          <p className="text-sm text-text-muted font-modern">Total This Month</p>
        </div>
      </div>
    </div>
  );
};

export default Announcements;