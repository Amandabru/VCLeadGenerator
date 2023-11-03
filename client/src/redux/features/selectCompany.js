export const getSavedCompanyByName = (state, companyName) => {
    return state.savedCompanies.find((company) => company.name === companyName);
  };