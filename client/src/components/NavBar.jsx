import { Link } from "react-router-dom";
import './NavBar.css';

function NavBar() {
 
    return (
       <nav>
          <Link to="/" className="title">InvesTinder</Link>
        <ul>
            <li>
                <Link to="/explore" className="test">Explore</Link>
            </li>
            <li>
                <Link to="/saved">Liked</Link>
            </li>
            <li>
                <Link to="/profile">Profile</Link>
            </li>
        </ul>
       </nav>
    );
}

export default NavBar;