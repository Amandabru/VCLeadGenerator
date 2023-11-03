import './AboutPage.css';
import team from '../assets/team.jpg';
import {BsLinkedin} from 'react-icons/bs';

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
                    <BsLinkedin color="#235347" size={25}/>
                    <p className='description'>
                        Lorem ipsum ejfnewjk wekjnewkj ndkjewnk wekjnewk wkednwjk ejf 
                        efwe wcw ecwec wccw wecewfw wewec wcw wcwecw wewfewc 
                    </p>
                </div>
                <div className='member'>
                    <img src={team}/>
                    <p className='name'>
                        Hanna Almqvist
                    </p>
                    <BsLinkedin color="#235347" size={25}/>
                    <p className='description'>
                    Lorem ipsum ejfnewjk wekjnewkj ndkjewnk wekjnewk wkednwjk ejf 
                        efwe wcw ecwec wccw wecewfw wewec wcw wcwecw wewfewc 
                    </p>
                </div>
                <div className='member'>
                    <img src={team}/>
                    <p className='name'>
                        Alexander Olsson
                    </p>
                    <BsLinkedin color="#235347" size={25}/>
                    <p className='description'>
                        Lorem ipsum ejfnewjk wekjnewkj ndkjewnk wekjnewk wkednwjk ejf 
                        efwe wcw ecwec wccw wecewfw wewec wcw wcwecw wewfewc 
                    </p>
                </div>
                <div className='member'>
                    <img src={team}/>
                    <p className='name'>
                        Sally Isakas
                    </p>
                    <BsLinkedin color="#235347" size={25}/>
                    <p className='description'>
                        Lorem ipsum ejfnewjk wekjnewkj ndkjewnk wekjnewk wkednwjk ejf 
                        efwe wcw ecwec wccw wecewfw wewec wcw wcwecw wewfewc 
                    </p>
                </div>
                <div className='member'>
                    <img src={team}/>
                    <p className='name'>
                        Amanda Brundin
                    </p>
                    <BsLinkedin color="#235347" size={25}/>
                    <p className='description'>
                        Lorem ipsum ejfnewjk wekjnewkj ndkjewnk wekjnewk wkednwjk ejf 
                        efwe wcw ecwec wccw wecewfw wewec wcw wcwecw wewfewc 
                    </p>
                </div>
            </div>
        </div>
    );
}

export default AboutPage;