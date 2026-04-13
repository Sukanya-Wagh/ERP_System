import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './components/modules/Dashboard';
import ManageStaff from './components/modules/ManageStaff';
import ManageTestMarks from './components/modules/ManageTestMarks';
import Announcements from './components/modules/Announcements';
import Subjects from './components/modules/Subjects';
import AssignSubjects from './components/modules/AssignSubjects';
import Complaints from './components/modules/Complaints';
import LeaveRequests from './components/modules/LeaveRequests';
import Reports from './components/modules/Reports';

function App() {
  const [activeModule, setActiveModule] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const renderActiveModule = () => {
    switch (activeModule) {
      case 'dashboard':
        return <Dashboard />;
      case 'announcements':
        return <Announcements />;
      case 'manage-staff':
        return <ManageStaff />;
      case 'subjects':
        return <Subjects />;
      case 'assign-subjects':
        return <AssignSubjects />;
      case 'test-marks':
        return <ManageTestMarks />;
      case 'complaints':
        return <Complaints />;
      case 'leave-requests':
        return <LeaveRequests />;
      case 'reports':
        return <Reports />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-cyber-dark">
      {/* Background Grid Pattern */}
      <div className="fixed inset-0 opacity-20 pointer-events-none">
        <div className="absolute inset-0" style={{
          backgroundImage: `
            linear-gradient(rgba(0, 245, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 245, 255, 0.1) 1px, transparent 1px)
          `,
          backgroundSize: '20px 20px'
        }}></div>
      </div>

      <div className="flex h-screen relative">
        {/* Sidebar */}
        <Sidebar 
          activeModule={activeModule}
          setActiveModule={setActiveModule}
          collapsed={sidebarCollapsed}
          setCollapsed={setSidebarCollapsed}
        />

        {/* Main Content */}
        <div className={`flex-1 flex flex-col transition-all duration-300 ${
          sidebarCollapsed ? 'ml-16' : 'ml-64'
        }`}>
          {/* Header */}
          <Header 
            activeModule={activeModule}
            toggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
          />

          {/* Content Area */}
          <main className="flex-1 overflow-y-auto p-6 bg-gradient-to-br from-cyber-dark via-cyber-darker to-cyber-dark">
            <div className="max-w-7xl mx-auto">
              {renderActiveModule()}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;