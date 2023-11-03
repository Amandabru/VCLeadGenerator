import { Link } from "react-router-dom";
import './NavBar.css';
import {IoSettingsOutline} from 'react-icons/io5';

function NavBar() {
 
    return (
       <nav>
          <Link to="/" className="title">SeedScout</Link>
        <ul>
            <li>
                <Link to="/explore" className="test">Explore</Link>
            </li>
            <li>
                <Link to="/saved">Liked</Link>
            </li>
            <li className="settings">
                <Link to="/profile">
                    <IoSettingsOutline size={22}/>
                </Link>
            </li>
        </ul>
       </nav>
    );
}

export default NavBar;