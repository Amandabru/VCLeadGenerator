// import { useState } from 'react'
import './App.css';
import { Route, Routes } from 'react-router-dom';
import NavBar from './components/NavBar';
import StartPage from './pages/StartPage';
import AboutPage from './pages/AboutPage';
import LikedPage from './pages/LikedPage';
import ExplorePage from './pages/ExplorePage';
import DetailsPage from './pages/DetailsPage';

function App() {

  return (
    <>
      <NavBar/>
      <div>
      <Routes>
        <Route path="/" element={<StartPage/>} />
        <Route path="/about" element={<AboutPage/>} />
        <Route path="/saved" element={<LikedPage/>} />
        <Route path="/explore" element={<ExplorePage/>} />
        <Route path="/details/:companyId" element={<DetailsPage/>} />
      </Routes>
      </div>
    </>
  )
}

export default App
