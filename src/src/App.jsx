import { useState } from 'react'
import DashboardPage from './DashboardPage'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <DashboardPage></DashboardPage>
    </>
  )
}

export default App
