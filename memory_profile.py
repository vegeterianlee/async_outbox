import psutil
import os

def memory_usage_mb():
    # 현재 프로세스의 메모리 사용량(MB)을 반환
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def count_primes(n: int):
    num_arr = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            num_arr[j] += 1
    prime_count = sum(1 for k in range(2, n + 1) if num_arr[k] == 2)
    return prime_count

if __name__ == '__main__':
    n = 10**7
    mem_before = memory_usage_mb()
    print(f"시작 메모리: {mem_before:.2f} MB")
    prime_count = count_primes(n)
    print(f"count_primes({n}) 결과: {prime_count}")

    mem_after = memory_usage_mb()
    print(f"종료 메모리: {mem_after:.2f} MB")
    print(f"메모리 사용량: {mem_after - mem_before:.2f} MB")
