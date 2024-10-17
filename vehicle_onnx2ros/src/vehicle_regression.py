#!/usr/bin/env python3

import os
import rospy
import onnxruntime as ort
from std_msgs.msg import Float32, Float32MultiArray
import random

# Initialize ROS node
rospy.init_node('complex_vehicle_model_node')

# Get the path to the ONNX model file
onnx_model_path = '/home/urja/Desktop/onnx2ros/onnx/complex_vehicle_model.onnx'
print("Loading ONNX model from:", onnx_model_path)

# Load the ONNX model
ort_session = ort.InferenceSession(onnx_model_path)

# Check ONNX model input and output names (debugging)
input_name = ort_session.get_inputs()[0].name
print(f"Model input name: {input_name}")

# Publishers for velocity, x_position, and y_position
vel_pub = rospy.Publisher('/predicted_velocity', Float32, queue_size=10)
x_pos_pub = rospy.Publisher('/predicted_x_position', Float32, queue_size=10)
y_pos_pub = rospy.Publisher('/predicted_y_position', Float32, queue_size=10)

# Function to handle received input data from the subscriber
def process_input(msg):
    input_data = msg.data  # Extract throttle and steering angle from the message
    input_data = [input_data]  # Convert to batch of 1 sample for ONNX model

    # Perform inference using the ONNX model
    outputs = ort_session.run(None, {input_name: input_data})

    # Extract predictions
    predicted_velocity = outputs[0][0][0]  # First output is velocity
    predicted_x_position = outputs[0][0][1]  # Second output is x_position
    predicted_y_position = outputs[0][0][2]  # Third output is y_position

    # Log predictions for debugging
    rospy.loginfo(f"Predicted velocity: {predicted_velocity}")
    rospy.loginfo(f"Predicted x position: {predicted_x_position}")
    rospy.loginfo(f"Predicted y position: {predicted_y_position}")

    # Publish the predicted results
    vel_pub.publish(predicted_velocity)
    x_pos_pub.publish(predicted_x_position)
    y_pos_pub.publish(predicted_y_position)

# Function to publish random input data (throttle, steering angle)
def publish_random_input(event):
    # Generate random throttle and steering angle values
    random_throttle = random.uniform(0, 1)  # Throttle between [0, 1]
    random_steering = random.uniform(-1, 1)  # Steering angle between [-1, 1]

    # Create a message and publish the random data
    input_msg = Float32MultiArray()
    input_msg.data = [random_throttle, random_steering]

    vehicle_input_pub.publish(input_msg)

    rospy.loginfo(f"Published random input data: Throttle={random_throttle}, Steering={random_steering}")

# Publisher for random input data
vehicle_input_pub = rospy.Publisher('/vehicle_input', Float32MultiArray, queue_size=10)

# Subscriber to the input data topic (throttle, steering angle)
rospy.Subscriber('/vehicle_input', Float32MultiArray, process_input)

# Set a timer to publish random input data every second
rospy.Timer(rospy.Duration(1), publish_random_input)

# Keep the node running
rospy.spin()
