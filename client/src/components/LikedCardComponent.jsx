import './LikedCardComponent.css';
import {AiTwotoneHeart} from 'react-icons/ai';
import { useDispatch } from 'react-redux';
import { unsaveCompany } from '../redux/features/savedCompaniesSlice.js';

function LikedCard({company}) {
    const dispatch = useDispatch();

    const handleUnsaveClick = () => {
        dispatch(unsaveCompany(company));
    };

    return (
        <div className='outer-div'>
            <div className='liked-card-container'>
                <div className='header'>
                    <h1 className='company-name'>
                        {company.name}
                    </h1>
                    <AiTwotoneHeart size={30} color="#58A894" onClick={handleUnsaveClick}/>
                </div>
                <p>
                    Nr of employees: {company.size}
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