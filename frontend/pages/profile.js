import { useAuth } from '../src/context/AuthContext';
import ProtectedRoute from '../src/components/ProtectedRoute';
import Head from 'next/head';

export default function ProfilePage() {
  const { user } = useAuth();

  return (
    <ProtectedRoute>
      <div className="profile-page">
        <Head>
          <title>Profile - Todo App</title>
          <meta name="description" content="Your profile" />
        </Head>
        
        <header className="profile-header">
          <h1>Your Profile</h1>
        </header>
        
        <main className="profile-main">
          <div className="profile-info">
            <h2>Account Information</h2>
            <div className="info-item">
              <label>Name:</label>
              <span>{user?.name}</span>
            </div>
            <div className="info-item">
              <label>Email:</label>
              <span>{user?.email}</span>
            </div>
            <div className="info-item">
              <label>Member Since:</label>
              <span>{user?.createdAt ? new Date(user.createdAt).toLocaleDateString() : 'N/A'}</span>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}