# Drake Equation Python Package

This Python package provides an implementation of the Drake Equation, which estimates the number of transmitting societies in the Milky Way galaxy. The Drake Equation takes several factors into account to calculate an estimate, including the rate of star formation, the fraction of stars with planetary systems, the number of planets with an environment suitable for life per solar system, the fraction of suitable planets where life actually appears, the fraction of life-bearing planets where intelligent life emerges, the fraction of civilizations that develop detectable signs of their existence, and the average length of time such civilizations produce such signs.

## Installation

To install the package, simply run the following command:

```
pip install drake-eq
```

## Usage

To use the Drake Equation package, follow these steps:

1. Import the `Equation` class from the `drake_eq.equation`:

    ```python
    from drake_eq.equation import Equation
    ```

2. Create an instance of the `Equation` class with optional parameter values:
    ```python
    drake_equation = Equation(Rstar=10, fp=0.5, ne=2, fe=1, fi=0.01, fc=0.01, L=10_000)
    ```
3. Estimate the number of technologically advanced civilizations:
    ```python
     result = drake_equation.estimate()
    ```
4. Print the result:
    ```python
     print(f"The estimated number of technologically advanced civilizations is: {result}")
    ```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository of this package.

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
