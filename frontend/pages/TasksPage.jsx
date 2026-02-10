import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../src/context/AuthContext';
import { makeAuthenticatedRequest } from '../src/utils/api';
import ProtectedRoute from '../src/components/ProtectedRoute';
import TaskForm from '../src/components/TaskForm';
import TaskList from '../src/components/TaskList';
import Head from 'next/head';

export default function TasksPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  const fetchTasks = async () => {
    try {
      const tasksData = await makeAuthenticatedRequest('/api/tasks', {
        authToken: user.token,
      });
      
      setTasks(tasksData.tasks || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching tasks:', err);
    }
  };

  const handleAddTask = async (taskData) => {
    try {
      const newTask = await makeAuthenticatedRequest('/api/tasks', {
        method: 'POST',
        authToken: user.token,
        body: JSON.stringify(taskData),
      });
      
      setTasks([...tasks, newTask]);
    } catch (err) {
      setError(err.message);
      console.error('Error adding task:', err);
    }
  };

  const handleUpdateTask = async (taskId, updatedTask) => {
    try {
      const updatedTaskData = await makeAuthenticatedRequest(`/api/tasks/${taskId}`, {
        method: 'PUT',
        authToken: user.token,
        body: JSON.stringify(updatedTask),
      });
      
      setTasks(tasks.map(task => 
        task._id === taskId ? updatedTaskData : task
      ));
    } catch (err) {
      setError(err.message);
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await makeAuthenticatedRequest(`/api/tasks/${taskId}`, {
        method: 'DELETE',
        authToken: user.token,
      });
      
      setTasks(tasks.filter(task => task._id !== taskId));
    } catch (err) {
      setError(err.message);
      console.error('Error deleting task:', err);
    }
  };

  return (
    <ProtectedRoute>
      <div className="tasks-page">
        <Head>
          <title>Tasks - Todo App</title>
          <meta name="description" content="Manage your tasks" />
        </Head>
        
        <header className="tasks-header">
          <h1>Your Tasks</h1>
        </header>
        
        <main className="tasks-main">
          {error && <div className="error-message">{error}</div>}
          
          <TaskForm onAddTask={handleAddTask} />
          <TaskList 
            tasks={tasks} 
            onUpdateTask={handleUpdateTask} 
            onDeleteTask={handleDeleteTask} 
            authToken={user.token}
          />
        </main>
      </div>
    </ProtectedRoute>
  );
}