from datetime import datetime, timedelta
from enum import Enum
import random
from collections import deque


# Random content of the posts
class PostContent(Enum):
    ANNOUNCEMENT = "Exciting announcement!"
    QUESTION = "What's your favorite color?"
    INSPIRATIONAL_QUOTE = "Always believe in yourself."
    FUNNY_JOKE = "Why don't scientists trust atoms? Because they make everything!"

# Random authors
class Author(Enum):
    HAMAD = "Hamad"
    Rashed = "Rashed"
    Ahmed = "Ahmed"
    Khaled = "Khaled"
    Badr = "Badr"

class SocialMediaPost:
    """A class that represents the posts in social media"""

    # Constructor
    def __init__(self, post_datetime, post_content, author, views):
        self.post_datetime = post_datetime  # Unique datetime value representing when the post was made
        self.post_content = post_content    # The content of the post
        self.author = author                # The person who posted the content
        self.views = views

    def __str__(self):
        return f"Post by {self.author} at {self.post_datetime}:\n{self.post_content} and gained {self.views} viewers."

# A function to generate any number of posts randomly in a specific range of dates
def generate_random_posts(num_posts, start_date):
    posts = []  # empty list to store the objects
    current_date = start_date  # initialize current date
    time_step = timedelta(hours=2)  # the time step to increment datetime,
                                    # this ensures that each post has a unique time

    for i in range(num_posts):
        post_datetime = current_date  # use current date for post datetime
        current_date += time_step  # increment current date by time step
        post_content = random.choice(list(PostContent)).value  # choose random content
        author = random.choice(list(Author)).value  # choose random authors
        views = random.randint(1000, 10000)  # choose random number of viewers
        post = SocialMediaPost(post_datetime, post_content, author, views)  # make the object
        posts.append(post)  # add it to the list
    return posts


class HashTable:
    """ A class that is used to create a hash table
     and order the posts based on the unique date"""

    # Constructor
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    # A function that assigns a value for the post based on the unique date
    def hash_function(self, post_datetime):
        return hash(post_datetime) % self.size

    # A function that inserts the post in the table based on its value
    def insert(self, post):
        index = self.hash_function(post.post_datetime)
        self.table[index].append(post)

    # A function that searches for the desired post through its date efficiently
    def search(self, target_datetime):
        index = self.hash_function(target_datetime)
        for post in self.table[index]:
            if post.post_datetime == target_datetime:
                return post
        return None

class TreeNode:
    def __init__(self, post):
        self.post = post
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, post):
        self.root = self.insert_recursive(self.root, post)

    def insert_recursive(self, node, post):
        if node is None:
            return TreeNode(post)
        if post.post_datetime < node.post.post_datetime:
            node.left = self.insert_recursive(node.left, post)
        else:
            node.right = self.insert_recursive(node.right, post)
        return node

    def search_in_range(self, start_datetime, end_datetime):
        posts_in_range = []
        self.search_in_range_recursive(self.root, start_datetime, end_datetime, posts_in_range)
        return posts_in_range

    def search_in_range_recursive(self, node, start_datetime, end_datetime, result):
        if node is None:
            return
        if start_datetime <= node.post.post_datetime <= end_datetime:
            result.append(node.post)
        if start_datetime < node.post.post_datetime:
            self.search_in_range_recursive(node.left, start_datetime, end_datetime, result)
        if end_datetime > node.post.post_datetime:
            self.search_in_range_recursive(node.right, start_datetime, end_datetime, result)

class MaxHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def insert(self, post):
        self.heap.append(post)
        self.sift_up(len(self.heap) - 1)

    def sift_up(self, i):
        while i > 0 and self.heap[self.parent(i)].views < self.heap[i].views:
            self.heap[self.parent(i)], self.heap[i] = self.heap[i], self.heap[self.parent(i)]
            i = self.parent(i)

    def extract_max(self):
        if len(self.heap) == 0:
            return None
        max_post = self.heap[0]
        self.heap[0] = self.heap[-1]
        del self.heap[-1]
        self.sift_down(0)
        return max_post

    def sift_down(self, i):
        max_index = i
        left = self.left_child(i)
        if left < len(self.heap) and self.heap[left].views > self.heap[max_index].views:
            max_index = left
        right = self.right_child(i)
        if right < len(self.heap) and self.heap[right].views > self.heap[max_index].views:
            max_index = right
        if i != max_index:
            self.heap[i], self.heap[max_index] = self.heap[max_index], self.heap[i]
            self.sift_down(max_index)

# A function that prioritize the posts based on the view count using heapsort
def heap_sort(posts):
    max_heap = MaxHeap()
    for post in posts:
        max_heap.insert(post)
    sorted_posts = []
    while len(max_heap.heap) > 0:
        sorted_posts.append(max_heap.extract_max())
    return sorted_posts









# Test cases
""" Random Generator """
# Generate 5 posts randomly and print them
start_date = datetime(2024, 4, 1)  # Start date
random_posts = generate_random_posts(5, start_date)
print("The generated posts:")
for i, post in enumerate(random_posts, 1):
    print(f"{i}. {post}")

print("-------------------------------------------------------------------")

""" Hash Table"""
hash_table = HashTable(size=10)  # Choose an appropriate size for the hash table

# Insert posts into the hash table
for post in random_posts:
    hash_table.insert(post)

# Search for a post by datetime
target_datetime = random_posts[2].post_datetime  # Assume we want to find the third post by its datetime
found_post = hash_table.search(target_datetime)
if found_post:
    print(f"The post with the date {target_datetime} is found:")
    print(found_post)
else:
    print("Post not found.")

print("-------------------------------------------------------------------")

""" Binary Search Tree"""
BST = BinarySearchTree()

# Insert posts into the BST
for post in random_posts:
    BST.insert(post)

# Define start and end datetime for the search range
start_datetime = datetime(2024, 4, 1, 6, 0)  # Start datetime
end_datetime = datetime(2024, 4, 1, 12, 0)   # End datetime

# Search for posts within the specified time range
posts_in_range = BST.search_in_range(start_datetime, end_datetime)

# Print the posts found within the time range
print("Posts within the specified time range:")
for i, post in enumerate(posts_in_range, 1):
    print(f"{i}. {post}")

print("-------------------------------------------------------------------")

""" Heap and HeapSort"""
# Sort posts by number of views using heap sort
sorted_posts = heap_sort(random_posts)

# Retrieve the post with the most views
most_viewed_post = sorted_posts[0]
print("Post with the most views:")
print(most_viewed_post)
print("")
print("Posts ordered based on views:")
for i, post in enumerate(sorted_posts, 1):
    print(f"{i}. {post}")