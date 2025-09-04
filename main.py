from data import fetch
from data import preprocess
from model import model
from model import evaluate

def main():
    #if market open then skip
    #else
    fetch.main()

    preprocess.main()

    model.main()

    evaluate.main()

    print('Code completed successfully!')

if __name__ == '__main__':
    main() 