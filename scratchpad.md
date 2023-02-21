`model1`

* `DISTANCE_PENALTY` = 2
* `MINOR_SAFETY_PENALTY` = 1
* `MAJOR_SAFETY_PENALTY` = 10

*Verdict*: Extremely poor performance

`model2`

* `DISTANCE_PENALTY` = 2
* `MINOR_SAFETY_PENALTY` = 0.5
* `MAJOR_SAFETY_PENALTY` = 5

*Verdict*: Performs extremely well to avoid obstacles, but is throwoff by the backwall

`model3`

* `DISTANCE_PENALTY` = 2
* `MINOR_SAFETY_PENALTY` = 0.5
* `MAJOR_SAFETY_PENALTY` = 10

*Verdict*: Performs well, sometimes can overcome the obstacle and gets stuck, also is thrownoff by the backwall

`model4`

* `DISTANCE_PENALTY` = 2
* `MINOR_SAFETY_PENALTY` = 1
* `MAJOR_SAFETY_PENALTY` = 5

*Verdict*: Slightly worse than model2 in obstacle avoidance, but doesn't get thrown off by the backwall

`model5`

* `DISTANCE_PENALTY` = 3
* `MINOR_SAFETY_PENALTY` = 1
* `MAJOR_SAFETY_PENALTY` = 10

*Verdict*: Great at avoiding obstacles, but gets thrown off by the backwall.

`model6`

* `DISTANCE_PENALTY` = 4
* `MINOR_SAFETY_PENALTY` = 1
* `MAJOR_SAFETY_PENALTY` = 10

*Verdict*: Extremely smooth trajectory, but gets thrown off by the backwall.


`model7`
**Taking the best of `model4` (small `MAJOR_SAFETY_PENALTY`) and `model6` (large `DISTANCE_PENALTY`)**

* `DISTANCE_PENALTY` = 4
* `MINOR_SAFETY_PENALTY` = 1
* `MAJOR_SAFETY_PENALTY` = 5

> Remark: All the above model seem to be ignoring the y component of the offset to target. They often end up next to the target, but unable to go to the left or right to reach the target. The only way they know to succeed is to fly into the target head on, which means if there is an obstacle close to the target, all of these models fail. One way to potentially mitigate this is by randomly spawning the drone next to the target at times initially instead of all the way at the other end of the box.