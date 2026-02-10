import { useState } from 'react';

const TaskList = ({ tasks, onUpdateTask, onDeleteTask, authToken }) => {
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editForm, setEditForm] = useState({});

  const startEditing = (task) => {
    setEditingTaskId(task._id);
    setEditForm({
      title: task.title,
      description: task.description || '',
      dueDate: task.dueDate ? new Date(task.dueDate).toISOString().split('T')[0] : '',
      priority: task.priority || 'medium',
      completed: task.completed
    });
  };

  const cancelEditing = () => {
    setEditingTaskId(null);
    setEditForm({});
  };

  const handleEditSubmit = async (taskId) => {
    try {
      await onUpdateTask(taskId, editForm);
      setEditingTaskId(null);
      setEditForm({});
    } catch (error) {
      console.error('Error updating task:', error);
      alert('Failed to update task');
    }
  };

  const handleToggleComplete = async (task) => {
    try {
      await onUpdateTask(task._id, {
        ...task,
        completed: !task.completed
      });
    } catch (error) {
      console.error('Error toggling task completion:', error);
      alert('Failed to update task');
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const getPriorityClass = (priority) => {
    switch (priority) {
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      case 'low': return 'priority-low';
      default: return '';
    }
  };

  return (
    <div className="task-list-container">
      <h2>Your Tasks ({tasks.length})</h2>
      
      {tasks.length === 0 ? (
        <div className="empty-tasks">
          <p>No tasks yet. Add a new task to get started!</p>
        </div>
      ) : (
        <div className="task-list">
          {tasks.map((task) => (
            <div key={task._id} className={`task-item ${task.completed ? 'completed' : ''}`}>
              {editingTaskId === task._id ? (
                // Edit form
                <div className="task-edit-form">
                  <div className="form-group">
                    <input
                      type="text"
                      value={editForm.title}
                      onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                      className="edit-title-input"
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <textarea
                      value={editForm.description}
                      onChange={(e) => setEditForm({...editForm, description: e.target.value})}
                      className="edit-description-input"
                      rows="2"
                    />
                  </div>
                  
                  <div className="form-row">
                    <div className="form-group">
                      <input
                        type="date"
                        value={editForm.dueDate}
                        onChange={(e) => setEditForm({...editForm, dueDate: e.target.value})}
                      />
                    </div>
                    
                    <div className="form-group">
                      <select
                        value={editForm.priority}
                        onChange={(e) => setEditForm({...editForm, priority: e.target.value})}
                      >
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                      </select>
                    </div>
                  </div>
                  
                  <div className="form-actions">
                    <button 
                      onClick={() => handleEditSubmit(task._id)}
                      className="btn-save"
                    >
                      Save
                    </button>
                    <button 
                      onClick={cancelEditing}
                      className="btn-cancel"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                // Display task
                <div className="task-content">
                  <div className="task-header">
                    <div className="task-checkbox">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => handleToggleComplete(task)}
                        id={`complete-${task._id}`}
                      />
                      <label htmlFor={`complete-${task._id}`} className="checkbox-label">
                        <span className={`task-title ${task.completed ? 'completed' : ''}`}>
                          {task.title}
                        </span>
                      </label>
                    </div>
                    
                    <div className="task-actions">
                      <button 
                        onClick={() => startEditing(task)}
                        className="btn-edit"
                      >
                        Edit
                      </button>
                      <button 
                        onClick={() => onDeleteTask(task._id)}
                        className="btn-delete"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                  
                  {task.description && (
                    <div className="task-description">
                      {task.description}
                    </div>
                  )}
                  
                  <div className="task-meta">
                    {task.dueDate && (
                      <span className="task-due-date">
                        Due: {formatDate(task.dueDate)}
                      </span>
                    )}
                    
                    <span className={`task-priority ${getPriorityClass(task.priority)}`}>
                      {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                    </span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;