/**
 * Dashboard component for the Todo application.
 * User dashboard showing personalized information and tasks.
 */

import React, { useState, useEffect } from 'react';
import { useSafeAuth } from '../src/hooks/useSafeAuth';
import TaskList from '../src/components/TaskList';
import TaskForm from '../src/components/TaskForm';
import Header from '../src/components/Header';

const Dashboard = () => {
  const { user, authToken, isAuthenticated, isLoading } = useSafeAuth();
  const [isCheckingAuth, setIsCheckingAuth] = useState(typeof window !== 'undefined');

  // Client-side check to ensure we're only checking auth on the client
  useEffect(() => {
    if (typeof window !== 'undefined') {
      setIsCheckingAuth(false);
    }
  }, []);

  if (isCheckingAuth || isLoading) {
    return (
      <div className="dashboard">
        <Header />
        <div className="dashboard-content">
          <div className="loading">
            <p>Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="dashboard">
        <Header />
        <div className="dashboard-content">
          <h1>Dashboard</h1>
          <p>Please log in to access your dashboard.</p>
        </div>
      </div>
    );
  }

  // Placeholder for user statistics
  const stats = {
    totalTasks: 10, // This would come from an API call in a real app
    completedTasks: 5,
    overdueTasks: 2,
    pendingTasks: 3
  };

  return (
    <div className="dashboard">
      <Header />
      <div className="dashboard-content">
        <div className="welcome-section">
          <h1>Welcome back{user?.username ? `, ${user.username}` : '!'}</h1>
          <p>Manage your tasks and stay productive</p>
        </div>

        <section className="dashboard-stats">
          <div className="stat-card">
            <h3>Total Tasks</h3>
            <p className="stat-number">{stats.totalTasks}</p>
          </div>
          <div className="stat-card">
            <h3>Completed</h3>
            <p className="stat-number">{stats.completedTasks}</p>
          </div>
          <div className="stat-card">
            <h3>Pending</h3>
            <p className="stat-number">{stats.pendingTasks}</p>
          </div>
          <div className="stat-card">
            <h3>Overdue</h3>
            <p className="stat-number">{stats.overdueTasks}</p>
          </div>
        </section>

        <section className="dashboard-content-section">
          <div className="tasks-section">
            <TaskForm authToken={authToken} />
            <TaskList authToken={authToken} />
          </div>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;