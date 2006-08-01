#!/bin/sh
# you only change TMP to your global temporary directory.
# usage:
# $ ./nzmathwiki_publish.sh
# automatically create nzmath-current manual located to
# /tmp/nzmath .
# if you check difference between nzmath-cvs manual,
# $ diff -ubBr /tmp/nzmath/manual {your-nzmathcvs-repo}/manual
# or you check only new version files,
# $ diff -r --brief /tmp/nzmath/manual {your-nzmathcvs-repo}/manual

# 0. check options. if set, cleanup and exit.
if [ "x$1" != "x" ]; then
    echo -n "Cleanup and remove /tmp/nzmath/manual ..."
    rm -rf /tmp/nzmath/manual
    echo "Done."
    exit 0
fi

# 0.1 structure directory tree.
TMP="/tmp"
echo -n "Check directory /tmp ..."
cd $TMP
[ -d nzmath ] || mkdir nzmath
[ -d nzmath/manual ] || mkdir nzmath/manual
[ -d nzmath/manual/modules ] || mkdir nzmath/manual/modules
[ -d nzmath/manual/modules/factor ] || mkdir nzmath/manual/modules/factor
BASEDIR="$TMP/nzmath/manual"
echo "ok."
WIKIBASE="http://hanaya.math.metro-u.ac.jp/nzmath-doc/"

echo "start to document source download from nzmath-doc wiki..."
# 1. get base document.
cd $BASEDIR
wget -q $WIKIBASE\?UserManual -O index.html
wget -q $WIKIBASE\?Install -O install.html
wget -q $WIKIBASE\?Tutorial -O tutorial.html
# 1.1. get module core document.
cd modules
for docs in arith1 bigrandom combinatorial elliptic equation finitefield gcd group imaginary integerResidueClass lattice matrix multiplicative permute polynomial prime quad rational rationalFunction real ring vector zassenhaus
do
  wget -q $WIKIBASE\?$docs.py -O $docs.html
done
# 1.1.1 get submodule core document. 
for subs in factor
do
  cd $subs
  for docs in find methods misc mpqs util
  do
    wget -q $WIKIBASE\?$subs%2F$docs.py -O $docs.html
  done
  cd ../
done
# 1.2. get module class document.
for docs in elliptic
do
  for clses in ECGeneric ECoverF2 ECoverFp ECoverQ
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in finitefield
do
  for clses in FiniteField FinitePrimeField FiniteExtendedField FiniteFieldElement FinitePrimeFieldElement FiniteExtendedFieldElement
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in group
do
  for clses in AberianGenerate GenerateGroup Group GroupElement
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in imaginary
do
  for clses in AbsoluteError Complex ComplexField ExponentialPowerSeries RelativeError
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in integerResidueClass
do
  for clses in IntegerResidueClass IntegerResidueClassRing
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in matrix
do
  for clses in Matrix SquareMatrix
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in permute
do
  for clses in ExPermute Permute
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in polynomial
do
  for clses in MultiVariableSparsePolynomial OneVariablePolynomial OneVariablePolynomialChar0 RationalOneVariablePolynomial OneVariablePolynomialCharNonZero OneVariablePolynomialCoefficients PolynomialRing MultiVariablePolynomialIdeal OneVariablePolynomialIdeal PolynomialResidueRing
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in quad
do
  for clses in ReducedQuadraticForm
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in rational
do
  for clses in Integer IntegerRing Rational RationalField
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in rationalFunction
do
  for clses in RationalFunction RationalFunctionField
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done
for docs in real
do
  for clses in RealField Constant ExponentialPowerSeries AbsoluteError RelativeError
  do
    wget -q $WIKIBASE\?$docs.py%2F$clses -O $docs\_$clses.html
  done
done

echo "automatically document parse and convert..."
# 2. edit document.
cd ../
CSSBDAT="skin\/default\.ja\.css"
CSSNDAT="default.css"
# 2.1. edit index.html .
cat index.html|sed -e "s/$CSSBDAT/$CSSNDAT/">index.html.sed
CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(.*\.\)py\" "
CONVNDAT="href=\"modules\/\1html\" "

cat index.html.sed|sed -e "s/$CONVBDAT/$CONVNDAT/">index.html.se
CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?Install\" "
CONVNDAT="href=\"install.html\" "
cat index.html.se|sed -e "s/$CONVBDAT/$CONVNDAT/">index.html.sed
CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?Tutorial\" "
CONVNDAT="href=\"tutorial.html\" "
cat index.html.sed|sed -e "s/$CONVBDAT/$CONVNDAT/">index.html.se
cat index.html.se|sed -e "s/%2F/\//">index.html

