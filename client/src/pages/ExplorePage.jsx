import CardComponent from "../components/CardComponent";
import './ExplorePage.css';
import {RxCross2} from 'react-icons/rx';
import {AiOutlineHeart} from 'react-icons/ai';
import { useSelector } from 'react-redux';
import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { saveCompany } from '../redux/features/savedCompaniesSlice.js';
import BeatLoader from "react-spinners/BeatLoader";
import selectUnsavedCompanies from '../redux/features/selectUnsavedCompanies';


function ExplorePage() {
    const dispatch = useDispatch();
    // const companies = useSelector((state) => state.card.companies);
    const unsavedCompanies = useSelector(selectUnsavedCompanies);
    const loading = useSelector((state) => state.card.loading);

    const [currentCompanyIndex, setCurrentCompanyIndex] = useState(0);

    const showNextCompany = () => {
        setCurrentCompanyIndex((prevIndex) =>
        prevIndex === unsavedCompanies.length - 1 ? 0 : prevIndex + 1
      );
      swipeToLeft();
    };

    let currentCompany;
    if(unsavedCompanies.length > 0) {
        currentCompany = unsavedCompanies[currentCompanyIndex];
    }
    else {
        currentCompany = null;
    }

    const handleSaveClick = () => {
        if (currentCompany) {
            dispatch(saveCompany(currentCompany));
        }
        if(unsavedCompanies.length == 2){
            setCurrentCompanyIndex(0);
        }
        swipeToRight();
    };

    const swipeToLeft = () =>{
        const cardElement = document.querySelector('.card');
        cardElement.style.transition = 'transform 0.3s ease-in-out, opacity 0.3s ease-in-out';
        cardElement.style.transform = 'translateX(-100%)';
        cardElement.style.opacity = 0;

        setTimeout(() => {
            cardElement.style.transition = '';
            cardElement.style.transform = '';
            cardElement.style.opacity = '';
        }, 400);
    };

    const swipeToRight = () =>{
        const cardElement = document.querySelector('.card');
        cardElement.style.transition = 'transform 0.3s ease-in-out, opacity 0.3s ease-in-out';
        cardElement.style.transform = 'translateX(100%)';
        cardElement.style.opacity = 0;

        setTimeout(() => {
            cardElement.style.transition = '';
            cardElement.style.transform = '';
            cardElement.style.opacity = '';
        }, 400);
    };


    const containerStyle = {
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
    };


    if (loading) {
        return <div style={containerStyle}>
        <BeatLoader
            color={'#58A894'}
            loading={true}
            size={15}
            aria-label="Loading Spinner"
            data-testid="loader"
        />
        </div>;
    }

    if (!currentCompany) {
        return (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '12rem' }}>
            <p className="text">
              There are no more startups that you haven't already liked.
            </p>
          </div>
        );
      }

    return (
        <div className="explore-container">
            <CardComponent company={currentCompany} isLiked={false}/>
            <div className="button-container">
                <button className="remove-button" onClick={showNextCompany}>
                    <RxCross2 color="black" size={30}/>
                </button>
                <button className="save-button" onClick={handleSaveClick}>
                    <AiOutlineHeart color="#58A894" size={30}/>
                </button>
            </div>
        </div>
    );
}

export default ExplorePage;