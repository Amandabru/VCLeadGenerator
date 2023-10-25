import { Link } from "react-router-dom";
import './NavBar.css';

function NavBar() {
 
    return (
       <nav>
          <Link to="/" className="title">Name</Link>
        <ul>
            <li>
                <Link to="/explore">Explore</Link>
            </li>
            <li>
                <Link to="/saved">Saved</Link>
            </li>
            <li>
                <Link to="/profile">Profile</Link>
            </li>
        </ul>
       </nav>
    );
}

export default NavBar;