# CS480_Group_Project

---

**Managers**

1. Someone has the option to register as a manager adding their information (name, ssn,
email). If someone is registered as a manager should be able to login using their ssn. (DONE)

2. Managers should be able to insert or remove cars or models in the system. (DONE)

3. Managers should be able to insert or remove drivers from the system along with their
information such as name, and address. (DONE)

4. Managers should be able to give as input a number k and the system should return
the names and emails of the top-k clients with respect to the number of rents they
have booked.

5. Managers should be able to generate a list containing every current car model and
next to it the number of rents it has been used.

6. Similarly, they should be able to generate a list containing for every current driver
in the system X: the name of X, total number of rents that X was the driver and the
average rating of X.

7. A manager should be able to give as input a city C1 and a city C2 and the system
should return the name and email of the clients who have at least one address from
city C1 and they have booked a rent having a driver with an address from city C2.

8. (only groups of four) Managers should be able to report the names of (current)
problematic local drivers. These are current drivers with average rating less than 2.5,
whose address is in city ’Chicago’, and drove in at least two rents booked by two
clients who have at least one address from ’Chicago’.

9. (only groups of four) Managers should be able to report a list containing i) the brand
of a car, ii) the average review ratings given to drivers who can drive at least one
model by that brand, and iii) the number of rents that used a model by that brand.

---

**Drivers**

Drivers login with their name.
1. Drivers should be able to change their address if they want.
2. Drivers should be able to see the list of all car models.
3. They should also be able to declare what car models they can drive.

**Clients**

1. When a new client registers they should add their information (name, and email
address). Furthermore, they insert their address(es) and credit card(s). Notice that a
client might have an address X but some credit card with a payment address Y which
is not the same as X. If a client is registered in the system, then the client can login to
the system using their email.

2. A client should be able to give as input a date D, and see the list of each available
(current) car models on D. A car model X is available on D if: i) X is not used at
another rent on the same date D, ii) there exists at least one driver R who can drive X,
and iii) driver R does not drive on another rent that date D.

3. A client should be able to book a rent with an available car model on a specific date.
The system automatically assigns any arbitrary available driver who can drive the
requested car model. If there is no available car model on thar date the system should
return an error message to the user.

4. A client should be able to see a list of all rents that the client has booked, along with
the car model and the assigned driver.

5. The user should be able to enter a review to a driver (that currently exists in the
system). The system should check whether the driver has been assigned to a rent
booked by the client. Otherwise, the system should not allow user to enter a review.

6. (only groups of 4) A client should have the option to book a rent with an available
specific car model with the best driver. If the client chooses this option then the system
automatically assigns the driver in the rent with the highest average rating among the
available drivers who can drive the requested available car model.
