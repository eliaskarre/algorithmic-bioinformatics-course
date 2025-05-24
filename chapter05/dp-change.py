def dpchange(money, coins):
    coins = list(coins)

    #dp[i] = minimale Münzen für Betrag i
    dp = [float('inf')] * (money + 1)
    dp[0] = 0  #0 Münzen für 0 Cent

    #Baue dp schrittweise auf
    for m in range(1, money + 1):
        for coin in coins:
            if m >= coin:
                if dp[m - coin] + 1 < dp[m]:
                    dp[m] = dp[m - coin] + 1

    return dp[money]

m = 12
c = {1,5,6}
print(dpchange(m, c))


def dpchange_nominations(money, coins):
    coins = list(coins)

    #dp = [float('inf')] * (money + 1)
    dp = [[float('inf'), {}] for i in range(money + 1)]
    dp[0][0] = 0

    for m in range(1, money + 1):
        for coin in coins:
            if m >= coin:
                if dp[m - coin][0] + 1 < dp[m][0]:
                    dp[m][0] = dp[m - coin][0] + 1

                    #Speichere Münzenhäufigkeiten
                    dp[m][1] = dp[m - coin][1].copy()
                    dp[m][1][coin] = dp[m][1].get(coin, 0) + 1

    return dp

m = 50
c = {25,15,10, 2}
print(dpchange_nominations(m, c))
