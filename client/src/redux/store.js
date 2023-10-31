import { configureStore } from '@reduxjs/toolkit';
import cardReducer from './features/cardSlice.js';
import savedCompaniesReducer from './features/savedCompaniesSlice.js';

const store = configureStore({
    reducer: {
        card: cardReducer,
        savedCompanies: savedCompaniesReducer,
    },
});

export default store;