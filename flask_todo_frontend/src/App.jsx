import { useState,useEffect } from 'react'
import axios from "axios"
import './App.css'

const APP_URL = "http://127.0.0.1:5000/todos" 

function App() {

  const [todos,setTodos] = useState([])
  const [task,setTask] = useState("");

  useEffect(() => {
    axios.get(APP_URL).then((res) => setTodos(res.data));
  }, []);

  const deleteTask=(id)=>{
    console.log(id)
    axios.delete(`${APP_URL}/${id}`).then(()=>{
      setTodos(todos.filter(todo=>todo.id !==id ))
    })
  }
  const toggleDone=(id)=>{
    console.log(id)
    axios.put(`${APP_URL}/${id}`).then(()=>{
      setTodos(todos.map((todo)=>{todo.id=id?{...todo,done:!todo.done}:todo}) )
    })
  }
  const addTask= ()=>{
    axios.post(APP_URL,{task}).then(()=>{
      setTodos([...todos,{task,done:false}])
      console.log(todos);
      setTask("")
    })
  }  
  return (
    <>
    <h1>Todos</h1>
    <div>
      <input
      type='text'
      value={task} 
      onChange={(e)=>setTask(e.target.value)}
      placeholder='enter the task'
      ></input>
      <button onClick={addTask}>Add Task</button>
  </div>
    <ul>
      {todos.map((todo)=>(
        <li key={todo.id}>
          <span
          style={{textDecoration:todo.done?"line-through":"none",cursor:"pointer"}}
          onClick={()=>toggleDone(todo.id)}>
            {todo.task}
          </span>
          <button
          onClick={()=>deleteTask(todo.id)}>
            ❌
          </button>
        </li>
      ))}
    </ul>
  <div>
    </div>
    </>
  )
}

export default App
