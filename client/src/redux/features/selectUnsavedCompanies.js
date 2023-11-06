import { createSelector } from 'reselect';

const selectAllCompanies = (state) => state.card.companies;
const selectSavedCompanies = (state) => state.savedCompanies;

const selectUnsavedCompanies = createSelector(
  [selectAllCompanies, selectSavedCompanies],
  (allCompanies, savedCompanies) => {
    return allCompanies.filter((company) => !savedCompanies.some((savedCompany) => savedCompany.id === company.id));
  }
);

export default selectUnsavedCompanies;