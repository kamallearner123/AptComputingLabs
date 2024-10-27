
#include <iostream>
#include <vector>
#include <map>

using namespace std;

void solution(vector<int> arr) {

	map<int,int> table;
	int max, temp, x=arr.size()-1;
	vector<int> maxs;

	while(x>=0) { //Sequence of sub-problems for index: 6 5 4 3 2 1
		cout << "Calculating for "<< arr[x] << endl;
		max = arr[x];	
		
		for (int i=x+1; i<arr.size(); i++) { // 6
			cout << "x = " << x <<  endl;
			if (arr[x]<arr[i])
			{
				auto subprob = table.find(arr[i]);
				max = arr[x] + subprob->second;
				maxs.push_back(max);
			}
		
		}
		
		// Adding result of sub problem
		auto value = std::max_element(maxs.begin(), maxs.end());
		table[arr[x]] = *value;
		cout << "Solution for " << arr[x] << " =" << *value << endl;
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
	vector<int> v1 = {3,1,8,2,5,10,20};
	solution(v1);	
}

