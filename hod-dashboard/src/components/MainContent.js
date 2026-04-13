import React from 'react';
import DashboardOverview from './sections/DashboardOverview';
import Announcements from './sections/Announcements';
import ManageStaff from './sections/ManageStaff';
import Subjects from './sections/Subjects';
import AssignSubjects from './sections/AssignSubjects';
import TestMarks from './sections/TestMarks';
import Complaints from './sections/Complaints';
import LeaveRequests from './sections/LeaveRequests';
import Reports from './sections/Reports';

const MainContent = ({ activeSection }) => {
  const renderSection = () => {
    switch (activeSection) {
      case 'dashboard':
        return <DashboardOverview />;
      case 'announcements':
        return <Announcements />;
      case 'manage-staff':
        return <ManageStaff />;
      case 'subjects':
        return <Subjects />;
      case 'assign-subjects':
        return <AssignSubjects />;
      case 'test-marks':
        return <TestMarks />;
      case 'complaints':
        return <Complaints />;
      case 'leave-requests':
        return <LeaveRequests />;
      case 'reports':
        return <Reports />;
      default:
        return <DashboardOverview />;
    }
  };

  return (
    <main className="flex-1 overflow-y-auto bg-cyber-dark p-6">
      <div className="max-w-7xl mx-auto">
        {renderSection()}
      </div>
    </main>
  );
};

export default MainContent;