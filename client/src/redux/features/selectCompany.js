export const getSavedCompanyByName = (state, companyId) => {
    return state.savedCompanies.find((company) => company.id === companyId);
  };