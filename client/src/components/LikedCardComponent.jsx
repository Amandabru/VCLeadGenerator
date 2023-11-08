import './LikedCardComponent.css';
import { AiTwotoneHeart } from 'react-icons/ai';
import { useDispatch } from 'react-redux';
import { unsaveCompany } from '../redux/features/savedCompaniesSlice.js';
import { useNavigate } from 'react-router-dom';

function LikedCard({ company }) {
    const dispatch = useDispatch();
    const navigateTo = useNavigate();

    const handleUnsaveClick = (event) => {
        event.stopPropagation();
        dispatch(unsaveCompany(company));
    };

    const showLikedCard = () => {
        navigateTo(`/details/${company.id}`);
    };

    return (
        <div className='outer-div' onClick={showLikedCard}>
            <div className='liked-card-container'>
                <div className='header'>
                    <h1 className='company-name'>
                        {company.name}
                    </h1>
                    <AiTwotoneHeart className="heart" size={30} color="#58A894" onClick={handleUnsaveClick} />
                </div>
                <p>
                    Nr of employees: {company.size}
                </p>
                <p>
                    Founded in {company.founded}
                </p>
                <div style={{display: 'flex', flexDirection: 'row', gap: '1rem', marginTop: '-1rem' }}>
                    <p>
                        <a className='website' href={company.website} rel="noreferrer" target='_blank' style={{ color: 'white', textDecoration: 'none', transition: 'color 0.2s' }}>
                            Website
                        </a>
                    </p>
                    <p>
                        <a className='website' href={"https://www.linkedin.com/company/" + company.id} rel="noreferrer" target='_blank' style={{ color: 'white', textDecoration: 'none', transition: 'color 0.2s' }}>
                            LinkedIn
                        </a>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default LikedCard;