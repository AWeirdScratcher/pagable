try:
    from .cli import main
except ImportError:
    exit("Please treat me as a module (-m)")

if __name__ == '__main__':
    main()
