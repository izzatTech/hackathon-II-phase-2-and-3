import { useAuth } from '../src/context/AuthContext';
import ProtectedRoute from '../src/components/ProtectedRoute';
import Head from 'next/head';

export default function Home() {
  const { user } = useAuth();

  return (
    <ProtectedRoute>
      <div className="dashboard">
        <Head>
          <title>Todo Dashboard</title>
          <meta name="description" content="Your Todo Dashboard" />
        </Head>
        
        <header className="dashboard-header">
          <h1>Welcome, {user?.name || user?.email}!</h1>
          <p>Your Todo Dashboard</p>
        </header>
        
        <main className="dashboard-main">
          <div className="dashboard-content">
            <div className="quick-stats">
              <div className="stat-card">
                <h3>Total Tasks</h3>
                <p>0</p>
              </div>
              <div className="stat-card">
                <h3>Completed</h3>
                <p>0</p>
              </div>
              <div className="stat-card">
                <h3>Pending</h3>
                <p>0</p>
              </div>
            </div>
            
            <div className="dashboard-actions">
              <a href="/tasks" className="btn-primary">View Tasks</a>
              <a href="/profile" className="btn-secondary">Profile</a>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}