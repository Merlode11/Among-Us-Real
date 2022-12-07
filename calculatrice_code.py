def fonction(n: float) -> float:
    return fonction2(5 / 3) * n + fonction2(0)


def fonction2(n: float) -> float:
    return 30 * n - 20


def check(gess: list, encoded_found: list):
    for i in range(len(gess)):
        gess[i] = int(gess[i])
        if fonction(gess[i]) != encoded_found[i]:
            print("Code incorrect.\n" + str(3 - i), "essais restant")
            return False
    print("Gagne !\nEnvoyez \"chapelure\"\na l'organisateur.ice !")
    return True


def main():
    encoded_found = [40, 10, 70, -20]
    for i in range(3):
        gess = input("Proposition " + str(i + 1) + ": ")
        gess = list(gess)
        if len(gess) != len(encoded_found):
            print("Code incorrect.\n" + str(3 - i), "essais restant")
            continue

        if check(gess, encoded_found):
            break


main()
