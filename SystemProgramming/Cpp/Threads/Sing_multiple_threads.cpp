#include <iostream>
#include <vector>
#include <thread>
#include <numeric>
#include <chrono>

// Function to sum a part of the array
void partial_sum(const std::vector<int>& data, size_t start, size_t end, long long& result) {
    result = std::accumulate(data.begin() + start, data.begin() + end, 0LL);
}

int main() {
    const size_t dataSize = 1000000000; // 1 billion elements
    std::vector<int> data(dataSize, 1); // Initialize with all elements as 1

    // Single-threaded sum
    auto start_time = std::chrono::high_resolution_clock::now();
    long long single_thread_result = std::accumulate(data.begin(), data.end(), 0LL);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto single_thread_duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    std::cout << "Single-threaded sum: " << single_thread_result << "\n";
    std::cout << "Time taken by single-threaded sum: " << single_thread_duration.count() << " ms\n";

    // Multi-threaded sum
    size_t num_threads = 50;//std::thread::hardware_concurrency(); // Get number of supported threads
    std::cout << "Maximum tasks supported: " << num_threads << std::endl;
    std::vector<std::thread> threads;
    std::vector<long long> partial_results(num_threads, 0);

    size_t block_size = dataSize / num_threads;

    start_time = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < num_threads; ++i) {
        size_t start = i * block_size;
        size_t end = (i == num_threads - 1) ? dataSize : (i + 1) * block_size;
        threads.emplace_back(partial_sum, std::ref(data), start, end, std::ref(partial_results[i]));
    }

    // Join threads
    for (auto& t : threads) {
        t.join();
    }

    long long multi_thread_result = std::accumulate(partial_results.begin(), partial_results.end(), 0LL);
    end_time = std::chrono::high_resolution_clock::now();
    auto multi_thread_duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);

    std::cout << "Multi-threaded sum: " << multi_thread_result << "\n";
    std::cout << "Time taken by multi-threaded sum: " << multi_thread_duration.count() << " ms\n";

    return 0;
}



// Number of tasks
// Kernel's decision p1-t1
// Priority of tasks
// per process what is the max time slot for which it can run

