#!/usr/bin/env python3
"""
Verify I_{5,10}(ξ) using mpmath for high-precision numerical integration.
"""

from mpmath import mp, quad, gamma, hyp2f1, sin, pi, matrix
import json
import sys

# Set high precision
mp.dps = 50  # 50 decimal places

def integrand(t, xi, m=5, p=10):
    """Compute the integrand for I_{m,p}(ξ)."""
    total = mp.mpc(0)

    for k in range(3):
        # Binomial coefficient C(2,k)
        binom = mp.binomial(2, k)
        sign = (-1)**k

        # Hypergeometric parameters
        a = -k + t/2 + 3
        b = -k + t/2 + 3
        c = -k + p + t/2 + 3

        # Hypergeometric function
        hyp_val = hyp2f1(a, b, c, xi)

        # Numerator
        num = (pi * t * (t-2) * (-2*k + t + 2) * (-2*k + t + 4) *
               gamma(p-1) * gamma(p) * gamma(p - t/2))

        # Denominator
        denom = (128 * sin(pi * t / 2)**2 *
                 gamma(-t/2 - 2) * gamma(k + p - t/2 - 2) * gamma(-k + p + t/2 + 3))

        # Power of xi
        xi_power = xi**(t/2 - k)

        term = sign * binom * xi_power * hyp_val * num / denom
        total += term

    # Multiply by t^m / (2πi)
    result = t**m * total / (2 * pi * mp.j)
    return result

def numerical_integral(xi, m=5, p=10):
    """Compute I_{m,p}(ξ) by contour integration along Re(t) = 1/2."""
    # Parametrize: t = 1/2 + i*y, y from -inf to +inf
    # dt = i*dy

    def integrand_y(y):
        t = mp.mpf('0.5') + mp.j * y
        val = integrand(t, xi, m, p)
        return val * mp.j  # dt = i*dy

    # Integrate from -inf to +inf (mpmath handles this)
    result = quad(integrand_y, [-mp.inf, mp.inf])
    return result

def polynomial_value(xi):
    """Evaluate the claimed polynomial from parallel pipeline."""
    # Coefficients with denominator 2^34
    coeffs = {
        0: mp.mpf('4105138088309984'),
        1: mp.mpf('-118328631771463616'),
        2: mp.mpf('833337393002881024'),
        3: mp.mpf('-2498819546167700352'),
        4: mp.mpf('3837993971649809408'),
        5: mp.mpf('-3184523721430220800'),
        6: mp.mpf('1363333076892884224'),
        7: mp.mpf('-236974204353653504')
    }

    denom = mp.mpf(2)**34
    result = sum(coeffs[j] * mp.mpf(xi)**j for j in range(8)) / denom
    return result

def main():
    print("=" * 70)
    print("Verification: I_{5,10}(ξ) with mpmath (50 digits precision)")
    print("=" * 70)

    # Test points
    test_xis = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.95]

    results = []

    for xi in test_xis:
        print(f"\nξ = {xi:.2f}")
        print("-" * 70)

        try:
            num_val = numerical_integral(xi)
            poly_val = polynomial_value(xi)

            # Should be real
            num_real = mp.re(num_val)
            num_imag = mp.im(num_val)

            error = abs(num_real - poly_val)
            rel_error = float(error / abs(poly_val)) if abs(poly_val) > 1e-10 else float('inf')

            print(f"  Numerical:  {num_real:.10f} + {num_imag:.2e}i")
            print(f"  Polynomial: {poly_val:.10f}")
            print(f"  Error:      {error:.2e} (relative: {rel_error:.2e})")

            status = 'PASS' if rel_error < 1e-6 else 'FAIL'
            results.append({
                'xi': xi,
                'numerical': str(num_real),
                'polynomial': str(poly_val),
                'error': str(error),
                'rel_error': rel_error,
                'status': status
            })

            print(f"  Status: {status}")

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                'xi': xi,
                'error_msg': str(e),
                'status': 'ERROR'
            })

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results if r.get('status') == 'PASS')
    failed = sum(1 for r in results if r.get('status') == 'FAIL')
    errors = sum(1 for r in results if r.get('status') == 'ERROR')

    print(f"Total tests: {len(results)}")
    print(f"  PASS:  {passed}")
    print(f"  FAIL:  {failed}")
    print(f"  ERROR: {errors}")

    if failed > 0 or errors > 0:
        print("\nFailed/Error cases:")
        for r in results:
            if r.get('status') != 'PASS':
                print(f"  ξ={r['xi']}: {r.get('status')}")

    # Save results
    output_file = '/home/usamimira/PHY-LLM/CC_Solver/verification_results_mpmath.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    if passed == len(results):
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
