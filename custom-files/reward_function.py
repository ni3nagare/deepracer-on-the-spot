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
        racing_track = [
            [8.43935, 3.01029, 3.38147, 0.05182],
            [8.26558, 3.05278, 3.66668, 0.04879],
            [8.08672, 3.08829, 3.99289, 0.04567],
            [7.90355, 3.11752, 4.0, 0.04637],
            [7.7168, 3.14119, 4.0, 0.04706],
            [7.5272, 3.16003, 4.0, 0.04763],
            [7.33541, 3.17474, 4.0, 0.04809],
            [7.14197, 3.18595, 4.0, 0.04844],
            [6.94735, 3.19423, 4.0, 0.0487],
            [6.75188, 3.20006, 4.0, 0.04889],
            [6.55582, 3.20385, 4.0, 0.04902],
            [6.35935, 3.20596, 4.0, 0.04912],
            [6.16259, 3.2067, 4.0, 0.04919],
            [5.96563, 3.20637, 4.0, 0.04924],
            [5.76852, 3.20523, 4.0, 0.04928],
            [5.5713, 3.20345, 4.0, 0.04931],
            [5.374, 3.20121, 4.0, 0.04933],
            [5.17505, 3.19858, 4.0, 0.04974],
            [4.97482, 3.19625, 4.0, 0.05006],
            [4.7741, 3.1942, 4.0, 0.05018],
            [4.57315, 3.19241, 4.0, 0.05024],
            [4.37212, 3.19089, 4.0, 0.05026],
            [4.17104, 3.18963, 4.0, 0.05027],
            [3.96995, 3.1886, 4.0, 0.05027],
            [3.76885, 3.18785, 4.0, 0.05027],
            [3.56776, 3.18737, 4.0, 0.05027],
            [3.36667, 3.18723, 4.0, 0.05027],
            [3.16558, 3.18748, 4.0, 0.05027],
            [2.9645, 3.18823, 4.0, 0.05027],
            [2.767, 3.18834, 3.95374, 0.04995],
            [2.57181, 3.18691, 3.50462, 0.0557],
            [2.37972, 3.18299, 3.12204, 0.06154],
            [2.19127, 3.1757, 2.77351, 0.068],
            [2.00696, 3.1642, 2.46194, 0.07501],
            [1.82722, 3.14773, 2.14836, 0.08401],
            [1.65284, 3.12518, 1.90076, 0.09251],
            [1.48458, 3.09547, 1.60102, 0.10672],
            [1.32329, 3.05752, 1.60102, 0.1035],
            [1.17005, 3.01005, 1.60102, 0.1002],
            [1.02623, 2.95169, 1.60102, 0.09694],
            [0.89404, 2.88058, 1.60102, 0.09375],
            [0.77624, 2.79519, 1.60102, 0.09088],
            [0.67913, 2.69318, 1.72418, 0.08169],
            [0.6005, 2.5801, 1.81546, 0.07587],
            [0.53883, 2.45932, 1.86991, 0.07252],
            [0.49331, 2.33309, 1.72372, 0.07785],
            [0.46313, 2.20314, 1.58412, 0.08421],
            [0.44777, 2.07085, 1.58412, 0.08408],
            [0.44713, 1.93731, 1.58412, 0.0843],
            [0.46234, 1.80363, 1.58412, 0.08493],
            [0.49473, 1.67118, 1.58412, 0.08607],
            [0.54795, 1.5423, 1.58412, 0.08802],
            [0.62663, 1.42132, 1.8093, 0.07976],
            [0.7254, 1.30942, 2.00671, 0.07438],
            [0.84116, 1.207, 2.21542, 0.06976],
            [0.97144, 1.11408, 2.47611, 0.06463],
            [1.11377, 1.03013, 2.70413, 0.06111],
            [1.26646, 0.95486, 2.94946, 0.05772],
            [1.42796, 0.88788, 3.21408, 0.0544],
            [1.59678, 0.82869, 3.49565, 0.05118],
            [1.77157, 0.77673, 3.78893, 0.04813],
            [1.95114, 0.73143, 4.0, 0.0463],
            [2.1344, 0.69223, 4.0, 0.04685],
            [2.32052, 0.65878, 4.0, 0.04728],
            [2.50861, 0.63037, 4.0, 0.04755],
            [2.69803, 0.60658, 4.0, 0.04773],
            [2.88828, 0.58702, 4.0, 0.04781],
            [3.07897, 0.57137, 4.0, 0.04783],
            [3.26976, 0.55938, 4.0, 0.04779],
            [3.46043, 0.55084, 4.0, 0.04771],
            [3.65077, 0.54552, 4.0, 0.04761],
            [3.84067, 0.54323, 4.0, 0.04748],
            [4.03002, 0.54376, 4.0, 0.04734],
            [4.21876, 0.54698, 4.0, 0.04719],
            [4.40686, 0.55268, 4.0, 0.04705],
            [4.59434, 0.5606, 4.0, 0.04691],
            [4.78125, 0.57046, 4.0, 0.04679],
            [4.96764, 0.58196, 4.0, 0.04669],
            [5.15358, 0.59487, 4.0, 0.0466],
            [5.33912, 0.60895, 4.0, 0.04652],
            [5.52029, 0.62381, 4.0, 0.04544],
            [5.70023, 0.63691, 4.0, 0.0451],
            [5.87917, 0.64789, 4.0, 0.04482],
            [6.05734, 0.65625, 4.0, 0.04459],
            [6.23489, 0.66152, 4.0, 0.04441],
            [6.41189, 0.66326, 4.0, 0.04425],
            [6.58836, 0.66112, 4.0, 0.04412],
            [6.76427, 0.65482, 4.0, 0.04401],
            [6.9396, 0.64421, 4.0, 0.04391],
            [7.11426, 0.62934, 4.0, 0.04382],
            [7.28813, 0.61046, 4.0, 0.04372],
            [7.46095, 0.58796, 4.0, 0.04357],
            [7.63235, 0.56236, 4.0, 0.04333],
            [7.80193, 0.53428, 3.33195, 0.05159],
            [7.96951, 0.50442, 2.85192, 0.05968],
            [8.13557, 0.47356, 2.47562, 0.06823],
            [8.28586, 0.44612, 2.17672, 0.07019],
            [8.43501, 0.42144, 1.95745, 0.07723],
            [8.58213, 0.40161, 1.70296, 0.08717],
            [8.72643, 0.38847, 1.46848, 0.09867],
            [8.86712, 0.38376, 1.3, 0.10829],
            [9.00334, 0.38927, 1.3, 0.10487],
            [9.1341, 0.40675, 1.3, 0.10148],
            [9.25837, 0.43766, 1.3, 0.09851],
            [9.37417, 0.48478, 1.3, 0.09617],
            [9.47805, 0.55213, 1.3, 0.09523],
            [9.56436, 0.64413, 1.60016, 0.07883],
            [9.63662, 0.75205, 1.74666, 0.07436],
            [9.69488, 0.87319, 1.88058, 0.07148],
            [9.73892, 1.00522, 2.02877, 0.06861],
            [9.76881, 1.14568, 2.1333, 0.06731],
            [9.78428, 1.29229, 2.22742, 0.06619],
            [9.78535, 1.4427, 2.29394, 0.06557],
            [9.7721, 1.59463, 2.28822, 0.06665],
            [9.745, 1.74604, 2.13553, 0.07203],
            [9.70477, 1.89525, 1.9143, 0.08072],
            [9.65229, 2.04097, 1.9143, 0.08091],
            [9.58774, 2.18197, 1.9143, 0.08101],
            [9.51133, 2.3171, 1.9143, 0.08109],
            [9.422, 2.44446, 1.9143, 0.08126],
            [9.31851, 2.56165, 1.9143, 0.08167],
            [9.19824, 2.66442, 2.15017, 0.07357],
            [9.06505, 2.75444, 2.36942, 0.06785],
            [8.92115, 2.83302, 2.59959, 0.06307],
            [8.76816, 2.90129, 2.82723, 0.05926],
            [8.60723, 2.96012, 3.07084, 0.0558],
        ]

        # planned speed based on waypoints
        # manually adjust the list for better performance, e.g. lower the speed before turning
        above_three_five = [
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            75,
            76,
            77,
            78,
            79,
            80,
            81,
            82,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            91,
            92,
            93,
            94,
        ]
        above_three = [1, 2, 122, 123, 124, 125, 126]
        above_two_five = [95, 96, 97, 98, 99, 100, 101]
        above_two = [
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            112,
            113,
            114,
            115,
            116,
            117,
            118,
            119,
            120,
            121,
        ]
        # planned speed based on waypoints
        # observe which side the car is expected to run at
        right_track = [83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93]
        center_track = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            59,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            94,
        ]
        left_track = [
            10,
            11,
            12,
            13,
            3,
            36,
            37,
            38,
            39,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            75,
            76,
            77,
            787,
            79,
            80,
            81,
            82,
            95,
            96,
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            104,
            109,
            110,
            111,
            112,
            113,
            114,
            115,
            116,
            117,
            118,
            124,
            125,
            126,
        ]

        # obvious sides
        strong_left = [
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            105,
            106,
            107,
            108,
            119,
            120,
            121,
            122,
            123,
        ]
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
