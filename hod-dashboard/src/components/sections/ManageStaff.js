import React, { useState } from 'react';
import { Plus, Edit, Trash2, Eye, Mail, Phone, User, Search } from 'lucide-react';

const ManageStaff = () => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [staff] = useState([
    {
      id: 1,
      name: 'Dr. Rajesh Kumar',
      email: 'rajesh.kumar@college.edu',
      phone: '+91 9876543210',
      department: 'Computer Science',
      designation: 'Professor',
      experience: '15 years',
      subjects: ['Data Structures', 'Algorithms'],
      status: 'active'
    },
    {
      id: 2,
      name: 'Prof. Priya Sharma',
      email: 'priya.sharma@college.edu',
      phone: '+91 9876543211',
      department: 'Computer Science',
      designation: 'Associate Professor',
      experience: '10 years',
      subjects: ['Database Systems', 'Web Development'],
      status: 'active'
    },
    {
      id: 3,
      name: 'Dr. Amit Patel',
      email: 'amit.patel@college.edu',
      phone: '+91 9876543212',
      department: 'Computer Science',
      designation: 'Assistant Professor',
      experience: '8 years',
      subjects: ['Machine Learning', 'AI'],
      status: 'active'
    },
    {
      id: 4,
      name: 'Prof. Sneha Gupta',
      email: 'sneha.gupta@college.edu',
      phone: '+91 9876543213',
      department: 'Computer Science',
      designation: 'Assistant Professor',
      experience: '6 years',
      subjects: ['Software Engineering', 'Project Management'],
      status: 'active'
    }
  ]);

  const filteredStaff = staff.filter(member =>
    member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    member.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    member.designation.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold gradient-text">Staff Management</h2>
          <p className="text-gray-400 mt-1">Manage faculty members in your department</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search staff..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none w-64"
            />
          </div>
          <button
            onClick={() => setShowAddForm(true)}
            className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-neon-green to-neon-cyan rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300 cyber-button"
          >
            <Plus size={20} />
            <span>Add Staff</span>
          </button>
        </div>
      </div>

      {/* Add Staff Form Modal */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="glass rounded-2xl p-6 border border-neon-green/30 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-bold text-neon-green mb-6">Add New Staff Member</h3>
            <form className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Full Name</label>
                  <input
                    type="text"
                    className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none"
                    placeholder="Enter full name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
                  <input
                    type="email"
                    className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none"
                    placeholder="Enter email address"
                  />
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Phone</label>
                  <input
                    type="tel"
                    className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none"
                    placeholder="Enter phone number"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Designation</label>
                  <select className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none">
                    <option value="">Select designation</option>
                    <option value="Professor">Professor</option>
                    <option value="Associate Professor">Associate Professor</option>
                    <option value="Assistant Professor">Assistant Professor</option>
                    <option value="Lecturer">Lecturer</option>
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Department</label>
                  <input
                    type="text"
                    className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none"
                    placeholder="Enter department"
                    defaultValue="Computer Science"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Experience</label>
                  <input
                    type="text"
                    className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none"
                    placeholder="e.g., 5 years"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Subjects (comma separated)</label>
                <input
                  type="text"
                  className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-green focus:outline-none"
                  placeholder="e.g., Data Structures, Algorithms"
                />
              </div>
              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  className="flex-1 py-3 bg-gradient-to-r from-neon-green to-neon-cyan rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300"
                >
                  Add Staff Member
                </button>
                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="px-6 py-3 border border-gray-600 rounded-xl text-gray-300 hover:bg-cyber-light transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Staff Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredStaff.map((member) => (
          <div
            key={member.id}
            className="glass rounded-2xl p-6 border border-neon-green/30 hover-glow transition-all duration-300"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-neon-green to-neon-cyan flex items-center justify-center">
                  <User size={24} className="text-black" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">{member.name}</h3>
                  <p className="text-neon-green text-sm">{member.designation}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
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

            <div className="space-y-3">
              <div className="flex items-center space-x-3 text-sm text-gray-300">
                <Mail size={16} className="text-neon-cyan" />
                <span>{member.email}</span>
              </div>
              <div className="flex items-center space-x-3 text-sm text-gray-300">
                <Phone size={16} className="text-neon-green" />
                <span>{member.phone}</span>
              </div>
              <div className="text-sm text-gray-300">
                <span className="text-neon-yellow">Experience:</span> {member.experience}
              </div>
              <div className="text-sm text-gray-300">
                <span className="text-neon-purple">Subjects:</span>
                <div className="flex flex-wrap gap-2 mt-2">
                  {member.subjects.map((subject, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-neon-purple/20 border border-neon-purple/30 rounded-lg text-xs text-neon-purple"
                    >
                      {subject}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Stats Footer */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass rounded-xl p-4 border border-neon-green/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-green">4</p>
            <p className="text-sm text-gray-400">Total Faculty</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-cyan/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-cyan">1</p>
            <p className="text-sm text-gray-400">Professors</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-yellow/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-yellow">1</p>
            <p className="text-sm text-gray-400">Associate Professors</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-purple/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-purple">2</p>
            <p className="text-sm text-gray-400">Assistant Professors</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ManageStaff;