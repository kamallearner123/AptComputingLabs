
struct Solution;
impl Solution {
    pub fn longest_common_prefix(strs: Vec<String>) -> String {
        let mut fina_index = 0;
        if strs.len() == 0 {
            return String::from("");
        }

        //1) Find min len among all the strings
        let mut min_len = strs[0].len();
        for index in 1..strs.len() {
            if min_len > strs[index].len() {
                min_len = strs[index].len()
            }
        }

        //2) Find common prefix
        'outer: for index in 0..min_len { // 0,1,2,3,4
            for j in 1..strs.len() { // all strings except first
                if  strs[j].chars().nth(index) != strs[0].chars().nth(index) {
                    break 'outer;
                }
            }
            fina_index += 1;
        }
        let result : &str = &strs[0][0..fina_index];
        return result.to_string();
    }
}
fn main() {
    let names: Vec<String> = vec!["kamal".to_string(), "kamil".to_string()];
    let result = Solution::longest_common_prefix(names);
    println!("{}", result);
}