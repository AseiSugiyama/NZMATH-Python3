#!/bin/sh
CVSDIR="$HOME/cvs/mochiya/"
NMATHDIR="$CVSDIR/nmath/"
BASEDIR="$NMATHDIR/manual"

WIKIBASE="http://hanaya.math.metro-u.ac.jp/nzmath-doc/"

cd $BASEDIR
wget -q $WIKIBASE\?UserManual -O index.html
wget -q $WIKIBASE\?Install -O install.html
cd modules
for docs in {arith1,bigrandom,combinatorial,elliptic,equation,finitefield,gcd,imaginary,integerResidueClass,lattice,matrix,multiplicative,polynomial,prime,rational,rationalFunction,real,vector,zassenhaus}
do
  wget -q $WIKIBASE\?$docs.py -O $docs.html
done
wget -q "$WIKIBASE\?ring%20%28en%29" -O ring.html
cd factor
for docs in {factor,mpqs,trialdivision}
do
  wget -q $WIKIBASE\?$docs.py -O $docs.html
done

cd ../../
CSSBDAT="skin\/default\.ja\.css"
CSSNDAT="default.css"
# edit index.html
CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\)\(.*\.\)\(py\)\" "
CONVNDAT="href=\"modules\/\2html\" "

cat index.html|sed -e "s/$CONVBDAT/$CONVNDAT/">index.html.sed
CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?Install\)\" "
CONVNDAT="href=\"install.html\" "
cat index.html.sed|sed -e "s/$CSSBDAT/$CSSNDAT/">index.html.se
cat index.html.se|sed -e "s/$CSSBDAT/$CSSNDAT/">index.html
#mv -f index.html.se index.html
echo "you must fix index.html for modules/factor ."

# edit all html link
CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?UserManual\)\" "
CONVNDAT="href=\"index.html\" "
cat install.html|sed -e "s/$CONVBDAT/$CONVNDAT/">install.html.sed
cat install.html.sed|sed -e "s/$CSSBDAT/$CSSNDAT/">install.html
#mv -f install.html.sed install.html

cd modules
CSSNDAT="..\/$CSSNDAT"
for htmlfile in *.html
do
  CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\)\(.*\.\)\(py\)\" "
  CONVNDAT="href=\"\2html\" "
  cat $htmlfile|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.sed
  CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?UserManual\)\" "
  CONVNDAT="href=\"..\/index.html\" "
  cat $htmlfile.sed|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.se
  cat $htmlfile.se|sed -e "s/$CSSBDAT/$CSSNDAT/">$htmlfile
  #mv -f $htmlfile.sed $htmlfile
done;

cd factor
CSSNDAT="..\/$CSSNDAT"
for htmlfile in *.html
do
  CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\)\(.*\.\)\(py\)\" "
  CONVNDAT="href=\"\2html\" "
  cat $htmlfile|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.sed
  CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?UserManual\)\" "
  CONVNDAT="href=\"..\/..\/index.html\" "
  cat $htmlfile.sed|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.se
  cat $htmlfile.se|sed -e "s/$CSSBDAT/$CSSNDAT/">$htmlfile
  #mv -f $htmlfile.sed $htmlfile
done;
