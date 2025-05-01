from flask import render_template, request, redirect, url_for
from models import Person, Manager, Car, Model, Driver, Address

def register_routes(app, db):
    # Routing back to the home page
    @app.route('/')
    def index():
        people = Person.query.all()
        return render_template('index.html', people=people)

    @app.route('/login-client', methods=['GET', 'POST'])
    def login_client():
        if request.method == 'POST':
            email = request.form['email']
            
            # Check if the client exists (you can use your database model here)
            client = Person.query.filter_by(email=email).first()
            
            if client:
                # Redirect the client to their dashboard or another page after successful login
                return redirect(url_for('client_dashboard', client_id=client.id))
            else:
                # If the client doesn't exist, show an error message
                return render_template('invalid_credentials.html', role="Client"), 401

        # For GET request, render the login form
        return render_template('login_client.html')

    @app.route('/login-driver',methods=['GET', 'POST'])
    def login_driver():
        print("Driver login route accessed", request.method)
        if request.method == 'POST':
            print("Driver login POST request received")
            name = request.form['name']
        
            # Check if the driver exists
            driver = Driver.query.filter_by(name=name).first()
            
            if driver:
                # Redirect the driver to their dashboard or another page after successful login
                return redirect(url_for('driver_dashboard', driver_id=driver.driverid))
            else:
                # If the driver doesn't exist, show an error message
                return render_template('invalid_credentials.html', role="Driver"), 401

        # For GET request, render the login form
        return render_template('login_driver.html')

    @app.route('/register-client', methods=['GET', 'POST'])
    def register_client():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            address = request.form['address']
            credit_card = request.form['credit-card']

            # Assuming your Person model has name, email, address, and credit_card fields
            new_client = Person(name=name, email=email, address=address, credit_card=credit_card)

            db.session.add(new_client)
            db.session.commit()

            return f"""
                <h2>✅ Client {name} registered successfully!</h2>
                <p><a href="/">Return to Home</a></p>
                <form action="/login-client" method="get">
                    <button type="submit">Login Now</button>
                </form>
            """

        return render_template('register_client.html')


    # Routing to registering a new manager screen
    @app.route('/register-manager', methods=['GET', 'POST'])
    def register_manager():
        if request.method == 'POST':
            name = request.form['name']
            ssn = request.form['ssn']
            email = request.form['email']
            
            new_manager = Manager(name=name, ssn=ssn, email=email)
            db.session.add(new_manager)
            db.session.commit()

            return f"""
                <h2>✅ Manager {name} registered successfully!</h2>
                <form action="/manager-dashboard/{ssn}" method="get">
                    <button type="submit">Continue to Dashboard</button>
                </form>
                <p><a href="/">Return to Home</a></p>
                    """

        return render_template('register_manager.html')
    
    # Logging in as a manager
    @app.route('/login-manager', methods=['GET', 'POST'])
    def login_manager():
        if request.method == 'POST':
            ssn = request.form['ssn']
            manager = Manager.query.filter_by(ssn=ssn).first()
            if manager:
                return redirect(f"/manager-dashboard/{ssn}")
            else:
                return render_template('invalid_credentials.html'), 401
        return render_template('login_manager.html')


    
    # Signing into the Manager dashboard
    @app.route('/manager-dashboard/<ssn>')
    def manager_dashboard(ssn):
        manager = Manager.query.filter_by(ssn=ssn).first()
        if not manager:
            return "Manager not found", 404
        return render_template('manager_dashboard.html', manager=manager)

    # Managing cars and models together for managers
    @app.route('/manage-cars-models', methods=['GET', 'POST'])
    def manage_cars_models():
        ssn = request.args.get('ssn')
        if not ssn:
            return "Missing manager SSN", 400

        if request.method == 'POST':
            form_type = request.form.get('form_type')

            if form_type == 'add_car':
                new_car = Car(
                    carid=request.form['carid'],
                    brand=request.form['brand']
                )
                db.session.add(new_car)
                db.session.commit()

            elif form_type == 'remove_car':
                car = Car.query.get(request.form['carid'])
                if car:
                    db.session.delete(car)
                    db.session.commit()

            elif form_type == 'add_model':
                new_model = Model(
                    carid=request.form['carid'],
                    modelid=request.form['modelid'],
                    color=request.form['color'],
                    construction_year=request.form['construction_year'],
                    transmission=request.form['transmission']
                )
                db.session.add(new_model)
                db.session.commit()

            elif form_type == 'remove_model':
                model = Model.query.get((request.form['carid'], request.form['modelid']))
                if model:
                    db.session.delete(model)
                    db.session.commit()

            return redirect(f"/manage-cars-models?ssn={ssn}")

        cars = Car.query.all()
        return render_template('manage_cars_models.html', cars=cars, manager_ssn=ssn)

    @app.route('/manage-drivers', methods=['GET', 'POST'])
    def manage_drivers():
        ssn = request.args.get('ssn')
        if not ssn:
            return "Missing manager SSN", 400

        if request.method == 'POST':
            form_type = request.form.get('form_type')

            if form_type == 'add_driver':
                # Check and insert address if needed
                street = request.form['street']
                number = request.form['number']
                city = request.form['city']
                address = Address.query.get((street, number, city))
                if not address:
                    address = Address(street=street, number=number, city=city)
                    db.session.add(address)

                new_driver = Driver(
                    driverid=request.form['driverid'],
                    name=request.form['name'],
                    email=request.form['email'],
                    street=street,
                    number=number,
                    city=city
                )
                db.session.add(new_driver)
                db.session.commit()

            elif form_type == 'remove_driver':
                driver = Driver.query.get(request.form['driverid'])
                if driver:
                    db.session.delete(driver)
                    db.session.commit()

            return redirect(f"/manage-drivers?ssn={ssn}")

        drivers = Driver.query.all()
        return render_template("manage_drivers.html", drivers=drivers, manager_ssn=ssn)

