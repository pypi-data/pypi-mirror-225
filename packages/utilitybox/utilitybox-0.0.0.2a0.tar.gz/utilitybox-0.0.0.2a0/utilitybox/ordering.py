import random

def random_number_list(number_elements: int, min=0, max=100):
    """
    The function `random_number_list` generates a list of random numbers within a specified range.
    
    Args:
      number_elements (int): The number of elements you want in the random number list.
      min: The minimum value that can be generated in the random number list. The default value is 0 if
    no value is provided. Defaults to 0
      max: The maximum value that can be generated in the random number list. By default, it is set to
    100. Defaults to 100
    
    Returns:
      a list of random numbers. The number of elements in the list is determined by the
    "number_elements" parameter. The minimum and maximum values for the random numbers can be specified
    using the "min" and "max" parameters, with default values of 0 and 100 respectively.
    """
    return [random.randint(min, max) for _ in range(number_elements)]

def bubble_sort(data: list):
    """
    The bubble_sort function takes a list of numbers and sorts them in ascending order using the bubble
    sort algorithm.
    
    Args:
      data (list): The parameter `data` is a list of numbers that you want to sort using the bubble sort
    algorithm.
    
    Returns:
      the sorted list in ascending order.
    """
    all_cleanded = True
    range_valid = len(data) - 1
    while all_cleanded:
        start, end = 0, 1
        all_cleanded = False
        for _ in range(range_valid):
            first_number, last_number  = data[start], data[end]
            if first_number > last_number:
                data[start], data[end] = last_number, first_number
                all_cleanded = True
            start, end = start + 1, end + 1
    return data
     
def selection_sort(data: list):
  ...


if __name__ == '__main__':
    data = random_number_list(20000)
    bubble = bubble_sort(data)
    print(bubble)
    selection = selection_sort(data)
    print(selection)
    