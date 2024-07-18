def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    is_offtrack = params['is_offtrack']
    
    if is_offtrack:
        return 1e-3
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_3:
        reward = 1.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
         # Reward for speed
         
    SPEED_THRESHOLD = 3.2  # Speed threshold to incentivize fast driving
    if speed > SPEED_THRESHOLD:
        reward += 1.1
    else:
        reward += speed / SPEED_THRESHOLD
    
    return float(reward)