# OS-bank-threads
OS class project 2 on threads - bank teller, customers
main.py - this the is python file with all the code, and the only file needed to run the project.
output.txt - one of the outputs with 100 customers

How to run the program
USE PYTHON3

The program outputs to the console and doesn't take inputs, so running it is fairly simple. Type 'python3 main.py'

You can change the number of customers that come in using the variable defined at line 7 (max_customers)
#
Writeup:

I first started the project by adding functionality of teller and customer. I only had 10 customers and 3 tellers, and the only functionality I added was that the customer is added to a queue and the teller takes the customer from the queue. Then the teller sleeps for a random amount of time and the transaction is done. Then I added in the functionality of the customer choosing a transaction, and conveying it to the teller. Then I added in the manager and safe semaphores, which was only a couple lines each.

Some problems I faced were when using the print function normally. It sometimes couldn't print the whole line and got cut off by another thread's print function. To solve this, I added in a printlock Lock and created a bankprint() function which uses the threading module to lock and ensure that the function is run to completion before releasing the lock.
Another issue was I didnt know how to make the customer choose the teller instead of the other way around. I solved this by creating an array of size 3 and a semaphore. whenever the customer can acquire the semaphore, it means one of the tellers is free, and the customer sets the appropriate value in the array to its name.

I learned a lot about threads from this project. I had no idea how to start at first and by the end adding in the manager and safe functionality felt super easy.
