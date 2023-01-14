#!/bin/bash

range=102/116/31/42
grid=0.5
SCALE=m109/37/0.3i
tpwt=$1
ant=$2
grdfile=test_boundary #grid2dv.30.z.txt
cptfile=test.cpt
TOPO_GRD=topo.grd
TOPO_GRD2=topo.grd2
TOPO_GRA=topo.gradient
gmt makecpt -Cseis -T3.3/3.8/0.1 -D -Z > test.cpt

title1=$1 #`echo $tpwt | awk -F. '{print "TPWT_"$3"_"$4}'`
title2=$2 #`echo $ant  | awk -F_ '{print "ANT_"$2"_"$3"_"$4}'`
cat $tpwt | awk '{print $1,$2,$3}' | gmt blockmean -R$range -I0.5 > vel1
gmt surface vel1 -Gvel1.grd -R$range -I0.5
gmt grdsample vel1.grd -I0.01 -Gvel1.grd1
cat $ant  | awk '{print $1,$2,$3}' | gmt blockmean -R$range -I0.5 > vel2
gmt surface vel2 -Gvel2.grd -R$range -I0.5
gmt grdsample vel2.grd -I0.01 -Gvel2.grd1

gmt grdcut ETOPO1.grd -R$range -G$TOPO_GRD
gmt grdsample $TOPO_GRD -G$TOPO_GRD2  -I0.01 -R$range
gmt grdgradient $TOPO_GRD2  -A45 -G$TOPO_GRA -Nt -V

gmt gmtset MAP_FRAME_TYPE plain
gmt gmtset MAP_TITLE_OFFSET 0.25p
gmt gmtset MAP_DEGREE_SYMBOL none
gmt gmtset FONT_TITLE 18
gmt begin "$title1"_"$title2" pdf
gmt coast -J$SCALE -R$range -BWSne+t"$title1" -Bxa2f2 -Bya2f2 -W -Dl -A10000 -Gwhite
gmt clip $grdfile #test_C_40.00_0.txt
gmt grdimage vel1.grd1 -C$cptfile -I$TOPO_GRA
gmt clip -C
cat station.1021163044.lst | awk '{print $2,$3}' | gmt psxy -St0.1c -Gblue -Wblack
cat ncc_lv.xy | gmt psxy -W0.8p,black
echo "test1"

gmt coast -J$SCALE -R$range -BWSne+t"$title2" -Bxa2f2 -Bya2f2 -W -Dl -A10000 -Gwhite -X12
gmt clip $grdfile #test_C_40.00_0.txt
gmt grdimage vel2.grd1 -C$cptfile -I$TOPO_GRA
gmt clip -C
cat station.1021163044.lst | awk '{print $2,$3}' | gmt psxy -St0.1c -Gblue -Wblack
cat ncc_lv.xy | gmt psxy -W0.8p,black
gmt colorbar -C$cptfile -DjBC+w5c/0.4c+o0c/-1.5c+m -Bxa0.2f0.2
echo "test2"

gmt coast -J$SCALE -R$range -BWSne -Bxa2f2 -Bya2f2 -W -Dl -A10000 -Gwhite -X-12 -Y-10.5
gmt surface vel1 -Gveldiff1.grd -R$range -I$grid
gmt grd2xyz veldiff1.grd > veldiff1
gmt surface vel2 -Gveldiff2.grd -R$range -I$grid
gmt grd2xyz veldiff2.grd > veldiff2
paste veldiff1 veldiff2 | awk '{print $1,$2,$3-$6}' > temp_diff.xyz
cat temp_diff.xyz | awk '{print $1,$2,$3*1000}' | gmt blockmean -R$range -I$grid > tomo_diff.xyz
cat tomo_diff.xyz | gmt surface -I$grid -Gdiff.grd -R$range
gmt grdsample diff.grd -I0.01 -Gdiff1.grd -R$range
gmt clip $grdfile #ant_C_30.lst
gmt grdimage diff1.grd -Cvs_dif2.cpt -I$TOPO_GRA
gmt clip -C
cat station.1021163044.lst | awk '{print $2,$3}' | gmt psxy -St0.1c -Gblue -Wblack
cat ncc_lv.xy | gmt psxy -W0.8p,black
gmt colorbar -Cvs_dif2.cpt -DjBC+w8c/0.4c+o0c/-1.5c+m -Bxa30f30
echo "test3"

gmt gmtselect tomo_diff.xyz -F$grdfile > diff.calc
aa=`cat diff.calc | awk 'BEGIN{aa=0}{aa=aa+$3}END{printf "%6.2f\n",aa/NR}'`
bb=`cat diff.calc | awk 'BEGIN{sum=0} {sum=sum+$3*$3} END{printf"%-8.2f\n",sqrt(sum/NR)}'`
echo $aa $bb
echo 1 2 "average velocity $aa" | gmt pstext -JX10c/5c -R0/3/0/3 -B5 -F+f12p -X12
echo 1 1 "std $bb" | gmt pstext -F+f12p
gmt end
