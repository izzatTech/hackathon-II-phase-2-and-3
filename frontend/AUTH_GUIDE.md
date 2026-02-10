# Authentication System Guide

This document explains how to use the authentication system in the Todo application.

## Components and Hooks

### AuthProvider
- Located in `src/context/AuthContext.jsx`
- Wraps the entire application in `_app.js`
- Provides authentication state and functions to all child components

### useAuth Hook
- Used to access authentication state and functions
- **Important**: Only use this hook within components that are descendants of `AuthProvider`
- Throws an error if used outside of `AuthProvider`

### useSafeAuth Hook
- A safer alternative to `useAuth`
- Doesn't throw an error if used outside of `AuthProvider`
- Returns a default state instead

### ProtectedRoute Component
- Wrapper component to protect routes that require authentication
- Redirects unauthenticated users to a specified route (default: '/login')

## Proper Usage

### In Pages
```jsx
import { useAuth } from '../context/AuthContext';

function MyPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) return <div>Loading...</div>;
  if (!isAuthenticated) return <div>Please log in</div>;
  
  return <div>Welcome, {user?.email}!</div>;
}
```

### Protecting Routes
```jsx
import ProtectedRoute from '../components/ProtectedRoute';

function Dashboard() {
  return (
    <ProtectedRoute>
      <div>Dashboard content</div>
    </ProtectedRoute>
  );
}
```

## Troubleshooting

### "useAuth must be used within an AuthProvider" Error
This error occurs when:
1. The component using `useAuth` is not a descendant of `AuthProvider`
2. The `AuthProvider` is not properly set up in `_app.js`

Make sure your `_app.js` looks like this:
```jsx
import { AuthProvider } from './src/context/AuthContext';

function MyApp({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}
```

### Server-Side Rendering Issues
The authentication system is designed to handle SSR properly by initializing state appropriately and checking for the `window` object before accessing localStorage.