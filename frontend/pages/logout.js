import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../src/context/AuthContext';

export default function LogoutPage() {
  const { logout, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      logout();
    }
  }, [loading, logout]);

  return (
    <div className="logout-page">
      <p>Logging out...</p>
    </div>
  );
}