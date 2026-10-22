cmake_minimum_required(VERSION 3.8)
project(mini_bot)

find_package(ament_cmake REQUIRED)

# solutions/ NO se instala: sus sim.launch.py chocarían con launch/sim.launch.py
# (ros2 launch busca por nombre en todo share/ y se niega si hay dos).
install(DIRECTORY
  urdf
  launch
  config
  rviz
  worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
