import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import MainContent from './MainContent';

const Dashboard = () => {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div className="flex h-screen bg-cyber-dark overflow-hidden">
      <Sidebar 
        activeSection={activeSection}
        setActiveSection={setActiveSection}
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
      />
      <div className="flex-1 flex flex-col">
        <Header 
          activeSection={activeSection}
          toggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
        />
        <MainContent activeSection={activeSection} />
      </div>
    </div>
  );
};

export default Dashboard;