import { useState, useEffect } from 'react'
import axios from "axios"
import './App.css'

const APP_URL = "https://flask-to-do-backend.onrender.com"

function App() {

  const [todos, setTodos] = useState([])
  const [task, setTask] = useState("")

  useEffect(() => {
    axios.get(`${APP_URL}/todos`)
      .then((res) => setTodos(res.data))
      .catch((err) => console.error("Error fetching todos:", err))
  }, [])

  const deleteTask = (id) => {
    axios.delete(`${APP_URL}/todos/${id}`)
      .then(() => {
        setTodos(todos.filter(todo => todo.id !== id))
      })
      .catch((err) => console.error("Error deleting todo:", err))
  }

  const toggleDone = (id) => {
    const todo = todos.find(t => t.id === id)
    axios.put(`${APP_URL}/todos/${id}`, { done: !todo.done })
      .then(() => {
        setTodos(todos.map(t =>
          t.id === id ? { ...t, done: !t.done } : t
        ))
      })
      .catch((err) => console.error("Error updating todo:", err))
  }

  const addTask = () => {
    if (task.trim() === "") return
    axios.post(`${APP_URL}/todos`, { task })
      .then((res) => {
        setTodos([...todos, { id: res.data.id || Date.now(), task, done: false }])
        setTask("")
      })
      .catch((err) => console.error("Error adding todo:", err))
  }

  return (
    <>
      <h1>Todos</h1>
      <div>
        <input
          type='text'
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder='Enter the task'
        />
        <button onClick={addTask}>Add Task</button>
      </div>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <span
              style={{
                textDecoration: todo.done ? "line-through" : "none",
                cursor: "pointer"
              }}
              onClick={() => toggleDone(todo.id)}
            >
              {todo.task}
            </span>
            <button onClick={() => deleteTask(todo.id)}>❌</button>
          </li>
        ))}
      </ul>
    </>
  )
}

export default App
