import { createSelector } from 'reselect';
import store from '../store';

const selectAllCompanies = (state) => state.card.companies;
const selectSavedCompanies = (state) => state.savedCompanies;

const selectUnsavedCompanies = createSelector(
  [selectAllCompanies, selectSavedCompanies],
  (allCompanies, savedCompanies) => {
    return allCompanies.filter((company) => !savedCompanies.some((savedCompany) => savedCompany.name === company.name));
  }
);

export default selectUnsavedCompanies;