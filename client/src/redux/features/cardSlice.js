import { createSlice } from '@reduxjs/toolkit';
import getCompanies from  '../../api/getCompanies';

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


/*
const cardSlice = createSlice({
    name: 'card',
    initialState: {
      companies: [
        {
            name: 'Company 1',
            industry: 'Tech',
            size: 4,
            description: 'Very good',
            business: '',
            founders: [],
            website: '',
        },
        {
            name: 'Company 2',
            industry: 'Finance',
            size: 3,
            description: 'Very nice',
            business: '',
            founders: [],
            website: '',
        },
        {
            name: 'Company 3',
            industry: 'AI', 
            size: 5,
            description: 'Very great',
            business: '',
            founders: [],
            website: '',
        }
      ],
      loading: false,
      error: null,
    },
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
  });*/

export default cardSlice.reducer;