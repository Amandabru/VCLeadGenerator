// import { useState } from 'react'
import './App.css';
import { Route, Routes } from 'react-router-dom';
import NavBar from './components/NavBar';
import StartPage from './pages/StartPage';
import ProfilePage from './pages/ProfilePage';
import SavedPage from './pages/SavedPage';
import ExplorePage from './pages/ExplorePage';

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
      <NavBar/>
      <div>
      <Routes>
        <Route path="/" element={<StartPage/>} />
        <Route path="/profile" element={<ProfilePage/>} />
        <Route path="/saved" element={<SavedPage/>} />
        <Route path="/explore" element={<ExplorePage/>} />
      </Routes>
      </div>
    </>
  )
}

export default App
