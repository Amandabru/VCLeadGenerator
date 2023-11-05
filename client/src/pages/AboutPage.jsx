import './AboutPage.css';
import team from '../assets/team.jpg';
import {BsLinkedin} from 'react-icons/bs';
import Hanna from '../assets/Hanna.jpg';
import Alex from '../assets/Alex.png';
import Amanda from '../assets/amanda.jpg';

function AboutPage() {
    return (
        <div className='outer-container'>
            <h1 className="title">
                Team
            </h1>
            <div className='member-container'>
                <div className='member'>
                    <img src={team}/>
                    <p className='name'>
                        Elias Lundgren
                    </p>
                    <a href="https://www.linkedin.com/in/amanda-brundin/" target='_blank' rel="noreferrer">
                        <BsLinkedin className="icon" color="#235347" size={25}/>
                    </a>
                    <p className='description'>
                        Lorem ipsum ejfnewjk wekjnewkj  
                    </p>
                </div>
                <div className='member'>
                    <img src={Hanna} width="500" height="200"/>
                    <p className='name'>
                        Hanna Almqvist
                    </p>
                    <a href="https://www.linkedin.com/in/hanna-almqvist/" target='_blank' rel="noreferrer">
                        <BsLinkedin className="icon" color="#235347" size={25}/>
                    </a>
                    <p className='description'>
                        User Research, User Experience Design
                    </p>
                </div>
                <div className='member'>
                    <img src={Alex} width="500" height="200"/>
                    <p className='name'>
                        Alexander Olsson
                    </p>
                    <a href="https://www.linkedin.com/in/olsson-alex/" target='_blank' rel="noreferrer">
                        <BsLinkedin className="icon" color="#235347" size={25}/>
                    </a>
                    <p className='description'>
                        Market research, Analyzed interviews
                    </p>
                </div>
                <div className='member'>
                    <img src={team}/>
                    <p className='name'>
                        Sally Isakas
                    </p>
                    <a href="https://www.linkedin.com/in/amanda-brundin/" target='_blank' rel="noreferrer">
                        <BsLinkedin className="icon" color="#235347" size={25}/>
                    </a>
                    <p className='description'>
                        Lorem ipsum ejfnewjk wekjnewkj
                    </p>
                </div>
                <div className='member'>
                    <img src={Amanda} width="500" height="200"/>
                    <p className='name'>
                        Amanda Brundin
                    </p>
                    <a href="https://www.linkedin.com/in/amanda-brundin/" target='_blank' rel="noreferrer">
                        <BsLinkedin className="icon" color="#235347" size={25}/>
                    </a>
                    <p className='description'>
                        Design, Frontend Development
                    </p>
                </div>
            </div>
        </div>
    );
}

export default AboutPage;