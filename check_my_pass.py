import requests
import hashlib
import sys


# request our data and give response
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code},check API and try again')
    return res


# response.txt gives us list of tails starting with our first5_char
def read_res(response):
    print(response.text)


def get_password_leaks_count(response, response_to_check):
    response = (line.split(':') for line in response.text.splitlines())
    for r, count in response:
        if r == response_to_check:
            return count


def pwned_api_check(password):
    # check password if exists in API response

    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


# ability to print out result of above functions
def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times.... you should change the password')
        else:
            print(f'{password} was not found... carry on!')


if __name__ == '__main__':
    main(sys.argv[1:])
