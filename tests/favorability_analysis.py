import random
import math

def calculate_hare(party_votes, total_valid_votes, total_seats):
    """
    Calculates seat allocation using Hare Quota (Largest Remainder).
    party_votes: list of integers (votes per party)
    total_valid_votes: integer (sum of all valid votes, including eliminated ones if any)
    total_seats: integer
    Returns: list of integers (seats per party, corresponding to input order)
    """
    if total_valid_votes == 0:
        return [0] * len(party_votes)

    quota = total_valid_votes / total_seats

    seats = []
    remainders = []

    for i, votes in enumerate(party_votes):
        allocated = math.floor(votes / quota)
        rem = votes - (allocated * quota)
        seats.append(allocated)
        remainders.append((rem, i))

    allocated_seats = sum(seats)
    remaining_seats = total_seats - allocated_seats

    # Sort by remainder descending
    remainders.sort(key=lambda x: x[0], reverse=True)

    for i in range(remaining_seats):
        if len(remainders) > 0:
            idx = remainders[i % len(remainders)][1]
            seats[idx] += 1

    return seats

def calculate_sainte_lague(party_votes, total_seats):
    """
    Calculates seat allocation using Sainte-Laguë (Divisor Method).
    party_votes: list of integers
    total_seats: integer
    Returns: list of integers
    """
    seats = [0] * len(party_votes)

    for _ in range(total_seats):
        max_quotient = -1
        winner_idx = -1

        for i, votes in enumerate(party_votes):
            divisor = 2 * seats[i] + 1
            quotient = votes / divisor

            # Simple tie-breaking: lower index wins (arbitrary but consistent)
            if quotient > max_quotient:
                max_quotient = quotient
                winner_idx = i

        if winner_idx != -1:
            seats[winner_idx] += 1

    return seats

def calculate_gallagher_index(votes, seats, total_votes, total_seats):
    """
    Calculates the Gallagher Index (disproportionality).
    Lower is better (more proportional).
    """
    if total_votes == 0 or total_seats == 0:
        return 0

    sum_squares = 0
    for v, s in zip(votes, seats):
        vote_percent = (v / total_votes) * 100
        seat_percent = (s / total_seats) * 100
        diff = vote_percent - seat_percent
        sum_squares += diff ** 2

    return math.sqrt(0.5 * sum_squares)

