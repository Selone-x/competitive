# Quiz: Binary Search

## Question 1: Conceptual
**Question**: What is the key requirement for using binary search, and why is it necessary?
**Expected Answer**: The array/search space must be monotonic (sorted or have some monotonic property). This is necessary because binary search relies on eliminating half of the search space based on comparisons - if elements aren't ordered, we can't guarantee which half to discard.
**Common Mistakes**: Only mentioning "sorted" without explaining why, or forgetting that monotonicity (not just sorting) is the real requirement.
**Follow-up if wrong**: If you have an unsorted array [5, 1, 9, 3], why can't you binary search for 9?

## Question 2: Application
**Question**: When would you use binary search on answer vs binary search on array?
**Expected Answer**:
- Binary search on array: When you have a sorted array and need to find a specific element
- Binary search on answer: When you need to find an optimal value and can verify if a candidate answer is valid (e.g., "minimum time to complete tasks", "maximum minimum distance")
**Common Mistakes**: Not recognizing binary search on answer opportunities, thinking binary search only works on arrays.
**Follow-up if wrong**: If a problem asks "what's the minimum number of days to ship all packages given capacity limits", what are you searching for?

## Question 3: Code Analysis
**Question**: What's wrong with this binary search implementation?
```cpp
int binary_search(vector<int>& arr, int target) {
    int left = 0, right = arr.size();
    while (left < right) {
        int mid = (left + right) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid;
        else right = mid;
    }
    return -1;
}
```
**Expected Answer**: Infinite loop issue - when `arr[mid] < target`, should be `left = mid + 1` not `left = mid`. Otherwise when `right - left == 1`, left will never advance.
**Common Mistakes**: Not recognizing the infinite loop, or suggesting to change the while condition instead of fixing the update.
**Follow-up if wrong**: Trace through with arr=[1,2,3,4], target=4. What happens when left=3, right=4?

## Question 4: Pattern Recognition
**Question**: You need to split an array into K subarrays such that the maximum sum among subarrays is minimized. What technique applies here?
**Expected Answer**: Binary search on answer. The answer (maximum sum) has a valid range (max element to sum of all elements). For any candidate max sum, we can verify if it's achievable by greedily forming subarrays - if we can form ≤K subarrays, it's valid.
**Common Mistakes**: Trying dynamic programming or greedy without recognizing the monotonic property of valid answers.
**Follow-up if wrong**: If max sum = X works (can split into K subarrays), will max sum = X+1 also work? What does this tell you?

## Question 5: Edge Cases
**Question**: What edge cases should you handle when implementing binary search?
**Expected Answer**:
- Empty array
- Single element array
- Target not found
- Duplicate elements (depending on requirements - first/last occurrence)
- Integer overflow in mid calculation: use `left + (right - left) / 2` instead of `(left + right) / 2`
**Common Mistakes**: Forgetting overflow, not considering what to return when target not found, assuming array always has the target.
**Follow-up if wrong**: What happens if left=2^30 and right=2^30, and you calculate mid = (left + right) / 2 in 32-bit integer?

---

## Scoring Guide
- 5/5: Excellent understanding, ready for practice
- 3-4/5: Good grasp, may need light review
- 1-2/5: Need more study, review materials first
- 0/5: Start from basics
