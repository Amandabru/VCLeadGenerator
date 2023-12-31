import { createSlice } from '@reduxjs/toolkit';

const savedCompaniesSlice = createSlice({
  name: 'savedCompanies',
  initialState: [],
  reducers: {
    saveCompany: (state, action) => {
      state.push(action.payload);
    },
    unsaveCompany: (state, action) => {
        return state.filter((company) => company.id !== action.payload.id);
    },
  },
});

export const { saveCompany, unsaveCompany } = savedCompaniesSlice.actions;

export default savedCompaniesSlice.reducer;
