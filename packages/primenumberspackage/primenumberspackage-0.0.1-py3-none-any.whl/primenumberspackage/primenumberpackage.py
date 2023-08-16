class PrimeNumbersRange:
    # Finds prime numbers in a given range
    def __init__(self):
        self.minimum_number = 0
        self.maximum_number = 0

    def minimum(self):
        # Asks for the minimum number
        while True:
            try:
                self.minimum_number = int(input("Minimum number: "))
                if self.minimum_number >= 1:
                    break
                else:
                    print("The minimum number must be greater than or equal to 1.")
            except ValueError:
                print("Invalid input! Please enter a valid INTEGER.")

    def maximum(self):
        # Asf for maximum number
        while True:
            try:
                self.maximum_number = int(input("Maximum number: "))
                if self.maximum_number > self.minimum_number:
                    break
                else:
                    print("The maximum number must be greater than the minimum number.")
            except ValueError:
                print("Invalid input! Please enter a valid INTEGER.")

    def find_prime_numbers(self):
        # Finds prime numbers in the range [minimum_number, maximum_number]
        for i in range(self.minimum_number, self.maximum_number + 1):
            rest = 0
            for j in range(2, i):
                if i % j == 0:
                    rest += 1
            if rest == 0:
                print(i)


def main():
    while True:
        prime_numbers = PrimeNumbersRange()

        prime_numbers.minimum()
        prime_numbers.maximum()

        prime_numbers.find_prime_numbers()
        option = input(
            """
            If you want to quit press Q.
            If you want to run it again press any other key.
            """
        ).upper()
        if option == "Q":
            break


if __name__ == "__main__":
    main()
