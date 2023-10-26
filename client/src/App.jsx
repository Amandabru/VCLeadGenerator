// import { useState } from 'react'
import './App.css';
import { Route, Routes } from 'react-router-dom';
import NavBar from './components/NavBar';
import StartPage from './pages/StartPage';
import ProfilePage from './pages/ProfilePage';
import LikedPage from './pages/LikedPage';
import ExplorePage from './pages/ExplorePage';

function App() {

  return (
    <>
      <NavBar/>
      <div>
      <Routes>
        <Route path="/" element={<StartPage/>} />
        <Route path="/profile" element={<ProfilePage/>} />
        <Route path="/saved" element={<LikedPage/>} />
        <Route path="/explore" element={<ExplorePage/>} />
      </Routes>
      </div>
    </>
  )
}

export default App
