/usr/bin/mjpg_streamer -i "/usr/lib/mjpg-streamer/input_opencv.so --filter /usr/lib/mjpg-streamer/cvfilter_py.so --fargs ./$1" -o "/usr/lib/mjpg-streamer/output_http.so -p 8090 -w /usr/share/mjpg-streamer/www"

