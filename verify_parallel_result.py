#!/usr/bin/env python3
"""
Verify the parallel pipeline's result for I_{5,10}(ξ).
Numerically integrate and compare with the claimed polynomial.
"""

import numpy as np
from scipy import integrate
from scipy.special import gamma, hyp2f1
import json
import sys

def integrand(t, xi, m=5, p=10):
    """Compute the integrand for I_{m,p}(ξ) at given t."""
    # Sum over k=0,1,2
    total = 0.0

    for k in range(3):
        binom_coeff = 1.0 if k == 0 else (2.0 if k == 1 else 1.0)
        sign = (-1)**k

        # Hypergeometric function
        a = -k + t/2 + 3
        b = -k + t/2 + 3
        c = -k + p + t/2 + 3

        try:
            hyp_val = hyp2f1(a, b, c, xi)
        except:
            hyp_val = 0.0

        # Numerator
        num = (np.pi * t * (t-2) * (-2*k + t + 2) * (-2*k + t + 4) *
               gamma(p-1) * gamma(p) * gamma(p - t/2))

        # Denominator
        denom = (128 * np.sin(np.pi * t / 2)**2 *
                 gamma(-t/2 - 2) * gamma(k + p - t/2 - 2) * gamma(-k + p + t/2 + 3))

        # Power of xi
        xi_power = xi**(t/2 - k)

        term = sign * binom_coeff * xi_power * hyp_val * num / denom
        total += term

    # Multiply by t^m / (2πi)
    result = t**m * total / (2 * np.pi * 1j)
    return result

def numerical_integral(xi, m=5, p=10):
    """Compute I_{m,p}(ξ) by numerical integration along Re(t) = 1/2."""
    # Integrate from 1/2 - i*inf to 1/2 + i*inf
    # Parametrize as t = 1/2 + i*y, y from -inf to inf

    def real_part(y):
        t = 0.5 + 1j * y
        val = integrand(t, xi, m, p)
        return np.real(val * 1j)  # dt = i*dy

    def imag_part(y):
        t = 0.5 + 1j * y
        val = integrand(t, xi, m, p)
        return np.imag(val * 1j)

    # Use quad with finite limits (approximate infinity)
    limit = 100
    real_result, _ = integrate.quad(real_part, -limit, limit, limit=100)
    imag_result, _ = integrate.quad(imag_part, -limit, limit, limit=100)

    return real_result + 1j * imag_result

def polynomial_value(xi):
    """Evaluate the claimed polynomial from parallel pipeline."""
    # Coefficients with denominator 2^34
    coeffs = {
        0: 4105138088309984,
        1: -118328631771463616,
        2: 833337393002881024,
        3: -2498819546167700352,
        4: 3837993971649809408,
        5: -3184523721430220800,
        6: 1363333076892884224,
        7: -236974204353653504
    }

    denom = 2**34
    result = sum(coeffs[j] * xi**j for j in range(8)) / denom
    return result

def main():
    print("=" * 70)
    print("Verification: I_{5,10}(ξ) parallel pipeline result")
    print("=" * 70)

    # Test points
    test_xis = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]

    results = []

    for xi in test_xis:
        print(f"\nξ = {xi:.2f}")
        print("-" * 70)

        try:
            num_val = numerical_integral(xi)
            poly_val = polynomial_value(xi)

            # The integral should be real (imaginary part from numerical error)
            num_real = np.real(num_val)
            num_imag = np.imag(num_val)

            error = abs(num_real - poly_val)
            rel_error = error / abs(poly_val) if poly_val != 0 else float('inf')

            print(f"  Numerical:  {num_real:.6f} + {num_imag:.2e}i")
            print(f"  Polynomial: {poly_val:.6f}")
            print(f"  Error:      {error:.2e} (relative: {rel_error:.2e})")

            results.append({
                'xi': xi,
                'numerical': num_real,
                'polynomial': poly_val,
                'error': error,
                'rel_error': rel_error,
                'status': 'PASS' if rel_error < 1e-5 else 'FAIL'
            })

        except Exception as e:
            print(f"  ERROR: {e}")
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
                print(f"  ξ={r['xi']}: {r.get('status')} - {r.get('error_msg', r.get('rel_error', 'N/A'))}")

    # Save results
    output_file = '/home/usamimira/PHY-LLM/CC_Solver/verification_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    # Exit code
    if failed > 0 or errors > 0:
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)

if __name__ == '__main__':
    main()
