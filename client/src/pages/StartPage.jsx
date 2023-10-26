import './StartPage.css';
import ExploreButton from '../components/ExploreButton';

function StartPage() {
    return (
        <div className="start-page-container">
            <div className='inner-div'>
                <h1>
                    Where Capital Meets Its Match!
                </h1>
                <p>
                    Dive into a world of limitless possibilities as you swipe through thousands of innovative startups.
                    Explore a diverse range of industries and make investment decisions that matter – 
                    all backed by a mix of company data and personal insights.
                </p>
                <p>
                    InvesTinder empowers you to discover your perfect investment match effortlessly. 
                    We've revolutionised the way VC firms and startups connect, creating an experience that's as fun as it is rewarding.
                    It's not just about swiping; it's about shaping the future of business.
                </p>
                <ExploreButton/>
            </div>
        </div>
    );
}

export default StartPage;