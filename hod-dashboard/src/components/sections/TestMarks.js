import React, { useState } from 'react';
import { ClipboardList, Upload, Download, Eye, BarChart3, Filter } from 'lucide-react';

const TestMarks = () => {
  const [selectedSubject, setSelectedSubject] = useState('all');
  const [selectedSemester, setSelectedSemester] = useState('all');
  
  const testData = [
    {
      id: 1,
      subject: 'Data Structures and Algorithms',
      semester: 3,
      testType: 'Mid-term',
      date: '2024-01-15',
      totalStudents: 45,
      submitted: 42,
      avgScore: 78.5,
      maxScore: 95,
      minScore: 45,
      faculty: 'Dr. Rajesh Kumar'
    },
    {
      id: 2,
      subject: 'Database Management Systems',
      semester: 3,
      testType: 'Quiz 1',
      date: '2024-01-12',
      totalStudents: 42,
      submitted: 40,
      avgScore: 82.3,
      maxScore: 98,
      minScore: 52,
      faculty: 'Prof. Priya Sharma'
    },
    {
      id: 3,
      subject: 'Machine Learning',
      semester: 4,
      testType: 'Assignment',
      date: '2024-01-10',
      totalStudents: 38,
      submitted: 35,
      avgScore: 75.8,
      maxScore: 92,
      minScore: 48,
      faculty: 'Dr. Amit Patel'
    },
    {
      id: 4,
      subject: 'Software Engineering',
      semester: 3,
      testType: 'Mid-term',
      date: '2024-01-08',
      totalStudents: 40,
      submitted: 38,
      avgScore: 80.2,
      maxScore: 96,
      minScore: 55,
      faculty: 'Prof. Sneha Gupta'
    }
  ];

  const subjects = ['Data Structures and Algorithms', 'Database Management Systems', 'Machine Learning', 'Software Engineering'];
  
  const filteredTests = testData.filter(test => {
    const subjectMatch = selectedSubject === 'all' || test.subject === selectedSubject;
    const semesterMatch = selectedSemester === 'all' || test.semester.toString() === selectedSemester;
    return subjectMatch && semesterMatch;
  });

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-neon-green';
    if (score >= 60) return 'text-neon-yellow';
    return 'text-red-400';
  };

  const getSubmissionRate = (submitted, total) => {
    return ((submitted / total) * 100).toFixed(1);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold gradient-text">Test Marks Management</h2>
          <p className="text-gray-400 mt-1">Monitor and manage class test performance</p>
        </div>
        <div className="flex items-center space-x-4">
          <button className="flex items-center space-x-2 px-4 py-3 border border-neon-green/30 rounded-xl text-neon-green hover:bg-neon-green/10 transition-all duration-300">
            <Upload size={20} />
            <span>Upload Marks</span>
          </button>
          <button className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-neon-cyan to-neon-purple rounded-xl text-black font-medium hover:shadow-glow transition-all duration-300 cyber-button">
            <BarChart3 size={20} />
            <span>Analytics</span>
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="glass rounded-2xl p-6 border border-neon-cyan/30">
        <div className="flex items-center space-x-4 mb-4">
          <Filter size={20} className="text-neon-cyan" />
          <h3 className="text-lg font-semibold text-neon-cyan">Filters</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Subject</label>
            <select 
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-cyan focus:outline-none"
            >
              <option value="all">All Subjects</option>
              {subjects.map((subject, index) => (
                <option key={index} value={subject}>{subject}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Semester</label>
            <select 
              value={selectedSemester}
              onChange={(e) => setSelectedSemester(e.target.value)}
              className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-cyan focus:outline-none"
            >
              <option value="all">All Semesters</option>
              {[1,2,3,4,5,6,7,8].map(sem => (
                <option key={sem} value={sem}>Semester {sem}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Test Type</label>
            <select className="w-full p-3 rounded-xl bg-cyber-light border border-gray-600 text-white focus:border-neon-cyan focus:outline-none">
              <option value="all">All Types</option>
              <option value="midterm">Mid-term</option>
              <option value="quiz">Quiz</option>
              <option value="assignment">Assignment</option>
            </select>
          </div>
        </div>
      </div>

      {/* Test Results Table */}
      <div className="glass rounded-2xl p-6 border border-neon-cyan/30">
        <h3 className="text-xl font-semibold text-neon-cyan mb-6">Test Results Overview</h3>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-600">
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Subject</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Test Type</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Date</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Submission</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Avg Score</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Range</th>
                <th className="text-left py-3 px-4 text-gray-300 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredTests.map((test) => (
                <tr key={test.id} className="border-b border-gray-700 hover:bg-cyber-light/50 transition-colors">
                  <td className="py-4 px-4">
                    <div>
                      <div className="font-medium text-white">{test.subject}</div>
                      <div className="text-sm text-gray-400">Sem {test.semester} • {test.faculty}</div>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <span className="px-3 py-1 bg-neon-purple/20 border border-neon-purple/30 rounded-full text-xs font-medium text-neon-purple">
                      {test.testType}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-gray-300">
                    {new Date(test.date).toLocaleDateString()}
                  </td>
                  <td className="py-4 px-4">
                    <div className="text-sm">
                      <div className="text-white">{test.submitted}/{test.totalStudents}</div>
                      <div className="text-neon-cyan">({getSubmissionRate(test.submitted, test.totalStudents)}%)</div>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`text-lg font-bold ${getScoreColor(test.avgScore)}`}>
                      {test.avgScore}%
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <div className="text-sm">
                      <div className="text-neon-green">Max: {test.maxScore}%</div>
                      <div className="text-red-400">Min: {test.minScore}%</div>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-2">
                      <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-cyan/20 text-neon-cyan transition-colors">
                        <Eye size={16} />
                      </button>
                      <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-green/20 text-neon-green transition-colors">
                        <Download size={16} />
                      </button>
                      <button className="p-2 rounded-lg bg-cyber-light hover:bg-neon-purple/20 text-neon-purple transition-colors">
                        <BarChart3 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Performance Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass rounded-xl p-4 border border-neon-cyan/30">
          <div className="text-center">
            <ClipboardList size={24} className="text-neon-cyan mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-cyan">12</p>
            <p className="text-sm text-gray-400">Total Tests</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-green/30">
          <div className="text-center">
            <BarChart3 size={24} className="text-neon-green mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-green">79.2%</p>
            <p className="text-sm text-gray-400">Overall Average</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-yellow/30">
          <div className="text-center">
            <Upload size={24} className="text-neon-yellow mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-yellow">92.5%</p>
            <p className="text-sm text-gray-400">Submission Rate</p>
          </div>
        </div>
        <div className="glass rounded-xl p-4 border border-neon-purple/30">
          <div className="text-center">
            <Eye size={24} className="text-neon-purple mx-auto mb-2" />
            <p className="text-2xl font-bold text-neon-purple">165</p>
            <p className="text-sm text-gray-400">Total Students</p>
          </div>
        </div>
      </div>

      {/* Subject Performance Chart */}
      <div className="glass rounded-2xl p-6 border border-neon-purple/30">
        <h3 className="text-xl font-semibold text-neon-purple mb-6">Subject Performance Overview</h3>
        <div className="space-y-4">
          {subjects.map((subject, index) => {
            const subjectTests = testData.filter(test => test.subject === subject);
            const avgScore = subjectTests.reduce((sum, test) => sum + test.avgScore, 0) / subjectTests.length;
            
            return (
              <div key={index} className="bg-cyber-light/30 rounded-xl p-4 border border-gray-600">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-medium text-white">{subject}</h4>
                  <span className={`font-bold ${getScoreColor(avgScore)}`}>
                    {avgScore.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-neon-purple to-neon-cyan h-3 rounded-full transition-all duration-500"
                    style={{ width: `${avgScore}%` }}
                  ></div>
                </div>
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>{subjectTests.length} tests</span>
                  <span>Target: 75%</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default TestMarks;