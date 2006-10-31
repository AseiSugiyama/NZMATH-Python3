from distutils.core import setup

doc_prefix = "share/doc/NZMATH-0.5.1/"

setup (
    name="NZMATH",
    version="0.5.1",
    url="http://tnt.math.metro-u.ac.jp/nzmath/",
    author="NZMATH development group",
    author_email="nzmath-user@tnt.math.metro-u.ac.jp",
    description="number theory oriented calculation system",

    packages=["nzmath", "nzmath.factor"],

    data_files=[(doc_prefix + "manual",
                 ['manual/default.css',
                  'manual/index.html',
                  'manual/install.html']),
                (doc_prefix + "manual/modules",
                 ['manual/modules/arith1.html',
                  'manual/modules/bigrandom.html',
                  'manual/modules/combinatorial.html',
                  'manual/modules/elliptic.html',
                  'manual/modules/elliptic_ECGeneric.html',
                  'manual/modules/elliptic_ECoverF2.html',
                  'manual/modules/elliptic_ECoverFp.html',
                  'manual/modules/elliptic_ECoverQ.html',
                  'manual/modules/equation.html',
                  'manual/modules/finitefield.html',
                  'manual/modules/finitefield_FiniteExtendedField.html',
                  'manual/modules/finitefield_FiniteExtendedFieldElement.html',
                  'manual/modules/finitefield_FiniteField.html',
                  'manual/modules/finitefield_FiniteFieldElement.html',
                  'manual/modules/finitefield_FinitePrimeField.html',
                  'manual/modules/finitefield_FinitePrimeFieldElement.html',
                  'manual/modules/gcd.html',
                  'manual/modules/group.html',
                  'manual/modules/group_AberianGenerate.html',
                  'manual/modules/group_GenerateGroup.html',
                  'manual/modules/group_Group.html',
                  'manual/modules/group_GroupElement.html',
                  'manual/modules/imaginary.html',
                  'manual/modules/imaginary_AbsoluteError.html',
                  'manual/modules/imaginary_Complex.html',
                  'manual/modules/imaginary_ComplexField.html',
                  'manual/modules/imaginary_ExponentialPowerSeries.html',
                  'manual/modules/imaginary_RelativeError.html',
                  'manual/modules/integerResidueClass.html',
                  'manual/modules/integerResidueClass_IntegerResidueClass.html',
                  'manual/modules/integerResidueClass_IntegerResidueClassRing.html',
                  'manual/modules/lattice.html',
                  'manual/modules/matrix.html',
                  'manual/modules/matrix_IntegerMatrix.html',
                  'manual/modules/matrix_IntegerSquareMatrix.html',
                  'manual/modules/matrix_Matrix.html',
                  'manual/modules/matrix_SquareMatrix.html',
                  'manual/modules/multiplicative.html',
                  'manual/modules/permute.html',
                  'manual/modules/permute_ExPermute.html',
                  'manual/modules/permute_Permute.html',
                  'manual/modules/polynomial.html',
                  'manual/modules/polynomial_MultiVariablePolynomialIdeal.html',
                  'manual/modules/polynomial_MultiVariableSparsePolynomial.html',
                  'manual/modules/polynomial_OneVariablePolynomial.html',
                  'manual/modules/polynomial_OneVariablePolynomialChar0.html',
                  'manual/modules/polynomial_OneVariablePolynomialCharNonZero.html',
                  'manual/modules/polynomial_OneVariablePolynomialCoefficients.html',
                  'manual/modules/polynomial_OneVariablePolynomialIdeal.html',
                  'manual/modules/polynomial_PolynomialResidueRing.html',
                  'manual/modules/polynomial_PolynomialRing.html',
                  'manual/modules/polynomial_RationalOneVariablePolynomial.html',
                  'manual/modules/prime.html',
                  'manual/modules/quad.html',
                  'manual/modules/quad_NextElement.html',
                  'manual/modules/quad_ReducedQuadraticForm.html',
                  'manual/modules/rational.html',
                  'manual/modules/rationalFunction.html',
                  'manual/modules/rationalFunction_RationalFunction.html',
                  'manual/modules/rationalFunction_RationalFunctionField.html',
                  'manual/modules/rational_Integer.html',
                  'manual/modules/rational_IntegerRing.html',
                  'manual/modules/rational_Rational.html',
                  'manual/modules/rational_RationalField.html',
                  'manual/modules/real.html',
                  'manual/modules/real_AbsoluteError.html',
                  'manual/modules/real_Constant.html',
                  'manual/modules/real_ExponentialPowerSeries.html',
                  'manual/modules/real_RealField.html',
                  'manual/modules/real_RelativeError.html',
                  'manual/modules/ring.html',
                  'manual/modules/vector.html',
                  'manual/modules/zassenhaus.html']),
                (doc_prefix + "manual/modules/factor",
                 ['manual/modules/factor/find.html',
                  'manual/modules/factor/methods.html',
                  'manual/modules/factor/misc.html',
                  'manual/modules/factor/mpqs.html',
                  'manual/modules/factor/util.html'])
                ]
     )
