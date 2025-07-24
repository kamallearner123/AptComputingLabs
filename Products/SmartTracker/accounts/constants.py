from enum import Enum

# Roles for employees
ROLE_CHOICES = [
        ('Service Advisor', 'Service Advisor'),
        ('Technician', 'Technician'),
        ('Representative', 'Representative'),
        ('Workshop Manager', 'Workshop Manager'),
        ('Account Staff', 'Account Staff')
    ]

# Status transition
STATUS_CHOICES = [
    ('Created', 'Created'),
    ('Estimation', 'Estimation'),
    ('Waiting for Customer approval', 'Waiting for Customer approval'),
    ('Customer Rejected', 'Customer Rejected'),
    ('Checking with Customer', 'Checking with Customer'),
    ('Service in progress', 'Service in progress'),
    ('QA Check', 'QA Check'),
    ('Ready for delivery', 'Ready for delivery'),
    ('Customer query', 'Customer query'),
    ('Query resolved', 'Query resolved'),
    ('Waiting for payment', 'Waiting for payment'),
    ('Invoice Paid', 'Invoice Paid'),
    ('Customer feedback', 'Customer feedback'),
    ('Resolved', 'Resolved')
]



# define enum with list of event (constants)
class Event(Enum):
    CREATED = 'Created'
    SENT_ESTIMATION = 'Estimation'
    RECEIVED_CONFORMATION_ON_ESTIMATION = 'Waiting for Customer approval'
    START_WORK = 'Start work'
    RECEIVED_REJECTION_ON_ESTIMATION = 'Customer Rejected'
    CLEARED_CUSTOMER_QUERY = 'Query resolved'
    RECEIVED_CHANGE_IN_ESTIMATION = 'Customer query'
    CHECKING_WITH_CUSTOMER = 'Checking with Customer'
    WORK_FINISHED = 'Finished'
    SENT_INVOICE = 'Ready for delivery'
    RECEIVED_PAYMENT = 'Waiting for payment'
    RECEIVED_PAYMENT_REJECTION = 'Customer query'
    DELIVERED = 'Delivered'
    RECEIVED_CUSTOMER_FEEDBACK = 'Customer feedback received'
    UNKNOWN = 'Unknown'
