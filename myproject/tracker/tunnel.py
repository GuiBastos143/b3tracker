import math
from scipy.stats import norm

def black_scholes_price(S, K, r, sigma, t, option_type):
    # S = Spot price, K = Strike, r = interest rate, sigma = vol, t = time in years
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * t) * norm.cdf(d2)
    else:
        return K * math.exp(-r * t) * norm.cdf(-d2) - S * norm.cdf(-d1)

def tunnel_limits(S, K, r, sigma, t, tunnel_type, option_type):
    # Set volatility shocks per tunnel type
    if tunnel_type == 'static':
        sigma_low = sigma * 0.9    # -10%
        sigma_high = sigma * 1.2   # +20%
    elif tunnel_type == 'dynamic_sync':
        sigma_low = sigma * 0.6    # -40% (example)
        sigma_high = sigma * 1.5   # +50%
    elif tunnel_type == 'dynamic_async':
        sigma_low = sigma * 0.8    # -20% (example)
        sigma_high = sigma * 1.3   # +30%
    else:
        # Default/fallback
        sigma_low = sigma * 0.9
        sigma_high = sigma * 1.2

    lower = black_scholes_price(S, K, r, sigma_low, t, option_type)
    upper = black_scholes_price(S, K, r, sigma_high, t, option_type)
    return lower, upper