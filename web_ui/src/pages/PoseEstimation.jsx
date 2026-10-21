import React, { useState } from 'react'
import {Box,Stack,Typography} from '@mui/material'
import { Container } from '@mui/system';
import { useSelector, useDispatch } from 'react-redux'

const PoseEstimation = () => {


// ##################### Current Distance Functions ############################# //

  const [apriltag_cam_dist, setapriltag_cam_dist] = useState(0)

  const rosConnectionState = useSelector((state) => state.RosConnection)
  const dispatch = useDispatch()

  const poseEstimationListner = new window.ROSLIB.Topic({
    ros: rosConnectionState.ros,
    name:"/distance_to_camera",  // distance between bittle and camera
    messageType:"std_msgs/Float64"
  })

  // subscribing
  const poseEstimationCallback = (msg)=>{
    setapriltag_cam_dist(Number(msg.data).toFixed(2))
  }


  if(poseEstimationListner.ros){
    poseEstimationListner?.subscribe(poseEstimationCallback)
  }

  return (
    <Container sx={{}}>
      <Box sx={{mt:9}}>

      <Box>
          <Stack direction="row" gap={20} sx={{mx:"auto",justifyContent:"center"}}>
            <Box>
                <Typography variant='h4' sx={{mt:6}}>Distance between Camera and Apriltag</Typography>
                <Box sx={{height:30,mb:11,mt:3,backgroundColor:"#25292a",width:300,mx:"auto",py:3.5,color:"lightseagreen",alignItems:"center",display:"flex",justifyContent:"center",fontSize:30,borderRadius:5}}>
                    {apriltag_cam_dist}
                </Box>
            </Box>
          </Stack>
      </Box>
    </Box>
    </Container>
  )
}

export default PoseEstimation
