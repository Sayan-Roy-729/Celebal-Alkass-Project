import datetime

def timeConversion(s):
    time = datetime.datetime.fromtimestamp(int(s)).strftime('%Y-%m-%d %H:%M:%S')
    return time

if __name__ == '__main__':
    s = "1691315584"
    result = timeConversion(s)
    print(result)
