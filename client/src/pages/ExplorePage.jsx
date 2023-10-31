import CardComponent from "../components/CardComponent";
import './ExplorePage.css';
import {RxCross2} from 'react-icons/rx';
import {AiOutlineHeart} from 'react-icons/ai';
import { useSelector } from 'react-redux';
import { useState } from 'react';

function ExplorePage() {
    const companies = useSelector((state) => state.card.companies);

    const [currentCompanyIndex, setCurrentCompanyIndex] = useState(0);

    const showNextCompany = () => {
      setCurrentCompanyIndex((prevIndex) =>
        prevIndex === companies.length - 1 ? 0 : prevIndex + 1
      );
    };
  
    const currentCompany = companies[currentCompanyIndex];

    return (
        <div className="explore-container">
            <CardComponent company={currentCompany}/>
            <div className="button-container">
                <button className="remove-button" onClick={showNextCompany}>
                    <RxCross2 color="black" size={30}/>
                </button>
                <button className="save-button" onClick={showNextCompany}>
                    <AiOutlineHeart color="#58A894" size={30}/>
                </button>
            </div>
        </div>
    );
}

export default ExplorePage;