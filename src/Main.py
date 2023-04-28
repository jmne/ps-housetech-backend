import argparse

from src.backend.Example import fibonacci_recursive


def main():
    """Build main function.

    Parses arguments and calculates the nth fibonacci number.

    Args:
        -n, --number: number to calculate fibonacci number for
        -r, --recursive: calculate fibonacci number recursively

    """
    # create parser
    parser = argparse.ArgumentParser(description='Fibonacci number calculator')

    # add arguments
    parser.add_argument(
        '-n',
        '--number',
        type=int,
        help='number to calculate fibonacci number for',
        required=True,
    )
    parser.add_argument(
        '-r',
        '--recursive',
        help='calculate fibonacci number recursively',
        action='store_true',
    )

    # parse arguments
    args = parser.parse_args()

    # get argument values
    n = args.number
    recursive = args.recursive

    # calculate fibonacci number
    if recursive:
        fib = fibonacci_recursive(n)
    else:
        print('No method selected, using recursive method by default.')
        fib = fibonacci_recursive(n)
    print(f'The {n}th fibonacci number is {fib}.')


if __name__ == '__main__':
    main()
