import { configureStore } from '@reduxjs/toolkit'
import DrawerOpenReducer from '../features/DrawerOpen/DrawerOpenSlice'
import RosConnectionReducer from '../features/RosConnection/RosConnectionSlice'
import LogoAppearReducer from '../features/LogoAppear/LogoAppearSlice'

export const store = configureStore({

  reducer: {
    DrawerOpen:DrawerOpenReducer,
    RosConnection: RosConnectionReducer,
    LogoAppear:LogoAppearReducer,
  },

  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    })
})
