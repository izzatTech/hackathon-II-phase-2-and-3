import { useAuth } from './AuthContext';

// Custom hook to get the auth token
export const useAuthToken = () => {
  const { user } = useAuth();
  return user?.token;
};