import React, { useEffect, useMemo, useState } from 'react'

const columns = [
  { id: 'todo', title: 'Todo' },
  { id: 'inprogress', title: 'In Progress' },
  { id: 'done', title: 'Done' },
]

export default function App() {
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [editingId, setEditingId] = useState(null)

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('kanban_tasks')
    if (saved) {
      try {
        setTasks(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to parse saved tasks', e)
      }
    }
  }, [])

  // Persist to localStorage when tasks change
  useEffect(() => {
    localStorage.setItem('kanban_tasks', JSON.stringify(tasks))
  }, [tasks])

  const isEditing = editingId !== null

  const addTask = (e) => {
    e.preventDefault()
    const trimmed = title.trim()
    if (!trimmed) return
    if (editingId !== null) {
      // Update existing task
      setTasks(prev => prev.map(t => t.id === editingId ? { ...t, title: trimmed } : t))
      setEditingId(null)
      setTitle('')
      return
    }
    const newTask = { id: Date.now(), title: trimmed, status: 'todo' }
    setTasks(prev => [newTask, ...prev])
    setTitle('')
  }

  const moveTask = (id, newStatus) => {
    setTasks(prev => prev.map(t => t.id === id ? { ...t, status: newStatus } : t))
  }

  const deleteTask = (id) => {
    setTasks(prev => prev.filter(t => t.id !== id))
  }

  const onDragStart = (e, id) => {
    e.dataTransfer.setData('text/plain', String(id))
    e.dataTransfer.effectAllowed = 'move'
  }

  const onDropColumn = (status, e) => {
    const id = Number(e.dataTransfer.getData('text/plain'))
    if (!Number.isFinite(id)) return
    moveTask(id, status)
    e.preventDefault()
  }

  const onDragOver = (e) => {
    e.preventDefault()
  }

  const filtered = (status) => tasks.filter(t => t.status === status)

  return (
    <div className="max-w-6xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4 text-center">Kanban Todo</h1>
      <form onSubmit={addTask} className="mb-4 flex gap-2 justify-center">
        <input
          value={title}
          onChange={(e)=>setTitle(e.target.value)}
          placeholder="New or edited todo title"
          className="border rounded px-3 py-2 w-80"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          {isEditing ? 'Update Todo' : 'Add Todo'}
        </button>
        {isEditing && (
          <button type="button" onClick={()=>{ setEditingId(null); setTitle(''); }} className="ml-2 bg-gray-200 px-3 py-2 rounded" title="Cancel editing">Cancel</button>
        )}
      </form>

      <div className="flex gap-4 h-96">
        {columns.map(col => (
          <div key={col.id} onDrop={(e)=>onDropColumn(col.id, e)} onDragOver={onDragOver} className="flex-1 bg-white rounded shadow p-2">
            <h2 className="text-lg font-semibold mb-2 text-center">{col.title}</h2>
            <div className="h-full min-h-64">
              {filtered(col.id).length === 0 && (
                <div className="text-sm text-gray-500 text-center mt-6">No tasks</div>
              )}
              {filtered(col.id).map(task => (
                <div key={task.id}
                     draggable
                     onDragStart={(e)=>onDragStart(e, task.id)}
                     className="bg-gray-100 rounded p-2 mb-2 shadow cursor-move"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{task.title}</span>
                    <div className="flex gap-1">
                      {task.status !== 'todo' && (
                        <button onClick={()=>moveTask(task.id, 'todo')} className="text-xs px-2 py-1 bg-blue-200 rounded">To Todo</button>
                      )}
                      {task.status !== 'inprogress' && (
                        <button onClick={()=>moveTask(task.id, 'inprogress')} className="text-xs px-2 py-1 bg-yellow-200 rounded">In Progress</button>
                      )}
                      {task.status !== 'done' && (
                        <button onClick={()=>moveTask(task.id, 'done')} className="text-xs px-2 py-1 bg-green-200 rounded">Done</button>
                      )}
                      <button onClick={()=>{ setEditingId(task.id); setTitle(task.title); }} className="text-xs px-2 py-1 bg-blue-200 rounded" title="Edit task">Edit</button>
                      <button
                        onClick={(e)=>{ e.stopPropagation(); deleteTask(task.id); }}
                        className="text-xs px-2 py-1 bg-red-200 rounded ml-1"
                        title="Delete task"
                      >Delete</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
