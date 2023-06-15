import timeit


# run same code 5 times to get measurable data
n = 1000

# calculate total execution time
result = timeit.timeit(stmt="test()", globals=globals(), number=n)

# calculate the execution time
# get the average execution time
print(f"Execution time is {result / n} seconds")
