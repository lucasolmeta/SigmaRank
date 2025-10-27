from scripts import fetch
from scripts import build_features

def main():
    fetch.main()

    build_features.main()

if __name__ == '__main__':
    main() 