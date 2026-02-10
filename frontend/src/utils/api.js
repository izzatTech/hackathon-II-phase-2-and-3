// Utility function to make authenticated API requests
// This function expects the token to be passed in as it's a utility function
export const makeAuthenticatedRequest = async (url, options = {}) => {
  const { authToken, backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3001', ...fetchOptions } = options;
  
  // Construct the full URL if it's a relative path
  const fullUrl = url.startsWith('http') ? url : `${backendUrl}${url}`;
  
  const response = await fetch(fullUrl, {
    ...fetchOptions,
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json',
      ...fetchOptions.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};