import CardComponent from "../components/CardComponent";
import './ExplorePage.css';
import {RxCross2} from 'react-icons/rx';
import {AiOutlineHeart} from 'react-icons/ai'

function ExplorePage() {
    return (
        <div className="explore-container">
            <CardComponent/>
            <div className="button-container">
                <button className="remove-button">
                    <RxCross2 color="black" size={30}/>
                </button>
                <button className="save-button">
                    <AiOutlineHeart color="#58A894" size={30}/>
                </button>
            </div>
        </div>
    );
}

export default ExplorePage;