# 2.2. edit all html link.
# 2.2.1 edit core htmls .
for docs in install tutorial
do
  cat $docs.html|sed -e "s/$CSSBDAT/$CSSNDAT/">$docs.html.sed
  CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?UserManual\" "
  CONVNDAT="href=\"index.html\" "
  cat $docs.html.sed|sed -e "s/$CONVBDAT/$CONVNDAT/">$docs.html.se
  CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?Install\" "
  CONVNDAT="href=\"install.html\" "
  cat $docs.html.se|sed -e "s/$CONVBDAT/$CONVNDAT/">$docs.html
done
# 2.2.2. edit module cores .
cd modules
CSSNDAT="..\/$CSSNDAT"
for htmlfile in *.html
do
  CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(\(.*\.\)py\)\" title=\"\1\( ([0-9]*[mhd])\)\">"
  CONVNDAT="href=\"\2html\" title=\"\1\">"
  sed -e "s/$CONVBDAT/$CONVNDAT/g" $htmlfile>$htmlfile.sed
  CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(\(.*\.\)py\)#\(.*\)\" title=\"\1\( ([0-9]*[mhd])\)\">"
  CONVNDAT="href=\"\2html#\3\" title=\"\1\">"
  sed -e "s/$CONVBDAT/$CONVNDAT/g" $htmlfile.sed>$htmlfile.se
  CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(\(.*\.\)py\)#\(.*\)\" title=\"\3\( ([0-9]*[mhd])\)\">"
  CONVNDAT="href=\"\2html#\3\" title=\"\3\">"
  sed -e "s/$CONVBDAT/$CONVNDAT/g" $htmlfile.se>$htmlfile.sed

  CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(\(.*\)\.py\)%2F\(.*\)\" title=\"\1\/\3\( ([0-9]*[mhd])\)\">"
  CONVNDAT="href=\"\2_\3.html\" title=\"\1\/\3\">"
  cat $htmlfile.sed|sed -e "s/$CONVBDAT/$CONVNDAT/g">$htmlfile.se
  CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(\(.*\)\.py\)%2F\(.*\)#\(.*\)\" title=\"\4\( ([0-9]*[mhd])\)\">"
  CONVNDAT="href=\"\2_\3.html#\4\" title=\"\4\">"
  cat $htmlfile.se|sed -e "s/$CONVBDAT/$CONVNDAT/g">$htmlfile.sed
  CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(\(.*\)\.py\)%2F\(.*\)#\(.*\)\" title=\"\1\/\3\( ([0-9]*[mhd])\)\">"
  CONVNDAT="href=\"\2_\3.html#\4\" title=\"\1\/\3\">"
  cat $htmlfile.sed|sed -e "s/$CONVBDAT/$CONVNDAT/g">$htmlfile.se
  CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?UserManual\" "
  CONVNDAT="href=\"..\/index.html\" "
  cat $htmlfile.se|sed -e "s/$CONVBDAT/$CONVNDAT/g">$htmlfile.sed
  cat $htmlfile.sed|sed -e "s/$CSSBDAT/$CSSNDAT/"g>$htmlfile
done

# 2.2.3. edit submodule cores .
CSSNDAT="..\/$CSSNDAT"
for subs in factor
do
  cd $subs
  for htmlfile in *.html
  do
    CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(.*\.\)py\" "
    CONVNDAT="href=\"..\/\1html\" "
    cat $htmlfile|sed -e "s/$CONVBDAT/$CONVNDAT/g">$htmlfile.sed
    CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(.*\.\)\{1\}py#\(.*\)\" "
    CONVNDAT="href=\"..\/\1html#\2\" "
    cat $htmlfile.sed|sed -e "s/$CONVBDAT/$CONVNDAT/g">$htmlfile.se
    CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(.*\)\.py%2F\(.*\)\" "
    CONVNDAT="href=\"..\/\1_\2.html\" "
    cat $htmlfile.se|sed -e "s/$CONVBDAT/$CONVNDAT/g">$htmlfile.sed
    CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?\(.*\)\.py%2F\(.*\)#\(.*\)\" "
    CONVNDAT="href=\"..\/\1_\2.html#\3\" "
    cat $htmlfile.sed|sed -e "s/$CONVBDAT/$CONVNDAT/g">$htmlfile.se
    CONVBDAT="href=\"http:\/\/hanaya\.math\.metro-u\.ac\.jp\/nzmath\/?UserManual\" "
    CONVNDAT="href=\"..\/..\/index.html\" "
    cat $htmlfile.se|sed -e "s/$CONVBDAT/$CONVNDAT/">$htmlfile.sed
    cat $htmlfile.sed|sed -e "s/$CSSBDAT/$CSSNDAT/">$htmlfile
  done
  cd ../
done
cd ../

echo "cleanup temporary files ..."
# 3. cleanup temporary file .
rm -rf *.se *.sed modules/*.se modules/*.sed modules/*/*.se modules/*/*.sed

echo "Done."
exit 0