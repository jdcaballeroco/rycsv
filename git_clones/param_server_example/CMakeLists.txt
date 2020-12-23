cmake_minimum_required(VERSION 3.0.2)
project(param_server_example)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  std_srvs
  dynamic_reconfigure
)


################################################
## Declare ROS messages, services and actions ##
################################################

################################################
## Declare ROS dynamic reconfigure parameters ##
################################################

## Generate dynamic reconfigure parameters in the 'cfg' folder
generate_dynamic_reconfigure_options(
  cfg/param_test.cfg
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES param_server_example
#  CATKIN_DEPENDS rospy std_msgs std_srvs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

# make sure configure headers are built before any node using them
#add_dependencies(${PROJECT_NAME} ${PROJECT_NAME}_gencfg)


#############
## Install ##
#############

#############
## Testing ##
#############
