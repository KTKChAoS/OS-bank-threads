import random
from queue import Queue, Empty
from random import randint
from threading import Semaphore, Thread, Lock
from time import sleep

max_customers = 100  # number of customers that will go to the bank today
manager = Semaphore(1)
printLock = Lock()
safe = Semaphore(2)
teller_sem = Semaphore(3)
teller_avail = ['-1', '-1', '-1']


class Customer:
    def __init__(self, _name):
        self.trans = None
        self.name = _name

    def setTrans(self, _trans):
        self.trans = _trans

    def getTrans(self):
        return f"{self.trans}"

    def __str__(self):
        return f"{self.name}"


class Teller:
    def __init__(self, _name):
        self.name = _name

    def __str__(self):
        return f"{self.name}"


def bankprint(msg):
    """
    Print commands with lock
    Args:
        msg: string
    Returns:
        None
    """
    printLock.acquire()
    try:
        print(msg)
    finally:
        printLock.release()


def customer_pool(customer, teller_line):
    """
    Thread function for Customer
    Args:
        customer: Customer object
        teller_line: Queue
    Returns:
        None
    """
    r = randint(0, 1)
    trans = ''
    if r == 0:
        trans = 'deposit'
        bankprint(f"{customer} wants to perform a deposit transaction")
    else:
        trans = 'withdrawal'
        bankprint(f"{customer} wants to perform a withdrawal transaction")
    customer.setTrans(trans)
    sleep(random.uniform(0, 2.5))
    bankprint(f"{customer} is going to the bank")
    try:
        bankprint(f"{customer} is getting in line")
        teller_sem.acquire()
        bankprint(f"{customer} is selecting a teller.")

        if teller_avail[0] == '-1':
            teller_avail[0] = customer
            bankprint(f"{customer} goes to Teller 1.")
        elif teller_avail[1] == '-1':
            teller_avail[1] = customer
            bankprint(f"{customer} goes to Teller 2.")
        elif teller_avail[2] == '-1':
            teller_avail[2] = customer
            bankprint(f"{customer} goes to Teller 3.")

        teller_line.put(customer)
    except Exception as Error:
        print("Cannot put {customer} into line " + str(Error))


def teller_job(teller, teller_line):
    """
    Thread method for Teller
    Args:
        teller: Teller object
        teller_line: Queue
    Returns:
        None
    """
    tel = teller.name
    t_num = int(tel[7:8])

    bankprint(f"{tel} is ready to serve.")
    while True:
        try:
            bankprint(f"{tel} is waiting for a customer.")
            customer = teller_line.get(timeout=2)
            bankprint(f"{customer} introduces itself to {tel}.")
            bankprint(f"{tel} is serving {customer}")
            bankprint(f"{customer} asks for a {customer.getTrans()} transaction.")
            bankprint(f"{tel} is handling the {customer.getTrans()} transaction.")
            if customer.trans == 'withdrawal':
                bankprint(f"{tel} is going to the manager")
                manager.acquire()
                bankprint(f"{tel} is getting the manager's permission")
                sleep(random.uniform(0.05, 0.3))
                bankprint(f"{tel} has got the manager's permission")
                manager.release()
            bankprint(f"{tel} is going to the safe.")
            safe.acquire()
            bankprint(f"{tel} is in the safe.")
            sleep(random.uniform(0.1, 0.5))
            bankprint(f"{tel} is leaving the safe.")
            safe.release()
            bankprint(f"{tel} finishes {customer}'s {customer.getTrans()} transaction.")
            bankprint(f"{customer} thanks {tel} and leaves")
            teller_avail[t_num-1] = '-1'
            teller_sem.release()

        except Empty:
            bankprint(f"{tel} is leaving for the day")
            break


if __name__ == '__main__':
    teller_line = Queue()

    tellers = [Teller("Teller " + str(i)) for i in range(1, 4)]
    tellers_list = [Thread(name=f"tellers[i]", target=teller_job, args=(tellers[i], teller_line)) for
                    i in range(0, len(tellers))]
    for teller in tellers_list:
        teller.start()

    customers = [Customer("Customer " + str(i)) for i in range(1, max_customers + 1)]
    customers_list = [Thread(name=f"customers[i]", target=customer_pool, args=(customers[i], teller_line)) for
                      i in range(0, len(customers))]

    for cust in customers_list:
        cust.start()

    for teller in tellers_list:
        teller.join()

    bankprint("Bank is closing for the day")
