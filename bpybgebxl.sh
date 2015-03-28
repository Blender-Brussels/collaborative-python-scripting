#!bin/sh    

# A shell script to download the python script and run it in Blender
curl http://codepad-demo.d250.hu/p/bpybgebxl.py/export/txt -o bpybgebxl.py
./blender --verbose 1 --background --factory-startup --python bpybgebxl.py --render-frame 1
