#!/bin/bash
touch /tmp/h_min
touch /tmp/h_max
touch /tmp/s_min
touch /tmp/s_max
touch /tmp/v_min
touch /tmp/v_max

/usr/bin/mjpg_streamer -i "/usr/lib/mjpg-streamer/input_opencv.so --filter /usr/lib/mjpg-streamer/cvfilter_py.so --fargs ./L3_image_filter.py" -o "/usr/lib/mjpg-streamer/output_http.so -p 8090 -w /usr/share/mjpg-streamer/www"
