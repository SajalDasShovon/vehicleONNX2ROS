# vehicleONNX2ROS  
  
  
# The package is designed for position prediction using throttle and steering of a car. #


**Neural Network Definition**

A neural network architecture includes:

Input Layer: 2 neurons (for throttle and steering angle).

Hidden Layers:
First hidden layer with 128 neurons.

Second hidden layer with 64 neurons.

Output Layer: 3 neurons corresponding to the predictions for velocity, x-position, and y-position.


**After training for 100 epochs, the model is exported to the ONNX format using torch.onnx.export(). This allows the model to be used in ROS.**


**ROS Architecture**

ONNX2ROS Key Components:

ONNX Model Loading: node loads a pre-trained ONNX model named vehicle_regression.onnx for performing inference.  
Input Data Processing: It subscribes to the /vehicle_input topic, which provides a Float32MultiArray containing throttle and steering angle values.  

Inference and Prediction:
The input data is processed and fed into the ONNX model to predict position and velocity.

Publish Results:  
Predicted position is published to the /predicted_position topic.


Random Input Publisher:  
The publish_random_input function generates random throttle and steering angle values within specified ranges and publishes them as a message.


ROS Subscriber and Timer:  
A subscriber is set up to listen for incoming messages.  
The pretrained model predicts the position of car from the random input of throttle & steering.

