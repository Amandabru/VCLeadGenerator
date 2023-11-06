import './AboutPage.css';
import team from '../assets/team.jpg';
import {BsLinkedin} from 'react-icons/bs';
import Hanna from '../assets/Hanna.jpg';
import Alex from '../assets/Alex.png';
import Amanda from '../assets/amanda.jpg';
import Elias from '../assets/Elias.png';
import Sally from '../assets/Sally.jpg';

function AboutPage() {
    return (
        <div className='outer-container'>
            <h1 className="title">
                Team
            </h1>
            <div className='member-container'>
                <div className='member'>
                    <img src={Elias} />
                    <p className='name'>
                        Elias Lundgren
                    </p>
                    <a href="https://www.linkedin.com/in/elias-lundgren/" target='_blank' rel="noreferrer">
                        <BsLinkedin className="icon" color="#235347" size={25}/>
                    </a>
                    <p className='description'>
                        Data Gathering and Processing, Back-end 
                    </p>
                </div>
                <div className='member'>
                    <img src={Hanna} />
                    <p className='name'>
                        Hanna Almqvist
                    </p>
                    <a href="https://www.linkedin.com/in/hanna-almqvist/" target='_blank' rel="noreferrer">
                        <BsLinkedin className="icon" color="#235347" size={25}/>
                    </a>
                    <p className='description'>
                        User Research, User Experience Design, User Testing
                    </p>
                </div>
                <div className='member'>
                    <img src={Alex} />
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
                    <img src={Sally} />
                    <p className='name'>
                        Sally Isakas
                    </p>
                    <a href="https://www.linkedin.com/in/sally-isakas/" target='_blank' rel="noreferrer">
                        <BsLinkedin className="icon" color="#235347" size={25}/>
                    </a>
                    <p className='description'>
                        Market research, Business Development, Support on Back-end
                    </p>
                </div>
                <div className='member'>
                    <img src={Amanda}/>
                    <p className='name'>
                        Amanda Brundin
                    </p>
                    <a href="https://www.linkedin.com/in/amanda-brundin/" target='_blank' rel="noreferrer">
                        <BsLinkedin className="icon" color="#235347" size={25}/>
                    </a>
                    <p className='description'>
                        User Experience Design, User Testing, Front-end Development
                    </p>
                </div>
            </div>
        </div>
    );
}

export default AboutPage;