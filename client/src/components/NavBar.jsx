import { NavLink } from 'react-router-dom';
import './NavBar.css';

function NavBar() {
 
    return (
       <nav>
          <NavLink to="/" className="title" style={({ isActive }) => ({ color: isActive ? '#58A894' : 'black' })}>SeedScout</NavLink>
        <ul>
            <li>
                <NavLink to="/explore" style={({ isActive }) => ({ color: isActive ? '#58A894' : 'black' })}>Explore</NavLink>
            </li>
            <li>
                <NavLink to="/saved" style={({ isActive }) => ({ color: isActive ? '#58A894' : 'black' })}>Liked</NavLink>
            </li>
            <li>
                <NavLink to="/about" style={({ isActive }) => ({ color: isActive ? '#58A894' : 'black' })}>About</NavLink>
            </li>
        </ul>
       </nav>
    );
}

export default NavBar;