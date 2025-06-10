from data import fetch
from data import preprocess
from model import model

def main():
    fetch.main()

    preprocess.main()

    model.main()

    print('Model results outputted successfully!')

if __name__ == '__main__':
    main() 