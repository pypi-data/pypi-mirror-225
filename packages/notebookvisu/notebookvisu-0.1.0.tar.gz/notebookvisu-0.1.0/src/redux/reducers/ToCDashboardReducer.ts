import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { LocationData, ToCState } from '../types';

export const initialToCDashboardState: ToCState = {
  refreshBoolean: false,
  displayDashboard: true,
  hasNotebookId: false,
  locationData: null
};

export const tocDashboardSlice = createSlice({
  name: 'tocdashboard',
  initialState: initialToCDashboardState,
  reducers: {
    refreshToC: state => {
      // safe to mutate state inside since createSlice is using Immer internally to translate this to immutable changes
      state.refreshBoolean = !state.refreshBoolean;
    },
    setDisplayHideDashboard: (state, action: PayloadAction<boolean>) => {
      state.displayDashboard = action.payload;
    },
    setHasNotebookId: (state, action: PayloadAction<boolean>) => {
      state.hasNotebookId = action.payload;
    },
    setFetchedLocationData: (state, action: PayloadAction<LocationData>) => {
      state.locationData = action.payload;
    }
  }
});

export const {
  refreshToC,
  setDisplayHideDashboard,
  setHasNotebookId,
  setFetchedLocationData
} = tocDashboardSlice.actions;

export default tocDashboardSlice.reducer;
