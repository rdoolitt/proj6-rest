import arrow
import datetime
import math

CONTROL_SPECS = [(200, 15, 34), (400, 15, 32), (600, 15, 30), (1000, 11.428, 28), (1300, 13.333, 26)]
FINAL_OPEN = [0, 5.55, 9, 12.133, 18.8, 39]
FINAL_CLOSE = [1, 13.5, 20, 27, 40, 75]
FINAL_CHECKPOINT = [0, 200, 300, 400, 600, 1000]


def shift_n_round(time, shift):
   start_time = arrow.get(time)
   shifted_time = start_time.shift(hours = shift)
   dateTime = datetime.datetime.fromisoformat(str(shifted_time))
   seconds = dateTime.second
   if seconds < 30:
      return shifted_time.floor('minute')
   else:
      return shifted_time.shift(minutes = 1).floor('minute')


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
   if control_dist_km >= brevet_dist_km:
      controlDistance = math.floor(brevet_dist_km)
      if controlDistance in FINAL_CHECKPOINT:
         openTime = shift_n_round(brevet_start_time, FINAL_OPEN[FINAL_CHECKPOINT.index(controlDistance)])
         return openTime.isoformat()
   else:
      controlDistance = math.floor(control_dist_km)

   previousDistance = 0
   distanceBetween = []

   for control in CONTROL_SPECS:
      distance, minimum, maximum = control
      distanceBetween.append(distance - previousDistance)
      previousDistance = distance

   startTime = arrow.get(brevet_start_time)
   remainingDistance = controlDistance
   startDelay = 0

   for control, distance_between in zip(CONTROL_SPECS, distanceBetween):
      distance, minimum, maximum = control
      if remainingDistance <= 0:
         break
      startDelay += (min(distance_between, remainingDistance)/maximum)
      remainingDistance -= distance_between

   openTime = shift_n_round(brevet_start_time, startDelay)
   return openTime.isoformat() 


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
   if control_dist_km >= brevet_dist_km:
      controlDistance = math.floor(brevet_dist_km)
      if controlDistance in FINAL_CHECKPOINT:
         closeTime = shift_n_round(brevet_start_time, FINAL_CLOSE[FINAL_CHECKPOINT.index(controlDistance)])
         return closeTime.isoformat()
   else:
      controlDistance = math.floor(control_dist_km)

   previousDistance = 0
   distanceBetween = []

   for control in CONTROL_SPECS:
      distance, minimum, maximum = control
      distanceBetween.append(distance - previousDistance)
      previousDistance = distance

   startTime = arrow.get(brevet_start_time)
   remainingDistance = controlDistance
   closeDelay = 0

   for control, distance_between in zip(CONTROL_SPECS, distanceBetween):
      distance, minimum, maximum = control
      if remainingDistance <= 0:
         break
      closeDelay += (min(distance_between, remainingDistance)/minimum)
      remainingDistance -= distance_between

   closeTime = shift_n_round(brevet_start_time, closeDelay)
   return closeTime.isoformat()