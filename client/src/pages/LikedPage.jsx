import LikedCard from "../components/LikedCardComponent";
import { useSelector } from 'react-redux';

function SavedPage() {
    const savedCompanies = useSelector((state) => state.savedCompanies);

    return (
        <div>
            {savedCompanies.map((company) => (
                <LikedCard key={company.name} company={company} />
            ))}
        </div>
    );
}

export default SavedPage;