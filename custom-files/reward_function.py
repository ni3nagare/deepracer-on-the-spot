def reward_function(params):
    '''
    Reward function for AWS DeepRacer on a bowtie track.
    '''

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])
    all_wheels_on_track = params['all_wheels_on_track']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Extract the closest waypoints
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]

    # Calculate the direction from the previous waypoint to the next waypoint
    import math

    track_direction = math.atan2(
        next_waypoint[1] - prev_waypoint[1],
        next_waypoint[0] - prev_waypoint[0]
    )
    track_direction = math.degrees(track_direction)
    
    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    
    # Ensure the difference is within [0, 180] range
    if direction_diff > 180:
        direction_diff = 360 - direction_diff



    # Initialize reward
    reward = 1.0

    # Reward for staying within the track boundaries
    if not all_wheels_on_track:
        return 1e-3  # Low reward if the car is off the track

    # Calculate distance markers from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Reward based on distance from the center line
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # Likely crashed/close to off track

    # Additional reward for maintaining a good speed
    SPEED_THRESHOLD = 3.0
    if speed > SPEED_THRESHOLD:
        reward += 0.5

    # Penalty for excessive steering
    STEERING_THRESHOLD = 20.0
    if steering_angle > STEERING_THRESHOLD:
        reward *= 0.8

    DIRECTION_THRESHOLD = 15.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5
    

    return float(reward)
