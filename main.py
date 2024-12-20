def edit_distance(word1: str, word2: str) -> int:
    m = len(word1)
    n = len(word2)

    # (m+1) x (n+1) matrix
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases:
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

def phrase_edit_distance(phrase1: str, phrase2: str) -> int:
    words1 = phrase1.split()
    words2 = phrase2.split()

    if len(words1) != len(words2):
        return float('inf')

    total_distance = 0
    for w1, w2 in zip(words1, words2):
        dist = edit_distance(w1, w2)
        total_distance += dist
        if total_distance > 2:
            break
    return total_distance


def suggest_corrections(query: str, dictionary: list) -> list:
    suggestions = []
    for candidate in dictionary:
        dist = phrase_edit_distance(query, candidate)
        if dist <= 2:
            suggestions.append((candidate, dist))
    suggestions.sort(key=lambda x: x[1])
    return suggestions


if __name__ == "__main__":
    # Read the dictionary from the external file
    with open("dictionary.txt", "r", encoding="utf-8") as f:
        dictionary = [line.strip() for line in f if line.strip()]

    query = "thank you mis"
    results = suggest_corrections(query, dictionary)
    print(f"Query: {query}")
    for phrase, dist in results:
        print(f"Suggestion: {phrase}, Edit Distance: {dist}")
