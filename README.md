### Diagrama de Clases

```mermaid
classDiagram
    class Concert {
        +Integer id
        +String name
        +DateTime date
        +String location
        +String description
        +ImageField image
        +String __str__()
    }

    class Ticket {
        +Integer id
        +Concert concert
        +String seat_number
        +User owner
        +Decimal price
        +Boolean is_sold
        +FileField pdf_file
        +String __str__()
        +save(*args, **kwargs)
    }

    class ShoppingCart {
        +Integer id
        +User user
        +ManyToManyField tickets
        +String __str__()
    }

    class Transaction {
        +Integer id
        +Ticket ticket
        +User buyer
        +User seller
        +DateTime date
        +Decimal amount
        +String __str__()
    }

    class User {
        <<from django.contrib.auth.models>>
    }

    Concert "1" --> "*" Ticket : tickets
    Ticket "1" --> "1" User : owner
    ShoppingCart "1" --> "1" User : user
    ShoppingCart "1" --> "*" Ticket : tickets
    Transaction "1" --> "1" Ticket : ticket
    Transaction "1" --> "1" User : buyer
    Transaction "1" --> "1" User : seller
