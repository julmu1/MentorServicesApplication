customers = Customer.objects.all()

firstCustomer = Customer.objects.first()

lastCustomer = Customer.objects.last()

customerByName = Customer.objects.get(name= 'Seth Murphy')

customerById = Customer.objects.get(id=4)

firstCustomer.order_set.all()

order = Order.objects.first()
parentName = order.customer.name

courses = Courses.objects.filter(category = 'dev')

leastToGreatest = Courses.objects.all().order_by('id')
greatestToLeast = Courses.objects.all().order_by('_id')

coursesFiltered = Courses.objects.filter(tags_name="")