from requests import get

url = 'https://csec.rit.edu'


def main():
    webpage = get(url)
    print(webpage)


if __name__ == '__main__':
    main()
