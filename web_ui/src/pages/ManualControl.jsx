import React from 'react'
import {Button,Stack, Box} from '@mui/material'
import { useSelector, useDispatch } from 'react-redux'

const ManualControl = () => {
  const rosConnectionState = useSelector((state) => state.RosConnection)
  const dispatch = useDispatch()


  const publishing_topics = {
    up_down : '/bittle/vertical_thrust',
    right_left: '/bittle/lateral_thrust',
    forward_backward: '/bittle/thrust',
    rotate_z: '/bittle/yaw'
  }

  // up_down topic
  const up_down_publisher = new window.ROSLIB.Topic({
    ros: rosConnectionState.ros,
    name:publishing_topics.up_down,
    messageType:"std_msgs/Float64"
  })

  // right_left topic
  const right_left_publisher = new window.ROSLIB.Topic({
    ros: rosConnectionState.ros,
    name:publishing_topics.right_left,
    messageType:"std_msgs/Float64"
  })

  // forward_backward topic
  const forward_backward_publisher = new window.ROSLIB.Topic({
    ros: rosConnectionState.ros,
    name:publishing_topics.forward_backward,
    messageType:"std_msgs/Float64"
  })

  // rotate_z topic
  const rotate_z_publisher = new window.ROSLIB.Topic({
    ros: rosConnectionState.ros,
    name:publishing_topics.rotate_z,
    messageType:"std_msgs/Float64"
  })


  const zero_message = new window.ROSLIB.Message({data:0})

  const publishTargetSpeed = (direction,speed) =>{

    up_down_publisher.publish(zero_message)
    right_left_publisher.publish(zero_message)
    forward_backward_publisher.publish(zero_message)
    rotate_z_publisher.publish(zero_message)

    // speed message
  const speed_message = new window.ROSLIB.Message({data:speed})
  if(rosConnectionState.connected){
    
    switch(direction){
      case 'up_down': up_down_publisher.publish(speed_message);break;
      case 'right_left': right_left_publisher.publish(speed_message);break;
      case 'forward_backward': forward_backward_publisher.publish(speed_message);break;
      case 'rotate_z': rotate_z_publisher.publish(speed_message);break;
      case 'stop': break;
      default: break;
    }
  }
  } 

  return (

    <Box sx={{mt:9}}>

      <Box sx={{mx:"auto",width:500}}>
          <Stack direction={"row"} sx={{mx:"auto"}} gap={1}>
            <Button contained="variant" sx={{backgroundColor:"lightseagreen","&:hover":{backgroundColor:"primary.main"},color:"#fff",width:250,py:1.9,fontSize:19,fontWeight:"bold", textTransform:"capitalize",mb:3}} onClick={() => publishTargetSpeed("up_down",1)}>Up</Button>
            <Button contained="variant" sx={{backgroundColor:"lightseagreen","&:hover":{backgroundColor:"primary.main"},color:"#fff",width:250,py:2,fontSize:19,fontWeight:"bold", textTransform:"capitalize",mb:3}} onClick={() => publishTargetSpeed("up_down",-1)}>Down</Button>
          </Stack>

          <Stack direction={"row"} sx={{mx:"auto"}} gap={1}>
              <Button contained="variant" sx={{backgroundColor:"lightseagreen","&:hover":{backgroundColor:"primary.main"},color:"#fff",width:250,py:2,fontSize:19,fontWeight:"bold", textTransform:"capitalize",mb:3}} onClick={() => publishTargetSpeed("right_left",1)}>Right</Button>
              <Button contained="variant" sx={{backgroundColor:"lightseagreen","&:hover":{backgroundColor:"primary.main"},color:"#fff",width:250,py:2,fontSize:19,fontWeight:"bold", textTransform:"capitalize",mb:3}} onClick={() => publishTargetSpeed("right_left",-1)}>Left</Button>
          </Stack>

          <Stack direction={"row"} sx={{mx:"auto"}} gap={1}>
              <Button contained="variant" sx={{backgroundColor:"lightseagreen","&:hover":{backgroundColor:"primary.main"},color:"#fff",width:250,py:2,fontSize:19,fontWeight:"bold", textTransform:"capitalize",mb:3}} onClick={() => publishTargetSpeed("forward_backward",1)}>Forward</Button>
              <Button contained="variant" sx={{backgroundColor:"lightseagreen","&:hover":{backgroundColor:"primary.main"},color:"#fff",width:250,py:2,fontSize:19,fontWeight:"bold", textTransform:"capitalize",mb:3}} onClick={() => publishTargetSpeed("forward_backward",-1)}>Backward</Button>
          </Stack>

          <Stack direction={"row"} sx={{mx:"auto"}} gap={1}>
              <Button contained="variant" sx={{backgroundColor:"lightseagreen","&:hover":{backgroundColor:"primary.main"},color:"#fff",width:250,py:2,fontSize:19,fontWeight:"bold", textTransform:"capitalize",mb:3}} onClick={() => publishTargetSpeed("rotate_z",1)}>Rotate CW</Button>
              <Button contained="variant" sx={{backgroundColor:"lightseagreen","&:hover":{backgroundColor:"primary.main"},color:"#fff",width:250,py:2,fontSize:19,fontWeight:"bold", textTransform:"capitalize",mb:3}} onClick={() => publishTargetSpeed("rotate_z",-1)}>Rotate CCW</Button>
          </Stack>
          <Button contained="variant" sx={{backgroundColor:"error.main","&:hover":{backgroundColor:"error.dark"},color:"#fff",width:250,py:2,fontSize:19,fontWeight:"bold", textTransform:"capitalize",mb:3}} onClick={() => publishTargetSpeed("stop",0)}>Stop</Button>

      </Box>


      </Box>
  )
}

export default ManualControl
