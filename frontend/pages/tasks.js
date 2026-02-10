/**
 * Tasks page for the Todo application
 */

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useSafeAuth } from '../src/hooks/useSafeAuth';
import TasksPageComponent from './TasksPage';
import Header from '../src/components/Header';

export default function Tasks() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading } = useSafeAuth();
  const [isCheckingAuth, setIsCheckingAuth] = useState(typeof window !== 'undefined');

  // Client-side check to ensure we're only checking auth on the client
  useEffect(() => {
    if (typeof window !== 'undefined') {
      setIsCheckingAuth(false);
    }
  }, []);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated && typeof window !== 'undefined') {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isCheckingAuth || isLoading) {
    return (
      <div>
        <Header />
        <div className="loading">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    return (
      <div>
        <Header />
        <div className="tasks-page-content">
          <TasksPageComponent />
        </div>
      </div>
    );
  }

  return (
    <div>
      <Header />
      <div className="loading">
        <p>Loading...</p>
      </div>
    </div>
  );
}