FROM osrf/ros:humble-desktop
SHELL ["/bin/bash", "-c"]

ENV DISPLAY 0

# Install additional packages
RUN sudo apt update \
    && apt install -y pip \
    # Clean up
    && apt autoremove -y \
    && apt clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --disable-pip-version-check --no-cache-dir -U -r requirements.txt \
    && rm requirements.txt

WORKDIR /home/OBJECT_DETECTION/ROS

#ENTRYPOINT ["tail", "-f", "/dev/null"]
CMD source /opt/ros/humble/setup.bash && source install/setup.bash && ros2 run unity_tcp_endpoint unity_tcp_endpoint
