import math


class Reward:
    def __init__(self):
        self.first_racingpoint_index = 0

    def reward_function(self, params):

        ################## HELPER FUNCTIONS ###################

        def dist_2_points(x1, x2, y1, y2):
            return abs(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2) ** 0.5

        def closest_2_racing_points_index(racing_coords, car_coords):

            # Calculate all distances to racing points
            distances = []
            for i in range(len(racing_coords)):
                distance = dist_2_points(
                    x1=racing_coords[i][0],
                    x2=car_coords[0],
                    y1=racing_coords[i][1],
                    y2=car_coords[1],
                )
                distances.append(distance)

            # Get index of the closest racing point
            closest_index = distances.index(min(distances))

            # Get index of the second closest racing point
            distances_no_closest = distances.copy()
            distances_no_closest[closest_index] = 999
            second_closest_index = distances_no_closest.index(min(distances_no_closest))

            return [closest_index, second_closest_index]

        def dist_to_racing_line(closest_coords, second_closest_coords, car_coords):

            # Calculate the distances between 2 closest racing points
            a = abs(
                dist_2_points(
                    x1=closest_coords[0],
                    x2=second_closest_coords[0],
                    y1=closest_coords[1],
                    y2=second_closest_coords[1],
                )
            )

            # Distances between car and closest and second closest racing point
            b = abs(
                dist_2_points(
                    x1=car_coords[0],
                    x2=closest_coords[0],
                    y1=car_coords[1],
                    y2=closest_coords[1],
                )
            )
            c = abs(
                dist_2_points(
                    x1=car_coords[0],
                    x2=second_closest_coords[0],
                    y1=car_coords[1],
                    y2=second_closest_coords[1],
                )
            )

            # Calculate distance between car and racing line (goes through 2 closest racing points)
            # try-except in case a=0 (rare bug in DeepRacer)
            try:
                distance = abs(
                    -(a**4)
                    + 2 * (a**2) * (b**2)
                    + 2 * (a**2) * (c**2)
                    - (b**4)
                    + 2 * (b**2) * (c**2)
                    - (c**4)
                ) ** 0.5 / (2 * a)
            except:
                distance = b

            return distance

        # Calculate which one of the closest racing points is the next one and which one the previous one
        def next_prev_racing_point(
            closest_coords, second_closest_coords, car_coords, heading
        ):

            # Virtually set the car more into the heading direction
            heading_vector = [
                math.cos(math.radians(heading)),
                math.sin(math.radians(heading)),
            ]
            new_car_coords = [
                car_coords[0] + heading_vector[0],
                car_coords[1] + heading_vector[1],
            ]

            # Calculate distance from new car coords to 2 closest racing points
            distance_closest_coords_new = dist_2_points(
                x1=new_car_coords[0],
                x2=closest_coords[0],
                y1=new_car_coords[1],
                y2=closest_coords[1],
            )
            distance_second_closest_coords_new = dist_2_points(
                x1=new_car_coords[0],
                x2=second_closest_coords[0],
                y1=new_car_coords[1],
                y2=second_closest_coords[1],
            )

            if distance_closest_coords_new <= distance_second_closest_coords_new:
                next_point_coords = closest_coords
                prev_point_coords = second_closest_coords
            else:
                next_point_coords = second_closest_coords
                prev_point_coords = closest_coords

            return [next_point_coords, prev_point_coords]

        def racing_direction_diff(
            closest_coords, second_closest_coords, car_coords, heading
        ):

            # Calculate the direction of the center line based on the closest waypoints
            next_point, prev_point = next_prev_racing_point(
                closest_coords, second_closest_coords, car_coords, heading
            )

            # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
            track_direction = math.atan2(
                next_point[1] - prev_point[1], next_point[0] - prev_point[0]
            )

            # Convert to degree
            track_direction = math.degrees(track_direction)

            # Calculate the difference between the track direction and the heading direction of the car
            direction_diff = abs(track_direction - heading)
            if direction_diff > 180:
                direction_diff = 360 - direction_diff

            return direction_diff

        #################### RACING LINE ######################

        # Optimal racing line for the Spain track
        # Each row: [x,y,speed,timeFromPreviousPoint]
        racing_track = [[4.30807, 0.44315, 4.0, 0.03167],
[4.43468, 0.44827, 4.0, 0.03168],
[4.56133, 0.45301, 4.0, 0.03169],
[4.68803, 0.45739, 4.0, 0.03169],
[4.81477, 0.46143, 3.73408, 0.03396],
[4.94155, 0.46522, 3.35733, 0.03778],
[5.06795, 0.46883, 3.08653, 0.04097],
[5.19314, 0.47323, 2.86192, 0.04377],
[5.3174, 0.47905, 2.7006, 0.04606],
[5.44063, 0.48684, 2.61812, 0.04716],
[5.56252, 0.49715, 2.56584, 0.04767],
[5.68275, 0.51048, 2.52461, 0.04792],
[5.80102, 0.52725, 2.33972, 0.05106],
[5.91701, 0.54785, 2.16444, 0.05443],
[6.03045, 0.57256, 1.98716, 0.05843],
[6.1412, 0.60144, 1.80096, 0.06355],
[6.24916, 0.63444, 1.61627, 0.06985],
[6.35426, 0.67152, 1.40594, 0.07927],
[6.45606, 0.71312, 1.40123, 0.07848],
[6.55402, 0.75973, 1.40123, 0.07742],
[6.64744, 0.81199, 1.40123, 0.07639],
[6.73534, 0.87073, 1.40123, 0.07545],
[6.8163, 0.93705, 1.40123, 0.07469],
[6.88783, 1.01275, 1.40123, 0.07433],
[6.94934, 1.09734, 1.56579, 0.06679],
[7.00234, 1.18879, 1.72804, 0.06117],
[7.04795, 1.28585, 1.93671, 0.05537],
[7.08731, 1.38743, 2.11018, 0.05163],
[7.12112, 1.4929, 2.29898, 0.04818],
[7.14999, 1.60175, 2.44562, 0.04604],
[7.17425, 1.71367, 2.69244, 0.04253],
[7.1945, 1.82821, 2.91843, 0.03986],
[7.21119, 1.94505, 3.1475, 0.0375],
[7.22467, 2.06394, 3.35409, 0.03567],
[7.23521, 2.18462, 3.45364, 0.03508],
[7.24295, 2.30684, 3.38597, 0.03617],
[7.24795, 2.43019, 3.30129, 0.0374],
[7.25015, 2.55412, 3.22188, 0.03847],
[7.24948, 2.67795, 3.03214, 0.04084],
[7.24586, 2.80106, 2.85776, 0.0431],
[7.23925, 2.92295, 2.67253, 0.04568],
[7.22964, 3.04329, 2.51901, 0.04793],
[7.21699, 3.16186, 2.26472, 0.05265],
[7.20128, 3.27852, 2.01646, 0.05838],
[7.18228, 3.39303, 1.8067, 0.06424],
[7.15973, 3.50515, 1.59778, 0.07158],
[7.13331, 3.6146, 1.41374, 0.07965],
[7.10276, 3.72114, 1.32972, 0.08335],
[7.06736, 3.82417, 1.32972, 0.08193],
[7.02621, 3.92287, 1.32972, 0.08043],
[6.97835, 4.01631, 1.32972, 0.07895],
[6.92254, 4.10307, 1.32972, 0.07758],
[6.85735, 4.18119, 1.32972, 0.07652],
[6.78241, 4.24918, 1.38635, 0.07298],
[6.69913, 4.30734, 1.53101, 0.06635],
[6.60928, 4.35695, 1.68884, 0.06077],
[6.51411, 4.39911, 1.88375, 0.05526],
[6.41467, 4.43492, 2.05281, 0.05149],
[6.31158, 4.46509, 2.24504, 0.04784],
[6.20542, 4.49028, 2.44576, 0.04461],
[6.09661, 4.51104, 2.65944, 0.04165],
[5.98551, 4.52789, 2.89169, 0.03886],
[5.87244, 4.54128, 3.17974, 0.03581],
[5.75768, 4.55171, 3.53324, 0.03261],
[5.64143, 4.55964, 3.9873, 0.02922],
[5.52375, 4.56558, 4.0, 0.02946],
[5.40461, 4.57001, 4.0, 0.02981],
[5.28378, 4.57328, 4.0, 0.03022],
[5.1606, 4.57779, 4.0, 0.03082],
[5.03753, 4.58341, 4.0, 0.0308],
[4.91457, 4.59013, 4.0, 0.03079],
[4.79173, 4.59796, 4.0, 0.03077],
[4.66901, 4.60691, 4.0, 0.03076],
[4.54644, 4.61701, 4.0, 0.03075],
[4.42401, 4.62825, 4.0, 0.03074],
[4.3017, 4.64045, 4.0, 0.03073],
[4.1795, 4.65349, 4.0, 0.03072],
[4.05741, 4.66726, 4.0, 0.03072],
[3.9354, 4.68163, 4.0, 0.03071],
[3.8175, 4.69607, 4.0, 0.0297],
[3.69949, 4.70994, 4.0, 0.02971],
[3.58134, 4.72318, 4.0, 0.02972],
[3.46304, 4.73576, 4.0, 0.02974],
[3.34453, 4.74758, 4.0, 0.02977],
[3.22576, 4.75852, 4.0, 0.02982],
[3.10668, 4.76856, 4.0, 0.02988],
[2.98722, 4.77758, 4.0, 0.02995],
[2.8673, 4.78554, 4.0, 0.03005],
[2.74686, 4.7924, 4.0, 0.03016],
[2.62584, 4.79814, 4.0, 0.03029],
[2.5042, 4.8027, 4.0, 0.03043],
[2.38192, 4.80602, 3.84178, 0.03184],
[2.25903, 4.808, 3.57342, 0.03439],
[2.13562, 4.80849, 3.32468, 0.03712],
[2.01182, 4.80731, 3.09796, 0.03996],
[1.88784, 4.80422, 2.8946, 0.04284],
[1.76396, 4.79895, 2.71691, 0.04564],
[1.64051, 4.7912, 2.57075, 0.04812],
[1.51785, 4.78062, 2.46907, 0.04986],
[1.39639, 4.76686, 2.46866, 0.04952],
[1.27655, 4.74956, 2.37684, 0.05094],
[1.15879, 4.72837, 2.28851, 0.05229],
[1.04351, 4.70297, 2.15679, 0.05473],
[0.93113, 4.67312, 1.97711, 0.05881],
[0.82194, 4.63871, 1.80928, 0.06327],
[0.71598, 4.6, 1.63437, 0.06903],
[0.61349, 4.5569, 1.42462, 0.07804],
[0.51477, 4.50934, 1.3, 0.08429],
[0.42029, 4.45707, 1.3, 0.08306],
[0.33086, 4.39956, 1.3, 0.08179],
[0.24749, 4.33629, 1.3, 0.08051],
[0.17161, 4.26659, 1.3, 0.07925],
[0.10584, 4.18949, 1.3, 0.07796],
[0.05269, 4.10523, 1.42812, 0.06976],
[0.01029, 4.01645, 1.50897, 0.0652],
[-0.0224, 3.92457, 1.57006, 0.06211],
[-0.04607, 3.83054, 1.62395, 0.05971],
[-0.06129, 3.73507, 1.55108, 0.06233],
[-0.06846, 3.63872, 1.42556, 0.06777],
[-0.06794, 3.54196, 1.42556, 0.06788],
[-0.05994, 3.44516, 1.42556, 0.06814],
[-0.04444, 3.34867, 1.42556, 0.06855],
[-0.02066, 3.25296, 1.42556, 0.06918],
[0.01297, 3.15881, 1.42556, 0.07013],
[0.05846, 3.06766, 1.64813, 0.06181],
[0.11295, 2.97961, 1.83459, 0.05644],
[0.17482, 2.89457, 2.04363, 0.05146],
[0.24275, 2.81228, 2.21388, 0.0482],
[0.31597, 2.73258, 2.37608, 0.04555],
[0.39386, 2.65534, 2.6721, 0.04105],
[0.47552, 2.58018, 3.03692, 0.03655],
[0.56016, 2.50673, 3.50257, 0.03199],
[0.64706, 2.43462, 3.72981, 0.03027],
[0.73588, 2.36329, 3.54321, 0.03215],
[0.82567, 2.28881, 3.47434, 0.03358],
[0.91432, 2.21277, 3.47434, 0.03361],
[1.00148, 2.13521, 3.47434, 0.03358],
[1.08709, 2.05607, 3.47434, 0.03356],
[1.17103, 1.97525, 3.47434, 0.03354],
[1.25314, 1.89259, 3.47434, 0.03354],
[1.33333, 1.808, 3.52781, 0.03304],
[1.41166, 1.72155, 3.69541, 0.03157],
[1.48827, 1.6334, 3.77066, 0.03097],
[1.56334, 1.54374, 3.36884, 0.03471],
[1.63698, 1.45279, 3.06013, 0.03824],
[1.7091, 1.36088, 2.76811, 0.04221],
[1.77915, 1.26879, 2.49547, 0.04637],
[1.84957, 1.17903, 2.21575, 0.05149],
[1.92114, 1.09133, 1.97995, 0.05717],
[1.99415, 1.00612, 1.76503, 0.06357],
[2.06887, 0.92383, 1.53232, 0.07254],
[2.14564, 0.84498, 1.53232, 0.07181],
[2.22484, 0.77025, 1.53232, 0.07106],
[2.30701, 0.7006, 1.53232, 0.0703],
[2.39272, 0.63716, 1.53232, 0.06959],
[2.48265, 0.58141, 1.53232, 0.06905],
[2.57787, 0.53584, 1.59773, 0.06607],
[2.67772, 0.49982, 1.7888, 0.05934],
[2.78121, 0.47164, 2.02193, 0.05305],
[2.88759, 0.44984, 2.22264, 0.04886],
[2.99643, 0.43353, 2.4301, 0.04529],
[3.10743, 0.422, 2.67166, 0.04177],
[3.22033, 0.4146, 2.93237, 0.03859],
[3.33497, 0.41075, 3.24932, 0.0353],
[3.45121, 0.40991, 3.67203, 0.03166],
[3.56891, 0.41153, 4.0, 0.02943],
[3.68788, 0.41501, 4.0, 0.02975],
[3.80788, 0.41984, 4.0, 0.03002],
[3.92856, 0.42549, 4.0, 0.0302],
[4.05502, 0.43174, 4.0, 0.03165],
[4.18152, 0.43763, 4.0, 0.03166]]

        # planned speed based on waypoints
        # manually adjust the list for better performance, e.g. lower the speed before turning
        above_three_five = []
        above_three = [5,6,7,8,33,34,35,36,37,38,39,40,41,65,76,77,88,89,90,91,92,93,94,95,96,133,146,165]
        above_two_five = []
        above_two = [1,2,3,4,66,67,68,69,70,71,72,73,74,75,134,135,136,137,138,139,140,141,142,143,144,145,166,167,168,169,170,171,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,78,79,80,81,82,83,84,85,86,87,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121]
        # planned speed based on waypoints
        # observe which side the car is expected to run at
        right_track = [1,2,3,4,66,67,68,69,70,71,72,73,74,75,134,135,136,137,138,139,140,141,142,143,144,145,166,167,168,169,170,171]
        center_track = [5,6,7,8,33,34,35,36,37,38,39,40,41,65,76,77,88,89,90,91,92,93,94,95,96,133,146,165]
        left_track = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,78,79,80,81,82,83,84,85,86,87,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164]

        # obvious sides
        strong_left = []
        strong_right = []

        ################## INPUT PARAMETERS ###################

        # Read all input parameters
        x = params["x"]
        y = params["y"]
        distance_from_center = params["distance_from_center"]
        is_left_of_center = params["is_left_of_center"]
        heading = params["heading"]
        progress = params["progress"]
        steps = params["steps"]
        speed = params["speed"]
        steering_angle = abs(params["steering_angle"])
        track_width = params["track_width"]
        is_offtrack = params["is_offtrack"]

        ############### OPTIMAL X,Y,SPEED,TIME ################

        # Get closest indexes for racing line (and distances to all points on racing line)
        closest_index, second_closest_index = closest_2_racing_points_index(
            racing_track, [x, y]
        )

        # Get optimal [x, y, speed, time] for closest and second closest index
        optimals = racing_track[closest_index]
        optimals_second = racing_track[second_closest_index]

        if steps == 1:
            self.first_racingpoint_index = closest_index

        ################ REWARD AND PUNISHMENT ################
        reward = 1e-3

        # Zero reward if off track ##
        if is_offtrack is True:
            return reward

        # Zero reward if obviously wrong direction (e.g. spin)
        direction_diff = racing_direction_diff(
            optimals[0:2], optimals_second[0:2], [x, y], heading
        )
        if direction_diff > 30:
            return reward

        # Reward if car goes close to optimal racing line
        def get_distance_reward(threshold, distance, multiplier):
            distance_reward = max(0, 1 - (distance / threshold))

            return distance_reward * multiplier

        DIST_THRESH = track_width * 0.5
        dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])

        if distance_from_center < 0.01 * track_width:
            if closest_index in center_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
        elif is_left_of_center:
            if closest_index in left_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
            if closest_index in strong_left:
                reward += get_distance_reward(DIST_THRESH, dist, 5)
        else:
            if closest_index in right_track:
                reward += get_distance_reward(DIST_THRESH, dist, 1)
            if closest_index in strong_right:
                reward += get_distance_reward(DIST_THRESH, dist, 5)

        def get_speed_reward(ceiling, threshold, diff):
            return ceiling - diff / threshold

        # Reward if speed falls within optimal range
        PENALTY_RATIO = 0.9
        SPEED_DIFF_NO_REWARD = 1
        speed_diff = abs(optimals[2] - speed)
        if speed_diff > SPEED_DIFF_NO_REWARD:
            return 1e-3

        if closest_index in above_three_five:
            if speed >= 3.5:
                reward += get_speed_reward(0.5, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 3:
                reward *= PENALTY_RATIO
        elif closest_index in above_three:
            if speed >= 3:
                reward += get_speed_reward(0.5, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 8:
                reward *= PENALTY_RATIO
        elif closest_index in above_two_five:
            if speed >= 2.5:
                reward += get_speed_reward(0.8, SPEED_DIFF_NO_REWARD, speed_diff)
            if steering_angle > 15:
                reward *= PENALTY_RATIO
        elif closest_index in above_two:
            if speed >= 2:
                reward += get_speed_reward(1, SPEED_DIFF_NO_REWARD, speed_diff)
        else:
            if speed < 2:
                reward += get_speed_reward(3, SPEED_DIFF_NO_REWARD, speed_diff)

        # Incentive for finishing the lap in less steps ##
        REWARD_FOR_FASTEST_TIME = (
            2000  # should be adapted to track length and other rewards
        )
        TARGET_STEPS = 110
        if progress == 100:
            reward += REWARD_FOR_FASTEST_TIME / (steps - TARGET_STEPS)

        #################### RETURN REWARD ####################

        # Always return a float value
        return float(reward)


reward_object = Reward()


def reward_function(params):
    return reward_object.reward_function(params)