def run_simulation():
    # Simulation Parameters
    party_counts = range(3, 16) # 3 to 15 parties
    seat_counts = [10, 50, 100, 250, 560] # Various parliament sizes
    thresholds = [0, 3, 4, 5] # 0%, 3%, 4%, and 5%
    vote_distributions = ['uniform', 'exponential', 'power-law']

    simulations_per_config = 1282 # Adjusted to ~1 million total scenarios (780 configs)

    total_scenarios = 0
    # Analysis buckets
    favorability_counts = {
        'small': {'hare': 0, 'sl': 0, 'neutral': 0},
        'medium': {'hare': 0, 'sl': 0, 'neutral': 0},
        'large': {'hare': 0, 'sl': 0, 'neutral': 0}
    }

    gallagher_stats = {
        'hare': [],
        'sl': []
    }

    print(f"Running Monte Carlo simulation with {simulations_per_config} runs per config...")

    # We will skip printing every single config line to avoid huge output,
    # but we will print summary stats.

    for num_parties in party_counts:
        for num_seats in seat_counts:
            for threshold_pct in thresholds:
                for dist_type in vote_distributions:

                    for _ in range(simulations_per_config):
                        # 1. Generate Votes
                        votes = []
                        if dist_type == 'uniform':
                            votes = [random.randint(1000, 100000) for _ in range(num_parties)]
                        elif dist_type == 'exponential':
                            votes = [int(random.expovariate(1/10000)) + 100 for _ in range(num_parties)]
                        elif dist_type == 'power-law':
                            votes = [int(random.paretovariate(1.2)) * 1000 for _ in range(num_parties)]

                        total_vote_count = sum(votes)

                        # 2. Apply Threshold
                        threshold_votes = total_vote_count * (threshold_pct / 100.0)
                        passed_indices = [i for i, v in enumerate(votes) if v >= threshold_votes]

                        if len(passed_indices) < 2: continue # Need at least 2 parties to compare

                        passed_votes = [votes[i] for i in passed_indices]

                        # 3. Calculate Allocations
                        hare_results_passed = calculate_hare(passed_votes, total_vote_count, num_seats)
                        sl_results_passed = calculate_sainte_lague(passed_votes, num_seats)

                        hare_seats_full = [0] * num_parties
                        sl_seats_full = [0] * num_parties
                        for idx, passed_idx in enumerate(passed_indices):
                            hare_seats_full[passed_idx] = hare_results_passed[idx]
                            sl_seats_full[passed_idx] = sl_results_passed[idx]

                        # Calculate Gallagher Index for this scenario (among passed parties or all? usually all but ignored if 0)
                        # Here we consider the outcome. Parties below threshold got 0 seats.
                        g_hare = calculate_gallagher_index(votes, hare_seats_full, total_vote_count, num_seats)
                        g_sl = calculate_gallagher_index(votes, sl_seats_full, total_vote_count, num_seats)

                        gallagher_stats['hare'].append(g_hare)
                        gallagher_stats['sl'].append(g_sl)

                        # 4. Analyze Favorability
                        # Classification based on vote share:
                        # Small: < 5%
                        # Medium: 5% - 15%
                        # Large: > 15%

                        small_indices = []
                        medium_indices = []
                        large_indices = []

                        for idx in range(num_parties):
                            share = votes[idx] / total_vote_count
                            if share < 0.05:
                                small_indices.append(idx)
                            elif share <= 0.15:
                                medium_indices.append(idx)
                            else:
                                large_indices.append(idx)

                        party_categories = {
                            "small": small_indices,
                            "medium": medium_indices,
                            "large": large_indices
                        }

                        for category, indices in party_categories.items():
                            if not indices: continue

                            hare_total = sum(hare_seats_full[i] for i in indices)
                            sl_total = sum(sl_seats_full[i] for i in indices)

                            if hare_total > sl_total:
                                favorability_counts[category]['hare'] += 1
                            elif sl_total > hare_total:
                                favorability_counts[category]['sl'] += 1
                            else:
                                favorability_counts[category]['neutral'] += 1

                        total_scenarios += 1

    print("Summary:")
    print(f"Total valid scenarios analyzed: {total_scenarios}")

    for category in ['small', 'medium', 'large']:
        cat_total = sum(favorability_counts[category].values())
        if cat_total == 0: continue

        hare_perc = (favorability_counts[category]['hare'] / cat_total) * 100
        sl_perc = (favorability_counts[category]['sl'] / cat_total) * 100
        neutral_perc = (favorability_counts[category]['neutral'] / cat_total) * 100

        print(f"\n--- {category.capitalize()} Parties (<5%, 5-15%, >15%) ---")
        print(f"Hare Quota favored: {favorability_counts[category]['hare']} times ({hare_perc:.2f}%)")
        print(f"Sainte-Laguë favored: {favorability_counts[category]['sl']} times ({sl_perc:.2f}%)")
        print(f"Neutral outcome:    {favorability_counts[category]['neutral']} times ({neutral_perc:.2f}%)")

    avg_g_hare = sum(gallagher_stats['hare']) / len(gallagher_stats['hare'])
    avg_g_sl = sum(gallagher_stats['sl']) / len(gallagher_stats['sl'])

    print(f"\n--- Gallagher Index (Disproportionality) ---")
    print(f"Average Hare Index: {avg_g_hare:.4f}")
    print(f"Average Sainte-Laguë Index: {avg_g_sl:.4f}")
    if avg_g_sl < avg_g_hare:
        print("Sainte-Laguë is on average more proportional.")
    else:
        print("Hare is on average more proportional.")


    print("\nCONCLUSION:")
    if favorability_counts['small']['hare'] > favorability_counts['small']['sl']:
        print("- The data SUPPORTS the claim that Hare Quota tends to favor SMALLER parties.")
    else:
        print("- The data DOES NOT support the claim that Hare Quota favors smaller parties.")

    if favorability_counts['large']['sl'] > favorability_counts['large']['hare']:
         print("- The data SUPPORTS the claim that Sainte-Laguë tends to favor LARGER parties.")
    else:
        print("- The data DOES NOT support the claim that Sainte-Laguë favors larger parties.")

if __name__ == "__main__":
    run_simulation()
