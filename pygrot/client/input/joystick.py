import copy


class JoystickMotion(object):
    THRESHOLD = 0.2
    MAX_SPEED_PER_TICK = 20

    def __init__(self, joystick):
        self.last_motions = 0, 0, 0, 0
        self.joystick = joystick

    def update(self, dt):
        motion = [self.joystick.x, self.joystick.y, self.joystick.rx, self.joystick.ry]
        speed_values = copy.copy(motion)
        for number, value in enumerate(self.last_motions):
            if motion[number] == value:
                speed_values[number] += value if not speed_values[number] + value > self.MAX_SPEED_PER_TICK else self.MAX_SPEED_PER_TICK
        self.last_motions = motion

        return speed_values
