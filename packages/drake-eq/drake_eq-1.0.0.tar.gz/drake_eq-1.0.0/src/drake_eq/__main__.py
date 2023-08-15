from equation import Equation


def main():
    drake_equation = Equation()
    result = drake_equation.estimate()
    return result


if __name__ == "__main__":
    main()
