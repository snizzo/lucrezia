import os
import os.path
import sys

'''
Fix correct lighting by applying correct normals to every vertex manually
'''
def apply_normals(filename):
    os.system("sed -i '/<UV> { 0 1 }/a<Normal> { 0 0 1 }' "+filename)
    os.system("sed -i '/<UV> { 1 1 }/a<Normal> { 0 0 1 }' "+filename)
    os.system("sed -i '/<UV> { 1 0 }/a<Normal> { 0 0 1 }' "+filename)
    os.system("sed -i '/<UV> { 0 0 }/a<Normal> { 0 0 1 }' "+filename)

charname = sys.argv[1]
filename = charname + ".png"

if charname == "--help":
    print "      =====PANDARPG ENGINE CHARACTERFY 0.1====="
    print "This script autogenerates a correct pandarpg character representation starting from a 128x192 rpgmaker xp tile.\n"
    print "Please insert the folder name of the character that should be have the following folder structure:"
    print " <charname>/<charname>.png\n"
    sys.exit()

print "Changing directory..."
if not os.path.exists(charname):
    print "ERROR: Couldn't find a folder called "+charname+"!"
    sys.exit()
os.chdir(charname)

print "Clearing previous files..."
if not os.path.exists(filename):
    print "ERROR: Couldn't find a tileable image called "+filename+"!"
    sys.exit()
os.system("find . ! -name '"+filename+"' -type f -exec rm -f {} +")

print "Cropping image..."
os.system("convert "+filename+" -crop 32x48 image-%d.png")

print "Renaming images..."
os.system("mv image-0.png wdown0.png")
os.system("mv image-1.png wdown1.png")
os.system("mv image-2.png wdown2.png")
os.system("mv image-3.png wdown3.png")
os.system("mv image-4.png wleft0.png")
os.system("mv image-5.png wleft1.png")
os.system("mv image-6.png wleft2.png")
os.system("mv image-7.png wleft3.png")
os.system("mv image-8.png wright0.png")
os.system("mv image-9.png wright1.png")
os.system("mv image-10.png wright2.png")
os.system("mv image-11.png wright3.png")
os.system("mv image-12.png wtop0.png")
os.system("mv image-13.png wtop1.png")
os.system("mv image-14.png wtop2.png")
os.system("mv image-15.png wtop3.png")

print "Baking animation eggs..."
os.system("egg-texture-cards -g0,1,0,1 -p384,384 -o wdown.egg -fps 4 wdown*.png")
os.system("egg-texture-cards -g0,1,0,1 -p384,384 -o wright.egg -fps 4 wright*.png")
os.system("egg-texture-cards -g0,1,0,1 -p384,384 -o wleft.egg -fps 4 wleft*.png")
os.system("egg-texture-cards -g0,1,0,1 -p384,384 -o wtop.egg -fps 4 wtop*.png")

print "Applying normals to animations..."
apply_normals("wdown.egg")
apply_normals("wleft.egg")
apply_normals("wtop.egg")
apply_normals("wright.egg")

print "Baking static eggs..."
os.system("egg-texture-cards -g0,1,0,1 -p384,384 -o sdown.egg wdown0.png")
os.system("egg-texture-cards -g0,1,0,1 -p384,384 -o sright.egg wright0.png")
os.system("egg-texture-cards -g0,1,0,1 -p384,384 -o sleft.egg wleft0.png")
os.system("egg-texture-cards -g0,1,0,1 -p384,384 -o stop.egg wtop0.png")

print "Applying normals to statics..."

apply_normals("sdown.egg")
apply_normals("sleft.egg")
apply_normals("stop.egg")
apply_normals("sright.egg")

print "Done!"
