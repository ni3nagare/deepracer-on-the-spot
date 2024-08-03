import math
def reward_function(params) :
    punishment = 1e-3 
    reward = punishment 
    x = params ['x'] 
    y = params ['y'] 
    speed = params ['speed'] 
    heading = params ['heading'] 
    waypoints = params ['waypoints'] 
    track_width = params ['track_width'] 
    is_offtrack = params ['is_offtrack']  
    closest_waypoints = params ['closest_waypoints'] 
    all_wheels_on_track = params ['all_wheels_on_track'] 

    next_waypoint_index = closest_waypoints [1] 
    num_steps = 5 
    future_index = (next_waypoint_index + num_steps) % len(waypoints) 
    future_waypoint = waypoints[future_index] 
    future_waypoint_x, future_waypoint_y = future_waypoint
    expected_heading = math.degrees(math.atan2(future_waypoint_y - y, future_waypoint_x - x)) 
    heading_diff = abs(expected_heading - heading) 
    if heading_diff > 180:
        heading_diff = abs(360 - heading_diff) 
    if is_offtrack:
        reward += punishment
    else:
        if all_wheels_on_track and heading_diff <= 15:
            reward += round((100*speed)/(heading_diff+1))+punishment 
    
    return float(reward)