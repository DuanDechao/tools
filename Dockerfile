#####################################################################
# Dockerfile to build game server container images
# Based on Ubuntu
#####################################################################

# Set the base image to Ubuntu
FROM ubuntu

MAINTAINER ddc_cug@163.com

######################## BEGIN INSTALLATION ##########################

RUN apt-get update

# Install g++
RUN apt-get install g++

#Install git
RUN apt-get install git

#Install cmake
RUN apt-get install cmake