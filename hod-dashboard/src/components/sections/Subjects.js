import React, { useState } from 'react';
import { Plus, Edit, Trash2, BookOpen, Search, Clock, Users } from 'lucide-react';

const Subjects = () => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [subjects] = useState([
    {
      id: 1,
      name: 'Data Structures and Algorithms',
      code: 'CS301',
      credits: 4,
      semester: 3,
      type: 'Core',
      faculty: 'Dr. Rajesh Kumar',
      students: 45,
      description: 'Fundamental concepts of data structures and algorithmic problem solving'
    },
    {
      id: 2,
      name: 'Database Management Systems',
      code: 'CS302',
      credits: 4,
      semester: 3,
      type: 'Core',
      faculty: 'Prof. Priya Sharma',
      students: 42,
      description: 'Design and implementation of database systems'
    },
    {
      id: 3,
      name: 'Machine Learning',
      code: 'CS401',
      credits: 3,
      semester: 4,
      type: 'Elective',
      faculty: 'Dr. Amit Patel',
      students: 38,
      description: 'Introduction to machine learning algorithms and applications'
    },
    {
      id: 4,
      name: 'Software Engineering',
      code: 'CS303',
      credits: 3,
      semester: 3,
      type: 'Core',
      faculty: 'Prof. Sneha Gupta',
      students: 40,
      description: 'Software development lifecycle and project management'
    }
  ]);

  const filteredSubjects = subjects.filter(subject =>
    subject.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    subject.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    subject.faculty.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getTypeColor = (type) => {
    switch (type) {
      case 'Core': return 'text-neon-cyan border-neon-cyan/30 bg-neon-cyan/10';
      case 'Elective': return 'text-neon-purple border-neon-purple/30 bg-neon-purple/10';
      case 'Lab': return 'text-neon-green border-neon-green/30 bg-neon-green/10';
      default: return 'text-gray-400 border-gray-400/30 bg-gray-400/10';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold gradient-text">Subject Management</h2>
          <p className="text-gray-400 mt-1">Manage subjects and curriculum</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search subjects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-yellow focus:outline-none w-64"
            />
          </div>
          <button
            onClick={() => setShowAddForm(true)}
            className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-neon-yellow to-neon-green rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300 cyber-button"
          >
            <Plus size={20} />
            <span>Add Subject</span>
          </button>
        </div>
      </div>

      {/* Add Subject Form Modal */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="glass rounded-2xl p-6 border border-neon-yellow/30 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-bold text-neon-yellow mb-6">Add New Subject</h3>
            <form className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Subject Name</label>
                  <input
                    type="text"
                    className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-yellow focus:outline-none"
                    placeholder="Enter subject name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Subject Code</label>
                  <input
                    type="text"
                    className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-yellow focus:outline-none"
                    placeholder="e.g., CS301"
                  />
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Credits</label>
                  <input
                    type="number"
                    className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-yellow focus:outline-none"
                    placeholder="Credits"
                    min="1"
                    max="6"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Semester</label>
                  <select className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-yellow focus:outline-none">
                    <option value="">Select semester</option>
                    {[1,2,3,4,5,6,7,8].map(sem => (
                      <option key={sem} value={sem}>Semester {sem}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Type</label>
                  <select className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-yellow focus:outline-none">
                    <option value="">Select type</option>
                    <option value="Core">Core</option>
                    <option value="Elective">Elective</option>
                    <option value="Lab">Lab</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Description</label>
                <textarea
                  rows="3"
                  className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-yellow focus:outline-none resize-none"
                  placeholder="Enter subject description"
                />
              </div>
              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  className="flex-1 py-3 bg-gradient-to-r from-neon-yellow to-neon-green rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300"
                >
                  Add Subject
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

      {/* Subjects Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredSubjects.map((subject) => (
          <div
            key={subject.id}
            className="glass rounded-2xl p-6 border border-neon-yellow/30 hover-glow transition-all duration-300"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-neon-yellow to-neon-green flex items-center justify-center">
                  <BookOpen size={24} className="text-black" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">{subject.name}</h3>
                  <p className="text-neon-yellow text-sm">{subject.code}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getTypeColor(subject.type)}`}>
                  {subject.type}
                </span>
                <div className="flex items-center space-x-1">
                  <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-yellow/20 text-neon-yellow transition-colors">
                    <Edit size={16} />
                  </button>
                  <button className="p-2 rounded-lg bg-cyber-light hover:bg-red-500/20 text-red-400 transition-colors">
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <p className="text-gray-300 text-sm">{subject.description}</p>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center space-x-2 text-sm">
                  <Clock size={16} className="text-neon-cyan" />
                  <span className="text-gray-300">
                    <span className="text-neon-cyan">Credits:</span> {subject.credits}
                  </span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <Users size={16} className="text-neon-green" />
                  <span className="text-gray-300">
                    <span className="text-neon-green">Students:</span> {subject.students}
                  </span>
                </div>
              </div>

              <div className="text-sm">
                <span className="text-neon-purple">Semester:</span>
                <span className="text-gray-300 ml-2">{subject.semester}</span>
              </div>

              <div className="text-sm">
                <span className="text-neon-pink">Faculty:</span>
                <span className="text-gray-300 ml-2">{subject.faculty}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Stats Footer */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass rounded-xl p-4 border border-neon-yellow/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-yellow">12</p>
            <p className="text-sm text-gray-400">Total Subjects</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-cyan/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-cyan">8</p>
            <p className="text-sm text-gray-400">Core Subjects</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-purple/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-purple">3</p>
            <p className="text-sm text-gray-400">Electives</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-green/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-green">1</p>
            <p className="text-sm text-gray-400">Lab Subjects</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Subjects;