def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    is_offtrack = params['is_offtrack']
    steps = params["steps"]
    progress = params["progress"]
    
    if is_offtrack:
        return 1e-3
    
    # Calculate 3 markers that are at varying distances away from the center line

    marker_point = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_point:
        reward = 1.0
    else:
        reward = 1e-3  # likely crashed/ close to off track
         
    # Reward for speed
    SPEED_THRESHOLD = 2.8  # Speed threshold to incentivize fast driving
    if speed > SPEED_THRESHOLD:
        reward += 1.0
    else:
        reward += speed / SPEED_THRESHOLD
    
    # Progress reawrd 
    if progress == 100:
        reward += 25
    else:
        reward += 0
        
    # steps reward    
    
    return float(reward)