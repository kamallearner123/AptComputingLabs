/*
Concepts: Vector, Vector of vectors
1) Return vector of vectors
*/


struct Solution;
impl Solution {
    pub fn four_sum(nums: Vec<i32>, target: i32) -> Vec<Vec<i32>> {
        let mut arrays:Vec<Vec<i32>> = Vec::new();
        arrays.push(vec![1,2,3]);

        if nums.len() < 4 {
            println!("Array is empty");
            return arrays;
        }

        return arrays;
    }
}

/*
Wrting macro
*/
macro_rules! print_vec {
    ($vec:expr) => {
        for element in $vec.iter() {
            println!("{:?}", element);
        }
    }
}


fn main() {
    let myVec = vec![3,5,2,1,8,9,0,2,11];
    let mut result = Solution::four_sum(myVec, 18);

    print_vec!(result);
}

