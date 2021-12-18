"""
Day 17
https://adventofcode.com/2021/day/17

1st star: >24h (*)
2nd star: >24h (*)

(*) I was on vacation when this problem was solved, so I wasn't 
    able to solve it right when it was released. The first part
    took me about 20 minutes, and the second part about 5 minutes.

This was a fun little physics-like problem. I rolled the dice on
whether (-250, 250) was a large enough range to find the solution,
and it looks like my gamble paid off.
"""

import util

def launch(vel_x, vel_y, min_x, max_x, min_y, max_y):
    """
    Launch a probe with a given velocity, and check whether
    it reaches a target area (and, if so, return the largest
    value of y it reached)
    """
    x, y = 0, 0

    largest_y = 0
    while True:
        x += vel_x
        y += vel_y

        if y > largest_y:
            largest_y = y

        # Are we in the target area, or have we gone
        # past it?
        if min_x <= x <= max_x and min_y <= y <= max_y:
            return True, largest_y
        elif x > max_x or y < min_y:
            return False, None

        if vel_x > 0:
            vel_x -= 1
        elif vel_x < 0:
            vel_x += 1

        vel_y -= 1


def check_velocities(target_min_x, target_max_x, 
                     target_min_y, target_max_y, 
                     lb_x, ub_x, lb_y, ub_y):
    """
    Check all the velocities within a given range, and check whether
    the probe reaches the target. This function solves both parts 1 and 2:
    it finds the largest value of y, and also counts up the number of probes
    that end up in the target area.
    """
    best_y = 0
    best_vel_x = 0
    best_vel_y = 0
    num_in_target = 0
    for vel_x in range(lb_x, ub_x):
        for vel_y in range(lb_y, ub_y):
            in_target, largest_y = launch(vel_x, vel_y, target_min_x, target_max_x, 
                                                        target_min_y, target_max_y)
            if in_target:
                num_in_target += 1
                if largest_y > best_y:
                    best_y = largest_y
                    best_vel_x = vel_x
                    best_vel_y = vel_y

    return best_y, best_vel_x, best_vel_y, num_in_target
    

if __name__ == "__main__":
    util.set_debug(False)

    print("TASK 1 + 2")
    util.call_and_print(check_velocities, 20, 30, -10, -5, -250, 250, -250, 250)
    util.call_and_print(check_velocities, 155, 182, -117, -67, -250, 250, -250, 250)
