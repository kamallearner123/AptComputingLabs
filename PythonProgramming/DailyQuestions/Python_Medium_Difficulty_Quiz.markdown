# Interactive Python Quiz: Medium Difficulty (Variables, Loops, Dictionaries, Sets)

---

## Question 1: Variable Scope
What is the output of the following code?
```python
x = 10
def func():
    x = 20
    print(x)
func()
print(x)
```
**Options**:  
A) 20 10  
B) 10 20  
C) 20 20  
D) Error  

---

## Question 2: Mutable Variables
What is the output of the following code?
```python
def modify(lst):
    lst.append(4)
numbers = [1, 2, 3]
modify(numbers)
print(numbers)
```
**Options**:  
A) [1, 2, 3]  
B) [1, 2, 3, 4]  
C) [4]  
D) Error  

---

## Question 3: For Loop with Step
What is the output of the following code?
```python
for i in range(1, 6, 2):
    print(i, end=" ")
```
**Options**:  
A) 1 3 5  
B) 1 2 3 4 5  
C) 2 4 6  
D) Error  

---

## Question 4: While Loop with Break
What is the output of the following code?
```python
count = 0
while count < 5:
    count += 1
    if count == 3:
        break
    print(count, end=" ")
```
**Options**:  
A) 1 2  
B) 1 2 3  
C) 0 1 2  
D) Error  

---

## Question 5: List Modification
What is the output of the following code?
```python
lst = [1, 2, 3]
lst[1:2] = [4, 5]
print(lst)
```
**Options**:  
A) [1, 4, 5, 3]  
B) [1, 2, 3, 4, 5]  
C) [4, 5, 3]  
D) Error  

---

## Question 6: List Slicing with Negative Indices
What is the output of the following code?
```python
lst = [10, 20, 30, 40, 50]
print(lst[-3:-1])
```
**Options**:  
A) [20, 30]  
B) [30, 40]  
C) [40, 50]  
D) Error  

---

## Question 7: Dictionary Key Access
What is the output of the following code?
```python
d = {"a": 1, "b": 2, "c": 3}
print(d.get("b", 0) + d.get("d", 0))
```
**Options**:  
A) 2  
B) 0  
C) 3  
D) Error  

---

## Question 8: Dictionary Comprehension
What is the output of the following code?
```python
numbers = [1, 2, 3]
d = {x: x**2 for x in numbers}
print(d)
```
**Options**:  
A) {1: 1, 2: 4, 3: 9}  
B) {1: 2, 2: 4, 3: 6}  
C) [1, 4, 9]  
D) Error  

---

## Question 9: Set Operations (Union)
What is the output of the following code?
```python
s1 = {1, 2, 3}
s2 = {3, 4, 5}
print(s1 | s2)
```
**Options**:  
A) {1, 2, 3, 4, 5}  
B) {3}  
C) {1, 2, 4, 5}  
D) Error  

---

## Question 10: Set Difference
What is the output of the following code?
```python
s1 = {1, 2, 3, 4}
s2 = {3, 4, 5}
print(s1 - s2)
```
**Options**:  
A) {1, 2}  
B) {3, 4}  
C) {5}  
D) Error  

---

## Question 11: Function with Mutable Default
What is the output of the following code?
```python
def add_item(item, lst=[]):
    lst.append(item)
    return lst
print(add_item(1))
print(add_item(2))
```
**Options**:  
A) [1] [2]  
B) [1] [1, 2]  
C) [1, 2] [1, 2]  
D) Error  

---

## Question 12: Nested Function
What is the output of the following code?
```python
def outer():
    x = 5
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()
print(outer())
```
**Options**:  
A) 5  
B) 6  
C) Error  
D) None  

---

## Question 13: Conditional with List
What is the output of the following code?
```python
numbers = [1, 2, 3, 4]
if len(numbers) > 3:
    numbers.pop()
print(numbers)
```
**Options**:  
A) [1, 2, 3]  
B) [1, 2, 3, 4]  
C) [4]  
D) Error  

---

## Question 14: Nested Loops with Condition
What is the output of the following code?
```python
for i in range(2):
    for j in range(3):
        if j == 1:
            continue
        print(f"{i}{j}", end=" ")
```
**Options**:  
A) 00 02 10 12  
B) 01 11  
C) 00 01 02 10 11 12  
D) Error  

---

## Question 15: List Comprehension with Condition
What is the output of the following code?
```python
numbers = [1, 2, 3, 4, 5]
evens = [x for x in numbers if x % 2 == 0]
print(evens)
```
**Options**:  
A) [1, 3, 5]  
B) [2, 4]  
C) [2, 4, 5]  
D) Error  

---

## Question 16: Dictionary Iteration
What is the output of the following code?
```python
d = {"a": 1, "b": 2}
for k, v in d.items():
    print(f"{k}{v}", end=" ")
```
**Options**:  
A) a1 b2  
B) ab 12  
C) 1 2  
D) Error  

---

## Question 17: Set Comprehension
What is the output of the following code?
```python
numbers = [1, 2, 2, 3]
s = {x**2 for x in numbers}
print(s)
```
**Options**:  
A) {1, 4, 9}  
B) {1, 4, 4, 9}  
C) [1, 4, 9]  
D) Error  

---

## Question 18: Loop with Else
What is the output of the following code?
```python
for i in range(3):
    if i == 5:
        break
else:
    print("Done")
```
**Options**:  
A) Done  
B) Nothing  
C) Error  
D) 0 1 2  

---

## Question 19: Dictionary with List Values
What is the output of the following code?
```python
d = {"nums": [1, 2, 3]}
d["nums"].append(4)
print(d["nums"])
```
**Options**:  
A) [1, 2, 3]  
B) [1, 2, 3, 4]  
C) [4]  
D) Error  

---

## Question 20: Unpacking in Loop
What is the output of the following code?
```python
pairs = [(1, "a"), (2, "b")]
for num, letter in pairs:
    print(f"{num}{letter}", end=" ")
```
**Options**:  
A) 1a 2b  
B) 12 ab  
C) (1, "a") (2, "b")  
D) Error  

---

## Answers
To keep the quiz interactive, here are the answers. Try to solve each question before checking!

1. A) 20 10  
2. B) [1, 2, 3, 4]  
3. A) 1 3 5  
4. A) 1 2  
5. A) [1, 4, 5, 3]  
6. B) [30, 40]  
7. A) 2  
8. A) {1: 1, 2: 4, 3: 9}  
9. A) {1, 2, 3, 4, 5}  
10. A) {1, 2}  
11. B) [1] [1, 2]  
12. B) 6  
13. A) [1, 2, 3]  
14. A) 00 02 10 12  
15. B) [2, 4]  
16. A) a1 b2  
17. A) {1, 4, 9}  
18. A) Done  
19. B) [1, 2, 3, 4]  
20. A) 1a 2b  

---

**How to Use This Quiz**:  
- Read each code snippet and try to predict the output.  
- Select the correct option from the choices provided.  
- Check your answers at the end to see how you did!  
- For a deeper understanding, try running the code snippets in a Python environment to verify the outputs.

Enjoy testing your Python skills!
