/**
 * Header component for the Todo application
 */

import React from 'react';
import { useRouter } from 'next/router';
import { useSafeAuth } from '../hooks/useSafeAuth';

const Header = () => {
  const router = useRouter();
  const { user, logout, isAuthenticated } = useSafeAuth();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <header className="app-header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <h1>TaskFlow</h1>
          </div>

          <nav className="nav-menu">
            <a href="/" className={router.pathname === '/' ? 'active' : ''}>Dashboard</a>
            <a href="/tasks" className={router.pathname === '/tasks' ? 'active' : ''}>Tasks</a>
            <a href="/chat" className={router.pathname === '/chat' ? 'active' : ''}>AI Assistant</a>
          </nav>

          <div className="header-actions">
            {isAuthenticated && user && (
              <div className="user-info">
                <span className="user-name">{user.email || user.username}</span>
                <button onClick={handleLogout} className="logout-btn">Logout</button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;