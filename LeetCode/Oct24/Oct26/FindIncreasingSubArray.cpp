
#include <iostream>
#include <vector>
#include <map>
#include <algorithm> 
using namespace std;

void solution(vector<int> arr) {

	map<int,int> table;
	int max, temp, x=arr.size()-1;
	int best_index = x;
	int best_max = arr[x];

	vector<int> maxs;

	// 1) Filling last element 20, max sum is 20 as there is not successive number
	table[arr[x]] = arr[x];
	x -= 1;

	while(x>=0) { // 2) Sequence of sub-problems for index: 5 4 3 2 1
		max = arr[x];	
		maxs.push_back(max);

		// 3) Check the combination with successive combinations
		for (int i=x+1; i<arr.size(); i++) { // 6
			if (arr[x]<arr[i])
			{
				auto subprob = table.find(arr[i]);
				max = arr[x] + subprob->second;
				maxs.push_back(max); // Add all possible numbers
			}
		
		}
		
		// 4) Adding result of each sub problem to map
		auto value = std::max_element(maxs.begin(), maxs.end());
		table[arr[x]] = *value;
		cout << "Solution for " << arr[x] << " =" << *value << endl;

		if (best_max<*value) {
			best_max = *value;
			best_index = x;
		}
		// Go to next sub-problem
		x--;
		maxs.clear();
	}
	/*
	 * 20 - 20
	 * 10 - 30
	 * 5 - 5, 5->5+table[10]=35, 5+table[20]=25 
	 */

}


int main() {
	vector<int> v1 = {3,1,8,2,5,4,5};
	solution(v1);
}

