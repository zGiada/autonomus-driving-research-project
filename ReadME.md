# Autonomous Driving Research Project

> Research Project for ICT FOR INDUSTRIAL APPLICATION course at @UniPD
>
> *Author:* @zGiada (me), @maddbosc and @GiorgioPovegliano

------

## Abstract

Autonomous Driving is one of the most popular and discussed technologies nowadays, as it’s ex- pected to revolutionize the way of transportation in the future. A lot of progress has been made in the last few years, especially thanks to the constant research activity and  the huge advancement in artificial intelligence and sensor and communication technology. 

Automated driving features offer numerous advantages and challenges in enhancing safety on public roads. One primary objective is to reduce road accidents caused by human error, such as distracted driving, drunk driving, and fatigue. Autonomous systems can react faster and make more accurate decisions, but they require fast detection and recognition of objects in the vehicle's surroundings. Relying solely on self-acquired information in critical situations is challenging, especially in dense traffic areas. Intelligent vehicles may need to share data with computing platforms or other vehicles to identify obstacles outside their sensors. However, the transmission of large volumes of data can be difficult, especially in dense traffic areas like main intersections.

## Goals of the project

This study aims to address the issue of exchanging data safely and efficiently to meet latency requirements. It develops an analytical method that filters and transmits only meaningful data, prioritizing transmissions with the highest value of information for the target application. The approach is generalized, assuming a central entity receiving and processing data. The controller's goal is to minimize transmissions from vehicles within intersections while ensuring a complete view of the environment.

## What I used?

- **Python**
- It is used the **linear programming**: it is a crucial tool for addressing the problem of providing a centralized view of an intersection using data from a vehicle's sensor system while minimizing transmission impact on the network. 
  The objective is to minimize the impact of transmissions on the network by using a sensor fusion approach that combines data from cameras and LiDAR sensors. This approach is known for its accuracy in detecting large objects like cars and vulnerable road users like pedestrians and cyclists.

  The central controller's goal is to provide the best visibility of the intersection by prioritizing transmission of sensor data from vehicles that contribute to the highest number of non-zero elements in the visibility. 
  The problem falls under the category of the well-known **Knapsack** **0-1 problem**.

  The 0-1 knapsack problem is a widely studied maximization problem involving the selection of items to maximize total value while minimizing combined weight. It is analogous to the knapsack problem, where each vehicle can transmit or not transmit, with the goal of maximizing overall benefit. The benefit of each transmission depends on its visibility, and a serial approach is not suitable due to interdependence among cells.

  = **pulp** library in Python