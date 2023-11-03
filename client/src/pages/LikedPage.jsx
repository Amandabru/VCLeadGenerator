import LikedCard from "../components/LikedCardComponent";
import ExploreButton from '../components/ExploreButton';
import { useSelector } from 'react-redux';
import './LikedPage.css';

function SavedPage() {
    const savedCompanies = useSelector((state) => state.savedCompanies);

    return (
        <div>
            {savedCompanies.length > 0 ? (
            <div>
                {savedCompanies.map((company) => (
                    <LikedCard key={company.name} company={company}/>
                ))}
            </div>
            ) : (
            <div style={{display:'flex', flexDirection:'column', alignItems: 'center', marginTop: '12rem'}}>
                <p className="text">
                    You have yet to match with your first startup!
                </p>
                <ExploreButton/>
            </div>    
            )}
        </div>
       
    );
}

export default SavedPage;