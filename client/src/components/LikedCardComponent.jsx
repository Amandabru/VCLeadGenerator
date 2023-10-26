import './LikedCardComponent.css';
import {AiTwotoneHeart} from 'react-icons/ai';


function LikedCard() {
    return (
        <div className='outer-div'>
            <div className='liked-card-container'>
                <div className='header'>
                    <h1 className='company-name'>
                        Company name
                    </h1>
                    <AiTwotoneHeart size={30} color="#58A894"/>
                </div>
                <p>
                    Nr of employees: 4
                </p>
                <p>
                    Founded in 2022
                </p>
                <p>
                    Company LinkedIn
                </p>
            </div>
        </div>
    );
}

export default LikedCard;