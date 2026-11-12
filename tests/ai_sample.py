def calculate_average(numbers):
    """Calculate the arithmetic mean of a collection."""
    if not numbers:
        return 0

    total_sum = sum(numbers)
    count = len(numbers)

    return total_sum / count


sample_numbers = [10, 20, 30, 40]
result = calculate_average(sample_numbers)
print(f"Average: {result}")