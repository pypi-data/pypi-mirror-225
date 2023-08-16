import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { SideDashboardLayer, SideDashboardState } from '../types';

export const initialSideDashboardState: SideDashboardState = {
  navigationState: [{ pageName: 'Notebook' }],
  timeWindow: 'null'
};

export const sideDashboardSlice = createSlice({
  name: 'sidedashboard',
  initialState: initialSideDashboardState,
  reducers: {
    // safe to mutate state inside since createSlice is using Immer internally to translate this to immutable changes

    // time window action
    setTimeWindow: (state, action: PayloadAction<string>) => {
      state.timeWindow = action.payload;
    },

    // navigation actions
    navigateDeeper: (state, action: PayloadAction<SideDashboardLayer>) => {
      state.navigationState.push(action.payload);
    },
    navigateBack: state => {
      state.navigationState.pop();
    },
    navigateToNotebook: (state, action: PayloadAction<void>) => {
      state.navigationState = [
        {
          pageName: 'Notebook'
        }
      ];
    },
    navigateToCell: (
      state,
      action: PayloadAction<{
        cellId: string;
      }>
    ) => {
      state.navigationState = [
        {
          pageName: 'Notebook'
        },
        {
          pageName: 'Cell',
          content: {
            cellId: action.payload.cellId
          }
        }
      ];
    },
    navigateToHistory: (state, action: PayloadAction<number>) => {
      state.navigationState = state.navigationState.slice(
        0,
        action.payload + 1
      );
    }
  }
});

export const {
  setTimeWindow,
  navigateDeeper,
  navigateBack,
  navigateToNotebook,
  navigateToCell,
  navigateToHistory
} = sideDashboardSlice.actions;

export default sideDashboardSlice.reducer;
