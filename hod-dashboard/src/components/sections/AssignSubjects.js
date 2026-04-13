import React, { useState } from 'react';
import { UserCheck, BookOpen, Plus, Save, RefreshCw } from 'lucide-react';

const AssignSubjects = () => {
  const [assignments, setAssignments] = useState([
    { id: 1, faculty: 'Dr. Rajesh Kumar', subject: 'Data Structures and Algorithms', semester: 3, students: 45 },
    { id: 2, faculty: 'Prof. Priya Sharma', subject: 'Database Management Systems', semester: 3, students: 42 },
    { id: 3, faculty: 'Dr. Amit Patel', subject: 'Machine Learning', semester: 4, students: 38 },
    { id: 4, faculty: 'Prof. Sneha Gupta', subject: 'Software Engineering', semester: 3, students: 40 }
  ]);

  const [showAssignForm, setShowAssignForm] = useState(false);
  
  const faculty = [
    'Dr. Rajesh Kumar',
    'Prof. Priya Sharma', 
    'Dr. Amit Patel',
    'Prof. Sneha Gupta'
  ];

  const subjects = [
    { name: 'Data Structures and Algorithms', code: 'CS301', semester: 3 },
    { name: 'Database Management Systems', code: 'CS302', semester: 3 },
    { name: 'Machine Learning', code: 'CS401', semester: 4 },
    { name: 'Software Engineering', code: 'CS303', semester: 3 },
    { name: 'Computer Networks', code: 'CS304', semester: 4 },
    { name: 'Operating Systems', code: 'CS305', semester: 4 }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold gradient-text">Subject Assignment</h2>
          <p className="text-gray-400 mt-1">Assign subjects to faculty members</p>
        </div>
        <div className="flex items-center space-x-4">
          <button className="flex items-center space-x-2 px-4 py-3 border border-neon-cyan/30 rounded-xl text-neon-cyan hover:bg-neon-cyan/10 transition-all duration-300">
            <RefreshCw size={20} />
            <span>Refresh</span>
          </button>
          <button
            onClick={() => setShowAssignForm(true)}
            className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-neon-pink to-neon-purple rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300 cyber-button"
          >
            <Plus size={20} />
            <span>New Assignment</span>
          </button>
        </div>
      </div>

      {/* Assignment Form Modal */}
      {showAssignForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="glass rounded-2xl p-6 border border-neon-pink/30 w-full max-w-2xl">
            <h3 className="text-xl font-bold text-neon-pink mb-6">Create New Assignment</h3>
            <form className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Faculty Member</label>
                  <select className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-pink focus:outline-none">
                    <option value="">Select faculty</option>
                    {faculty.map((member, index) => (
                      <option key={index} value={member}>{member}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Subject</label>
                  <select className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-pink focus:outline-none">
                    <option value="">Select subject</option>
                    {subjects.map((subject, index) => (
                      <option key={index} value={subject.name}>
                        {subject.name} ({subject.code})
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Semester</label>
                  <select className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-pink focus:outline-none">
                    <option value="">Select semester</option>
                    {[1,2,3,4,5,6,7,8].map(sem => (
                      <option key={sem} value={sem}>Semester {sem}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Expected Students</label>
                  <input
                    type="number"
                    className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-pink focus:outline-none"
                    placeholder="Number of students"
                    min="1"
                  />
                </div>
              </div>
              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  className="flex-1 py-3 bg-gradient-to-r from-neon-pink to-neon-purple rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300"
                >
                  Create Assignment
                </button>
                <button
                  type="button"
                  onClick={() => setShowAssignForm(false)}
                  className="px-6 py-3 border border-gray-600 rounded-xl text-gray-300 hover:bg-cyber-light transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Current Assignments */}
      <div className="glass rounded-2xl p-6 border border-neon-pink/30">
        <h3 className="text-xl font-semibold text-neon-pink mb-6">Current Subject Assignments</h3>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-600">
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Faculty Member</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Subject</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Semester</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Students</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {assignments.map((assignment) => (
                <tr key={assignment.id} className="border-b border-gray-700 hover:bg-cyber-light/50 transition-colors">
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-neon-pink to-neon-purple flex items-center justify-center">
                        <UserCheck size={16} className="text-black" />
                      </div>
                      <span className="text-white font-medium">{assignment.faculty}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-3">
                      <BookOpen size={16} className="text-neon-cyan" />
                      <span className="text-gray-300">{assignment.subject}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <span className="px-3 py-1 bg-neon-yellow/20 border border-neon-yellow/30 rounded-full text-xs font-medium text-neon-yellow">
                      Semester {assignment.semester}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <span className="text-neon-green font-medium">{assignment.students}</span>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-2">
                      <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-cyan/20 text-neon-cyan transition-colors">
                        <Save size={16} />
                      </button>
                      <button className="p-2 rounded-lg bg-cyber-light hover:bg-red-500/20 text-red-400 transition-colors">
                        <RefreshCw size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Assignment Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass rounded-xl p-4 border border-neon-pink/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-pink">4</p>
            <p className="text-sm text-gray-400">Total Assignments</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-cyan/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-cyan">4</p>
            <p className="text-sm text-gray-400">Faculty Assigned</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-green/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-green">165</p>
            <p className="text-sm text-gray-400">Total Students</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-yellow/30">
          <div className="text-center">
            <p className="text-2xl font-bold text-neon-yellow">2</p>
            <p className="text-sm text-gray-400">Semesters Covered</p>
          </div>
        </div>
      </div>

      {/* Faculty Workload Overview */}
      <div className="glass rounded-2xl p-6 border border-neon-cyan/30">
        <h3 className="text-xl font-semibold text-neon-cyan mb-6">Faculty Workload Overview</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {faculty.map((member, index) => {
            const memberAssignments = assignments.filter(a => a.faculty === member);
            const totalStudents = memberAssignments.reduce((sum, a) => sum + a.students, 0);
            
            return (
              <div key={index} className="bg-cyber-light/30 rounded-xl p-4 border border-gray-600">
                <h4 className="font-semibold text-white mb-3">{member}</h4>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Subjects:</span>
                    <span className="text-neon-cyan">{memberAssignments.length}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Total Students:</span>
                    <span className="text-neon-green">{totalStudents}</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2 mt-3">
                    <div 
                      className="bg-gradient-to-r from-neon-cyan to-neon-green h-2 rounded-full transition-all duration-300"
                      style={{ width: `${Math.min((totalStudents / 50) * 100, 100)}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default AssignSubjects;