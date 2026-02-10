import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

// Safe hook to use the AuthContext without throwing errors
export const useSafeAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    // Return a default state when not in provider context
    return {
      user: null,
      authToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: 'Not in AuthProvider context',
      login: () => Promise.resolve({ success: false, error: 'Not in AuthProvider context' }),
      signup: () => Promise.resolve({ success: false, error: 'Not in AuthProvider context' }),
      logout: () => {},
      clearError: () => {},
    };
  }
  return context;
};