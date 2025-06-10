from data import fetch
from data import preprocess
from model import model

def main():
    fetch.main()
    print('DATA OBTAINED')

    preprocess.main()
    print('PREPROCESSING COMPLETE')

    model.main()
    print('TRAINING COMPLETE')

if __name__ == '__main__':
    main() 