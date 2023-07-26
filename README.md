# xdf-reader

Simple parser for xdf-based binary files. Assumes the following format:
* list of streams (as dict) containing: streaminfo ('info'), datapoints ('time_series') and associated time stamps ('time_stamps')

Containing streams include:
* 'Progress': experiment progress markers
* 'Stick-Figure': [pose landmarker model](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/) of the user (33 landmarks)
    * [x,y,z,visibility] for each landmark -> 33*4=132 channels
* 'XSensDot Hydra#X': number of XSens streams (two each, including proper acceleration and quaternions) of four placed IMUs (twice ankles, twice hip)
  * proper acceleration: [x,y,z,local_timestamp] (local_timestamp can be ignored)
  * quaternions: [a,b,c,d,local_timestamp] (local_timestamp can be ignored)

More pyxdf examples:
* https://github.com/xdf-modules/pyxdf/tree/main
* https://github.com/xdf-modules/pyxdf/blob/main/pyxdf/example.py