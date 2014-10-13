# Humanoid

This is a module that deals with the constructon and organization of humanoid
robots.

# Modules

The base of each model is a joint type. Joint types control how a part of the
robot can move.

# Serializers

Each component provides a serializer which can be used to create a json api
representation of the robot. This is a usefull feature when setting up a
control system.
