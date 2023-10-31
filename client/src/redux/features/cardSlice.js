import { createSlice } from '@reduxjs/toolkit';
import { getCompanies } from  '../../api/getCompanies.js';

const initialState = {
    companies: [],
    loading: false,
    error: null,
};

const cardSlice = createSlice({
    name: 'card',
    initialState,
    reducers: {
        startLoading: (state) => {
          state.loading = true;
          state.error = null;
        },
        fetchSuccess: (state, action) => {
          state.companies = action.payload;
          state.loading = false;
          state.error = null;
        },
        fetchFailure: (state, action) => {
          state.loading = false;
          state.error = action.payload;
        },
      },
});


export const { startLoading, fetchSuccess, fetchFailure } = cardSlice.actions;

export const fetchCompanies = (amount) => async (dispatch) => {
  dispatch(startLoading());

  try {
    const data = await getCompanies(amount);
    dispatch(fetchSuccess(data));
  } catch (error) {
    dispatch(fetchFailure(error.message));
  }
};


export default cardSlice.reducer;