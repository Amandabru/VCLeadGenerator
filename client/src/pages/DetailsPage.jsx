import CardComponent from "../components/CardComponent";
import { useParams } from 'react-router-dom';
import { getSavedCompanyByName } from '../redux/features/selectCompany.js';
import { useSelector } from 'react-redux';
import {RxCross2} from 'react-icons/rx';
import './DetailsPage.css';
import { useNavigate } from 'react-router-dom';

function DetailsPage() {
    const { companyName } = useParams();
    const savedCompany = useSelector((state) => getSavedCompanyByName(state, companyName));
    const navigateTo = useNavigate();

    const redirect = () => {
        navigateTo('/saved');
    };

    if (!savedCompany) {
        return <div className="text">Company not found</div>;
    }

    return (
        <div className="outer-container">
            <RxCross2 color="black" size={30} className="cross" onClick={redirect}/>
            <CardComponent company={savedCompany}/>
        </div>
    );
}

export default DetailsPage;