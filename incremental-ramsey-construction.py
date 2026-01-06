# ==========================================
# Old-table local-threshold generator (new rule)
# ==========================================

def exists_table(n, t, step_limit=10_000_000):
    """
    Check whether there exists a 0/1 assignment
    to the old triangular table of size n
    satisfying the new comparison rule.
    """

    # table[i] represents row i+1 (0-based index)
    # row i has n - (i+1) entries
    table = []
    steps = 0

    def valid_with_previous(i):
        """
        Check row i (0-based) against all j < i
        """
        row_i = table[i]
        len_i = len(row_i)

        for j in range(i):
            row_j = table[j]
            pivot_index = (i + 1) - (j + 1) - 1  # (i - j) in 1-based, minus 1 for 0-based

            # safety check (should always hold)
            if pivot_index < 0 or pivot_index >= len(row_j):
                continue

            pivot_value = row_j[pivot_index]
            count = 0

            # compare same positions k
            for k in range(len_i):
                if row_i[k] == row_j[k] == pivot_value:
                    count += 1
                    if count > t:
                        return False

        return True

    def dfs(i):
        nonlocal steps
        steps += 1
        if steps > step_limit:
            return False

        if i == n - 1:
            return True  # all rows filled

        row_length = n - (i + 1)

        # try all 0/1 assignments for row i
        for mask in range(1 << row_length):
            row = [(mask >> k) & 1 for k in range(row_length)]
            table.append(row)

            if valid_with_previous(i):
                if dfs(i + 1):
                    return True

            table.pop()

        return False

    return dfs(0)


def find_max_n(t, max_n=30):
    """
    Incrementally test n = 1,2,3,...
    Stop at first failure.
    """
    for n in range(1, max_n + 1):
        print(f"Testing n = {n} ...")
        ok = exists_table(n, t)
        if ok:
            print(f"  ✓ n = {n} is feasible")
        else:
            print(f"  ✗ n = {n} is NOT feasible")
            print(f"\nMaximum feasible n = {n-1}")
            return n - 1

    print(f"\nNo failure up to n = {max_n}")
    return max_n


# ===============================
# User input
# ===============================

t = int(input("Enter threshold t: "))
max_n = int(input("Search up to max n = "))

result = find_max_n(t, max_n)
print("\nResult:", result)

