import './ExploreButton.css';
import { useNavigate } from 'react-router-dom';

function ExploreButton() {
    const navigateTo = useNavigate();

    const handleExploreClick = () => {
        navigateTo('/explore');
    };

    return (
        <div>
            <button onClick={handleExploreClick} className='button-style'>
                Start Exploring!
            </button>
        </div>
    );
}

export default ExploreButton;