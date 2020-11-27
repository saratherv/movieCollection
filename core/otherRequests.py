from movieCollection.settings.base import credy_password, credy_username
import requests, json


def retry(times, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    attempt += 1
            return func(*args, **kwargs)
        return newfn
    return decorator


@retry(times=3, exceptions=(ValueError, TypeError, Exception))
def fetchMovies(page):
    url = f"https://demo.credy.in/api/v1/maya/movies/?page={page}"
    response = requests.get(url=url, auth=(credy_username, credy_password))
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        raise ValueError('response code is not 200')
        # return Response(data, status=status.HTTP_200_OK)
