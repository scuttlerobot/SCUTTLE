#!/bin/bash
touch /tmp/h_min
touch /tmp/h_max
touch /tmp/s_min
touch /tmp/s_max
touch /tmp/v_min
touch /tmp/v_max

/usr/local/bin/mjpg_streamer -i "/usr/local/lib/mjpg-streamer/input_opencv.so --filter /usr/local/lib/mjpg-streamer/cvfilter_py.so --fargs ./L3_image_filter.py" -o "/usr/local/lib/mjpg-streamer/output_http.so -p 8090 -w /usr/local/share/mjpg-streamer/www"

