import React, { useState } from 'react';
import { Plus, Trash2, Eye, Search, UserPlus, Users } from 'lucide-react';

const ManageStaff = () => {
  const [staffMembers, setStaffMembers] = useState([
    { id: 1, username: 'S.Mahajan', fullName: 'Sonal Mahajan', role: 'Faculty', email: 'sonal@college.edu' },
    { id: 2, username: 'Faculty_User', fullName: 'Faculty User', role: 'Faculty', email: 'faculty@college.edu' },
    { id: 3, username: 'K.Mahajan', fullName: 'K.Mahajan', role: 'Faculty', email: 'k.mahajan@college.edu' },
    { id: 4, username: 'CC_User', fullName: 'CC User', role: 'CC', email: 'cc@college.edu' },
    { id: 5, username: 'M.B.Patil', fullName: 'M.B.Patil', role: 'Faculty', email: 'm.patil@college.edu' },
    { id: 6, username: 'A.A.Jadhav', fullName: 'A.A.Jadhav', role: 'Faculty', email: 'a.jadhav@college.edu' },
  ]);

  const [newStaff, setNewStaff] = useState({
    username: '',
    password: '',
    fullName: '',
    email: '',
    role: 'Faculty'
  });

  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleAddStaff = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      const newMember = {
        id: staffMembers.length + 1,
        ...newStaff
      };
      setStaffMembers([...staffMembers, newMember]);
      setNewStaff({
        username: '',
        password: '',
        fullName: '',
        email: '',
        role: 'Faculty'
      });
      setIsLoading(false);
    }, 1000);
  };

  const handleRemoveStaff = (id) => {
    setStaffMembers(staffMembers.filter(member => member.id !== id));
  };

  const filteredStaff = staffMembers.filter(member =>
    member.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    member.fullName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    member.role.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getRoleBadgeClass = (role) => {
    switch (role) {
      case 'Faculty':
        return 'badge badge-primary';
      case 'CC':
        return 'badge badge-purple';
      default:
        return 'badge badge-success';
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text font-cyber">Staff Management</h1>
          <p className="text-text-muted mt-1 font-modern">Add or remove faculty members from your department</p>
        </div>
        <div className="flex items-center space-x-2">
          <Users size={24} className="text-neon-cyan" />
          <span className="text-neon-cyan font-bold text-lg">{staffMembers.length}</span>
          <span className="text-text-muted text-sm">Total Staff</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Add New Staff Member Form */}
        <div className="glass-strong rounded-2xl p-6 border border-neon-cyan/30 hover-glow card-hover animate-delay-100">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-cyan to-neon-teal flex items-center justify-center">
              <UserPlus size={20} className="text-cyber-dark" />
            </div>
            <h2 className="text-xl font-semibold text-neon-cyan font-cyber">Add New Staff Member</h2>
          </div>

          <form onSubmit={handleAddStaff} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Username</label>
              <input
                type="text"
                value={newStaff.username}
                onChange={(e) => setNewStaff({...newStaff, username: e.target.value})}
                className="w-full p-3 rounded-xl cyber-input font-modern"
                placeholder="Enter username"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Password</label>
              <input
                type="password"
                value={newStaff.password}
                onChange={(e) => setNewStaff({...newStaff, password: e.target.value})}
                className="w-full p-3 rounded-xl cyber-input font-modern"
                placeholder="Enter password"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Full Name</label>
              <input
                type="text"
                value={newStaff.fullName}
                onChange={(e) => setNewStaff({...newStaff, fullName: e.target.value})}
                className="w-full p-3 rounded-xl cyber-input font-modern"
                placeholder="Enter full name"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Email</label>
              <input
                type="email"
                value={newStaff.email}
                onChange={(e) => setNewStaff({...newStaff, email: e.target.value})}
                className="w-full p-3 rounded-xl cyber-input font-modern"
                placeholder="Enter email address"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Role</label>
              <select
                value={newStaff.role}
                onChange={(e) => setNewStaff({...newStaff, role: e.target.value})}
                className="w-full p-3 rounded-xl cyber-input font-modern"
                required
              >
                <option value="Faculty">Faculty</option>
                <option value="CC">CC</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-neon-cyan to-neon-teal text-cyber-dark font-bold py-3 px-6 rounded-xl cyber-button hover-glow transition-all duration-300 font-modern"
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="loading-spinner"></div>
                  <span>Adding Staff...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center space-x-2">
                  <Plus size={20} />
                  <span>Add Staff</span>
                </div>
              )}
            </button>
          </form>
        </div>

        {/* Current Staff Members */}
        <div className="glass-strong rounded-2xl p-6 border border-neon-purple/30 hover-glow card-hover animate-delay-200">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-purple to-neon-pink flex items-center justify-center">
                <Users size={20} className="text-cyber-dark" />
              </div>
              <h2 className="text-xl font-semibold text-neon-purple font-cyber">Current Staff Members</h2>
            </div>
          </div>

          {/* Search */}
          <div className="relative mb-4">
            <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-text-muted" />
            <input
              type="text"
              placeholder="Search staff..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-xl cyber-input font-modern"
            />
          </div>

          {/* Staff Table */}
          <div className="overflow-hidden rounded-xl border border-cyber-border">
            <table className="w-full cyber-table">
              <thead>
                <tr>
                  <th className="text-left">Username</th>
                  <th className="text-left">Full Name</th>
                  <th className="text-left">Role</th>
                  <th className="text-left">Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredStaff.map((member) => (
                  <tr key={member.id} className="group">
                    <td className="font-medium text-text-primary font-modern">{member.username}</td>
                    <td className="text-text-secondary font-modern">{member.fullName}</td>
                    <td>
                      <span className={getRoleBadgeClass(member.role)}>
                        {member.role}
                      </span>
                    </td>
                    <td>
                      <div className="flex items-center space-x-2">
                        <button className="p-2 rounded-lg bg-cyber-surface hover:bg-neon-cyan/20 text-neon-cyan transition-colors">
                          <Eye size={16} />
                        </button>
                        <button 
                          onClick={() => handleRemoveStaff(member.id)}
                          className="p-2 rounded-lg bg-cyber-surface hover:bg-error/20 text-error transition-colors"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredStaff.length === 0 && (
            <div className="text-center py-8">
              <Users size={48} className="mx-auto text-text-muted mb-4" />
              <p className="text-text-muted font-modern">No staff members found</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ManageStaff;