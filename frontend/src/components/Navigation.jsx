import { useAuth } from '../context/AuthContext';
import Link from 'next/link';

const Navigation = () => {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <nav className="navigation">
      <div className="nav-brand">
        <Link href="/">
          <a>Todo App</a>
        </Link>
      </div>
      
      <div className="nav-links">
        {isAuthenticated ? (
          <>
            <Link href="/">
              <a>Dashboard</a>
            </Link>
            <Link href="/tasks">
              <a>Tasks</a>
            </Link>
            <Link href="/profile">
              <a>Profile</a>
            </Link>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link href="/login">
              <a>Login</a>
            </Link>
            <Link href="/signup">
              <a>Sign Up</a>
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navigation;