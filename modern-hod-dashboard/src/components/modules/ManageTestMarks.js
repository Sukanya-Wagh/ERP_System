import React, { useState } from 'react';
import { Plus, Edit, Trash2, ClipboardList, TrendingUp } from 'lucide-react';

const ManageTestMarks = () => {
  const [testMarks, setTestMarks] = useState([
    { id: 1, student: 'Jadhav', subject: 'IT-102', testNumber: 'Test 1', marks: 85, percentage: 85, date: '2024-01-15' },
    { id: 2, student: 'Ghanshyam Waghj', subject: 'CS-101', testNumber: 'Test 2', marks: 78, percentage: 78, date: '2024-01-14' },
    { id: 3, student: 'Mayur Kale', subject: 'IT-102', testNumber: 'Test 1', marks: 92, percentage: 92, date: '2024-01-13' },
    { id: 4, student: 'Prashant Patil', subject: 'CS-101', testNumber: 'Test 2', marks: 88, percentage: 88, date: '2024-01-12' },
    { id: 5, student: 'Jayashri', subject: 'IT-102', testNumber: 'Test 1', marks: 76, percentage: 76, date: '2024-01-11' },
    { id: 6, student: 'Shantanu Patil', subject: 'CS-101', testNumber: 'Test 2', marks: 94, percentage: 94, date: '2024-01-10' },
  ]);

  const [newTestMark, setNewTestMark] = useState({
    student: '',
    subject: '',
    testNumber: '',
    testDate: '',
    marksObtained: '',
    totalMarks: ''
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleAddTestMark = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Calculate percentage
    const percentage = (parseInt(newTestMark.marksObtained) / parseInt(newTestMark.totalMarks)) * 100;
    
    // Simulate API call
    setTimeout(() => {
      const newMark = {
        id: testMarks.length + 1,
        student: newTestMark.student,
        subject: newTestMark.subject,
        testNumber: newTestMark.testNumber,
        marks: parseInt(newTestMark.marksObtained),
        percentage: Math.round(percentage),
        date: newTestMark.testDate
      };
      setTestMarks([...testMarks, newMark]);
      setNewTestMark({
        student: '',
        subject: '',
        testNumber: '',
        testDate: '',
        marksObtained: '',
        totalMarks: ''
      });
      setIsLoading(false);
    }, 1000);
  };

  const handleDeleteMark = (id) => {
    setTestMarks(testMarks.filter(mark => mark.id !== id));
  };

  const getPercentageBadgeClass = (percentage) => {
    if (percentage >= 90) return 'badge badge-success';
    if (percentage >= 75) return 'badge badge-primary';
    if (percentage >= 60) return 'badge badge-warning';
    return 'badge badge-error';
  };

  const getTestNumberBadgeClass = (testNumber) => {
    const colors = ['badge-primary', 'badge-purple', 'badge-success', 'badge-warning'];
    const index = parseInt(testNumber.replace('Test ', '')) - 1;
    return `badge ${colors[index % colors.length]}`;
  };

  const averagePercentage = testMarks.reduce((sum, mark) => sum + mark.percentage, 0) / testMarks.length;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text font-cyber">Manage Test Marks</h1>
          <p className="text-text-muted mt-1 font-modern">Oversee and manage class test marks for all subjects</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <TrendingUp size={24} className="text-neon-green" />
            <span className="text-neon-green font-bold text-lg">{Math.round(averagePercentage)}%</span>
            <span className="text-text-muted text-sm">Avg Score</span>
          </div>
          <div className="flex items-center space-x-2">
            <ClipboardList size={24} className="text-neon-cyan" />
            <span className="text-neon-cyan font-bold text-lg">{testMarks.length}</span>
            <span className="text-text-muted text-sm">Total Tests</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Add Test Marks Form */}
        <div className="glass-strong rounded-2xl p-6 border border-neon-cyan/30 hover-glow card-hover animate-delay-100">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-cyan to-neon-teal flex items-center justify-center">
              <Plus size={20} className="text-cyber-dark" />
            </div>
            <h2 className="text-xl font-semibold text-neon-cyan font-cyber">Add Test Marks</h2>
          </div>

          <form onSubmit={handleAddTestMark} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Student</label>
              <input
                type="text"
                value={newTestMark.student}
                onChange={(e) => setNewTestMark({...newTestMark, student: e.target.value})}
                className="w-full p-3 rounded-xl cyber-input font-modern"
                placeholder="Enter student name"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Subject</label>
              <select
                value={newTestMark.subject}
                onChange={(e) => setNewTestMark({...newTestMark, subject: e.target.value})}
                className="w-full p-3 rounded-xl cyber-input font-modern"
                required
              >
                <option value="">Select Subject</option>
                <option value="IT-102">IT-102 - Data Analytics</option>
                <option value="CS-101">CS-101 - User Analytics</option>
                <option value="IT-103">IT-103 - Database Systems</option>
                <option value="CS-102">CS-102 - Web Development</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Test Number</label>
                <select
                  value={newTestMark.testNumber}
                  onChange={(e) => setNewTestMark({...newTestMark, testNumber: e.target.value})}
                  className="w-full p-3 rounded-xl cyber-input font-modern"
                  required
                >
                  <option value="">Select Test</option>
                  <option value="Test 1">Test 1</option>
                  <option value="Test 2">Test 2</option>
                  <option value="Test 3">Test 3</option>
                  <option value="Test 4">Test 4</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Test Date</label>
                <input
                  type="date"
                  value={newTestMark.testDate}
                  onChange={(e) => setNewTestMark({...newTestMark, testDate: e.target.value})}
                  className="w-full p-3 rounded-xl cyber-input font-modern"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Marks Obtained</label>
                <input
                  type="number"
                  value={newTestMark.marksObtained}
                  onChange={(e) => setNewTestMark({...newTestMark, marksObtained: e.target.value})}
                  className="w-full p-3 rounded-xl cyber-input font-modern"
                  placeholder="e.g., 85"
                  min="0"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2 font-modern">Total Marks</label>
                <input
                  type="number"
                  value={newTestMark.totalMarks}
                  onChange={(e) => setNewTestMark({...newTestMark, totalMarks: e.target.value})}
                  className="w-full p-3 rounded-xl cyber-input font-modern"
                  placeholder="e.g., 100"
                  min="1"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-neon-cyan to-neon-teal text-cyber-dark font-bold py-3 px-6 rounded-xl cyber-button hover-glow transition-all duration-300 font-modern"
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="loading-spinner"></div>
                  <span>Adding Marks...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center space-x-2">
                  <Plus size={20} />
                  <span>Add Marks</span>
                </div>
              )}
            </button>
          </form>
        </div>

        {/* Recent Test Marks */}
        <div className="glass-strong rounded-2xl p-6 border border-neon-purple/30 hover-glow card-hover animate-delay-200">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-purple to-neon-pink flex items-center justify-center">
              <ClipboardList size={20} className="text-cyber-dark" />
            </div>
            <h2 className="text-xl font-semibold text-neon-purple font-cyber">Recent Test Marks</h2>
          </div>

          {/* Test Marks Table */}
          <div className="overflow-hidden rounded-xl border border-cyber-border max-h-96 overflow-y-auto">
            <table className="w-full cyber-table">
              <thead className="sticky top-0">
                <tr>
                  <th className="text-left">Student</th>
                  <th className="text-left">Subject</th>
                  <th className="text-left">Test #</th>
                  <th className="text-left">Marks</th>
                  <th className="text-left">Percentage</th>
                  <th className="text-left">Date</th>
                  <th className="text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {testMarks.map((mark) => (
                  <tr key={mark.id} className="group">
                    <td className="font-medium text-text-primary font-modern">{mark.student}</td>
                    <td className="text-neon-cyan font-modern">{mark.subject}</td>
                    <td>
                      <span className={`badge ${getTestNumberBadgeClass(mark.testNumber)}`}>
                        {mark.testNumber}
                      </span>
                    </td>
                    <td className="text-text-secondary font-modern">{mark.marks}</td>
                    <td>
                      <span className={getPercentageBadgeClass(mark.percentage)}>
                        {mark.percentage}%
                      </span>
                    </td>
                    <td className="text-text-muted font-modern text-sm">
                      {new Date(mark.date).toLocaleDateString()}
                    </td>
                    <td>
                      <div className="flex items-center space-x-2">
                        <button className="p-2 rounded-lg bg-cyber-surface hover:bg-neon-yellow/20 text-neon-yellow transition-colors">
                          <Edit size={16} />
                        </button>
                        <button 
                          onClick={() => handleDeleteMark(mark.id)}
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

          {testMarks.length === 0 && (
            <div className="text-center py-8">
              <ClipboardList size={48} className="mx-auto text-text-muted mb-4" />
              <p className="text-text-muted font-modern">No test marks found</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ManageTestMarks;