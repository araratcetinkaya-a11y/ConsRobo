import React from 'react'
import {Paper} from '@mui/material'
import { useState } from 'react'

const CustomInput = () => {

    const[searchTerm,setsearchTerm] = useState('')

    const handleSubmit = ()=>{
        console.log("submit")
    }
  return (
    <Paper
          component="form"
          onSubmit={handleSubmit}
          sx={{
            my: 1,
            pl: 2,
            borderRadius: 10,
            border: "1px solid #e3e3e3",
            boxShadow: "none",
            mr: { sm: 5, md: 12, lg: 15 },
          }}
        >
            <input
              placeholder="Search..."
              value={searchTerm}
              onChange={(e)=>{
                setsearchTerm(e.target.value)
              }}
              style={{
                border: "none",
                outline: "none",
                width: "320px",

                marginLeft: "5px",
                fontSize: "17px",
              }}
            />
    </Paper>
  )
}

export default CustomInput