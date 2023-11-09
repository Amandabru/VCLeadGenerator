import './AboutPage.css';
import { BsLinkedin } from 'react-icons/bs';
import { FaGithubSquare } from 'react-icons/fa'
import Hanna from '../assets/Hanna.jpg';
import Alex from '../assets/Alex.png';
import Amanda from '../assets/amanda.jpg';
import Elias from '../assets/Elias.png';
import Sally from '../assets/Sally.jpg';

function AboutPage() {
    return (
        <div className='outer-container'>
             <h1 className="title">
                About
            </h1>
            <div className='about'>
                <p>
                    Welcome to SeedScout, where innovation meets efficiency in the world of venture capital. 
                    Our mission is to revolutionize how VC firms discover and evaluate promising start-ups in the early stages, 
                    focusing on Pre-Seed to Series A companies.
                </p>
                <p>
                    Sweden's startup game is strong, covering fintech, healthcare, gaming, and more. 
                    VC firms hustle through events and connections, but the startup world is changing. 
                    Enter SeedScout, your solution for spotting golden opportunities if you don't have an in-house system.
                </p>
                <p>
                    Deal sourcing is the core of VC life. Everyone's got their methods—some rely on inbound offers, 
                    others on recommendations and data scraping from platforms. We're here to blend it all, 
                    delivering a curated list of startups that fit your criteria.
                </p>
                <p>
                    Numbers are crucial, but there's more to it. We call it "soft values"—the secret sauce behind a startup's success. 
                    SeedScout shines a light on the founder's vibe, leadership style, and industry-changing potential. 
                    We saw a gap in the market, and we're here to fill it. Think of us as your shortcut to making investment decisions that just feel right.
                </p>
                <p>
                    In a world sticking to the usual playbook, SeedScout is your laid-back sidekick. 
                    An easy-to-use tool that fits into your workflow without needing a big tech overhaul. 
                    Our algorithm, with a dash of scraping and ChatGPT magic, gives you the lowdown on startups in a way that feels familiar.
                </p>
                <a src="https://github.com/Amandabru/VCLeadGenerator.git" target='_blank'>
                    <FaGithubSquare className="icon" size={30} color="#235347" style={{cursor: 'pointer'}}/>
                </a>
            </div>
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
                        Market Research, Interview Insights, Process Tracking
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
                        Market Research, Business Development, Support on Back-end
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