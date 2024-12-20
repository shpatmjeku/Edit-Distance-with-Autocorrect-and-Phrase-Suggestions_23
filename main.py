def edit_distance(word1: str, word2: str) -> int:
    m = len(word1)
    n = len(word2)

    # Initialize a (m+1) x (n+1) matrix
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming from an empty string
    for i in range(m + 1):
        dp[i][0] = i  # Deletions
    for j in range(n + 1):
        dp[0][j] = j  # Insertions

    # Fill the DP matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],  # deletion
                                   dp[i][j - 1],  # insertion
                                   dp[i - 1][j - 1])  # substitution

    return dp[m][n]

# Example Usage
if __name__ == "__main__":
    word1 = "yll"
    word2 = "Yll"
    distance = edit_distance(word1, word2)
    print(f"Number of operations needed to convert '{word1}' and '{word2}' is {distance}")


