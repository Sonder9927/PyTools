#!/bin/bash

topodata=@earth_relief_01s
R=115.5/122.5/29/35

# for file in `ls -d grids/grid.*`
for per in 20 25 30 35 40 45 50 60 70 80 90 100
do
file=`ls -d grids/grid.${per}.*`
echo $file
range=`gmt gmtinfo $file | awk '{print$7}' | sed 's/<//g' | sed 's/>//g'` 
# range=3.65/3.75
sta=station.lst
TOPO_GRD=topo.grd
TOPO_GRD2=topo.grd2
TOPO_GRA=topo.gradient
###gmt grdcut ETOPO1.grd -R$R -G$TOPO_GRD
gmt grdcut $topodata -R$R -G$TOPO_GRD
gmt grdsample $TOPO_GRD -G$TOPO_GRD2 -I0.01 -R$R
gmt grdgradient $TOPO_GRD2 -A45 -G$TOPO_GRA -Nt -V

cat $file | awk '{print $1,$2,$3}' > tmp
cat tmp | gmt blockmean -R$R -I0.01 > ttmp
gmt surface ttmp -Gtmp.grd -R$R -I0.01
gmt grdsample tmp.grd -I0.01 -Gtmp2.grd
gmt makecpt -Cgray -T2.5/3.6/0.1 -Z >g.cpt

gmt begin $file png
gmt gmtset MAP_FRAME_TYPE plain
gmt grdimage $TOPO_GRD2 -I$TOPO_GRA -Cg.cpt #Parts outside the target area,g means glue
#gmt clip boundry.dat -R$R
gmt clip boundary.dat -R$R
gmt makecpt -CVc_1.8s.cpt -T$range -D -H > Icpt.cpt 
gmt grdimage tmp2.grd -CIcpt.cpt -I$TOPO_GRA  #Parts inside the target area
gmt clip -C
cat China_tectonic.dat | gmt psxy -W1p,black,-
cat CN-faults.dat | gmt psxy -W1p,black,-
gmt colorbar -CIcpt.cpt -DjBC+w10c/0.3c+o0c/-1c+m -Bxa0.05f0.05 
cat $sta | awk '{print $2,$3}' | gmt psxy -St0.2 -Gred
cat $sta | awk '{print $2,$3,$1}' | gmt pstext -F+f5p,0.35,white+jTR -Dj0.1c/-0.1c 
# gmt coast -BWSne+t"$file" -Bxa0.6f0.1 -Bya0.4f0.1 -Df -A1000 -W1/0.8p,black -W2/0.5p,black
gmt coast -BWSne -Bxa1f0.5 -Bya1f0.5 -Df -A1000 -W1/0.8p,black -W2/0.5p,black
echo T=$per | gmt text -R$R -F+f30p,4+cBL -D2c/2c
gmt end 
mv $file.png ${file}_boundary.png
done
mv grids/*.png figs/
