#!/bin/sh
# you only change CVSDIR to your mochia(simath)cvs repo.
CVSDIR="$HOME/cvs/mochiya/"
NMATHDIR="$CVSDIR/nmath/"
BASEDIR="$NMATHDIR/manual"

WIKIBASE="http://hanaya.math.metro-u.ac.jp/nzmath-doc/"

# 1. get base document.
cd $BASEDIR
wget -q $WIKIBASE\?UserManual -O index.html
wget -q $WIKIBASE\?Install -O install.html
# 1.1. get module core document.
cd modules
for docs in arith1 bigrandom combinatorial elliptic equation finitefield gcd imaginary integerResidueClass lattice matrix multiplicative polynomial prime rational rationalFunction real ring vector zassenhaus
do
  wget -q $WIKIBASE\?$docs.py -O $docs.html
done
# 1.1.1 get submodule core document. 
for subs in factor
do
  cd $subs
  for docs in factor mpqs trialdivision
  do
    wget -q $WIKIBASE\?$subs%2F$docs.py -O $docs.html
  done
  cd ../
done

# 2. edit document.
cd ../
CSSBDAT="skin\/default\.ja\.css"
CSSNDAT="default.css"
# 2.1. edit index.html .
CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\)\(.*\.\)\(py\)\" "
CONVNDAT="href=\"modules\/\2html\" "

cat index.html|sed -e "s/$CONVBDAT/$CONVNDAT/">index.html.sed
CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?Install\)\" "
CONVNDAT="href=\"install.html\" "
cat index.html.sed|sed -e "s/$CSSBDAT/$CSSNDAT/">index.html.se
cat index.html.se|sed -e "s/$CSSBDAT/$CSSNDAT/">index.html.sed
cat index.html.sed|sed -e "s/%2F/\//">index.html
#mv -f index.html.se index.html
echo "you must fix index.html for modules/factor ."

# 2.2. edit all html link.
# 2.2.1 edit install.html .
CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?UserManual\)\" "
CONVNDAT="href=\"index.html\" "
cat install.html|sed -e "s/$CONVBDAT/$CONVNDAT/">install.html.sed
cat install.html.sed|sed -e "s/$CSSBDAT/$CSSNDAT/">install.html
#mv -f install.html.sed install.html

# 2.2.2. edit module cores .
cd modules
CSSNDAT="..\/$CSSNDAT"
for htmlfile in *.html
do
  CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\)\(.*\.\)\(py\)\" "
  CONVNDAT="href=\"\2html\" "
  cat $htmlfile|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.sed
  CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\)\(.*\.\)\(py\)#\(.*\)\" "
  CONVNDAT="href=\"\2html#\4\" "
  cat $htmlfile.sed|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.se
  CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?UserManual\)\" "
  CONVNDAT="href=\"..\/index.html\" "
  cat $htmlfile.se|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.sed
  cat $htmlfile.sed|sed -e "s/$CSSBDAT/$CSSNDAT/">$htmlfile
  #mv -f $htmlfile.sed $htmlfile
done

# 2.2.3. edit submodule cores .
for subs in factor
do
  cd $subs
  CSSNDAT="..\/$CSSNDAT"
  for htmlfile in *.html
  do
    CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\)\(.*\.\)\(py\)\" "
    CONVNDAT="href=\"\2html\" "
    cat $htmlfile|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.sed
    CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\)\(.*\.\)\(py\)#\(.*\)\" "
    CONVNDAT="href=\"..\/\2html#\4\" "
    cat $htmlfile.sed|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.se
    CONVBDAT="href=\"\(http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?UserManual\)\" "
    CONVNDAT="href=\"..\/index.html\" "
    cat $htmlfile.se|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.sed
    cat $htmlfile.sed|sed -e "s/$CSSBDAT/$CSSNDAT/">$htmlfile
  done
  cd ../
done
cd ../
# 3. cleanup temporary file .
rm -rf *.se *.sed modules/*.se modules/*.sed modules/*/*.se modules/*/*.sed
