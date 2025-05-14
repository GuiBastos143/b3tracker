import math
from scipy.stats import norm

def black_scholes_call(S, K, t, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    call_price = S * norm.cdf(d1) - K * math.exp(-r * t) * norm.cdf(d2)
    return call_price

def calculate_tunnel_bounds(S, K, t, r, sigma, method='static'):
    if method == 'static':
        sigma_low = sigma * (1 - 0.1)   # 10% down
        sigma_high = sigma * (1 + 0.2)  # 20% up
    elif method == 'dynamic_sync':
        sigma_low = sigma * (1 - 0.4)
        sigma_high = sigma * (1 + 0.5)
    elif method == 'dynamic_async':
        sigma_low = sigma * (1 - 0.2)
        sigma_high = sigma * (1 + 0.3)
    else:
        raise ValueError("Invalid tunnel method")

    price_low = black_scholes_call(S, K, t, r, sigma_low)
    price_high = black_scholes_call(S, K, t, r, sigma_high)
    return price_low, price_high