def binarySearch():
    def binarySearch(arr, target):
        low = 0
        high = len(arr) - 1

        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

        return -1
    
    arr = list(range(200, 0, -1))
    target = 42
    result = binarySearch(arr, target)
    print(f"Target {target} found at index {result}" if result != -1 else "Target not found")