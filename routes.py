from flask import render_template, request, redirect, url_for
from models import Client, Driver, Manager, Address, ClientAddress, CreditCard, Car, Model, DriverModel, Rent
from flask import flash
from sqlalchemy import text, func

def register_routes(app, db):
    # Routing back to the home page
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login-client', methods=['GET', 'POST'])
    def login_client():
        if request.method == 'POST':
            email = request.form['email']
            
            # Check if the client exists (you can use your database model here)
            client = Client.query.filter_by(email=email).first()
            
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
    
    # Signing into the driver dashboard
    @app.route('/driver-dashboard/<driver_id>')
    def driver_dashboard(driver_id):
        driver = Driver.query.filter_by(driverid=driver_id).first()
        if not Driver:
            return "Driver not found", 404
        return render_template('driver_dashboard.html', driver=driver)

    @app.route('/register-client', methods=['GET', 'POST'])
    def register_client():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            street = request.form['street']
            number = request.form['number']
            city = request.form['city']
            card_number = request.form['credit-card']

            # Step 1: Ensure address exists
            address = Address.query.filter_by(street=street, number=number, city=city).first()
            if not address:
                address = Address(street=street, number=number, city=city)
                db.session.add(address)
                db.session.commit()

            # Step 2: Create client
            new_client = Client(name=name, email=email)
            db.session.add(new_client)
            db.session.commit()

            # Step 3: Add client address
            client_address = ClientAddress(
                client_id=new_client.client_id,
                street=street,
                number=number,
                city=city
            )
            db.session.add(client_address)

            # Step 4: Add credit card
            credit_card = CreditCard(
                card_number=card_number,
                client_id=new_client.client_id,
                street=street,
                number=number,
                city=city
            )
            db.session.add(credit_card)

            db.session.commit()

            return f"""
                <h2>✅ Client {name} registered successfully!</h2>
                <p><a href="/">Return to Home</a></p>
                <form action="/login-client" method="get">
                    <button type="submit">Login Now</button>
                </form>
            """

        return render_template('register_client.html')

    @app.route('/register-driver', methods=['GET', 'POST'])
    def register_driver():
        if request.method == 'POST':
            name = request.form['name']
            number = request.form['number']
            street = request.form['street']
            city = request.form['city']

            # Step 1: Ensure address exists
            address = Address.query.filter_by(street=street, number=number, city=city).first()
            if not address:
                address = Address(street=street, number=number, city=city)
                db.session.add(address)
                db.session.commit()

            # Step 2: Check if driver already exists
            existing_driver = Driver.query.filter_by(name=name).first()
            if existing_driver:
                return """
                    <h2>❌ Driver with that name already exists.</h2>
                    <p><a href="/register-driver">Try Again</a></p>
                """

            # Step 3: Create new driver
            new_driver = Driver(name=name, street=street, number=number, city=city)
            db.session.add(new_driver)
            db.session.commit()

            # Step 4: Show success message
            return f"""
                <h2>✅ Driver {name} registered successfully!</h2>
                <p><a href="/">Return to Home</a></p>
                <form action="/login-driver" method="get">
                    <button type="submit">Login Now</button>
                </form>
            """

        return render_template('register_driver.html')

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

        # Rent count per model
        model_usage = db.session.query(
            Model.carid,
            Model.modelid,
            func.count(Rent.rent_id).label('rent_count')
        ).outerjoin(
            Rent, (Model.carid == Rent.carid) & (Model.modelid == Rent.modelid)
        ).group_by(Model.carid, Model.modelid).all()

        usage_lookup = {(entry.carid, entry.modelid): entry.rent_count for entry in model_usage}

        return render_template("manage_cars_models.html", cars=cars, manager_ssn=ssn, usage_lookup=usage_lookup)

    @app.route('/manage-drivers', methods=['GET', 'POST'])
    def manage_drivers():
        ssn = request.args.get('ssn', '1')

        if request.method == 'POST':
            form_type = request.form.get('form_type')

            if form_type == 'add_driver':
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

            elif form_type == 'assign_model':
                driverid = request.form['driverid']
                car_model = request.form['car_model']
                carid, modelid = map(int, car_model.split('-'))

                existing = DriverModel.query.filter_by(driverid=driverid, carid=carid, modelid=modelid).first()
                if not existing:
                    assignment = DriverModel(driverid=driverid, carid=carid, modelid=modelid)
                    db.session.add(assignment)
                    db.session.commit()


            elif form_type == 'remove_assignment':
                driverid = request.form['driverid']
                carid = request.form['carid']
                modelid = request.form['modelid']
                assignment = DriverModel.query.get((driverid, carid, modelid))
                if assignment:
                    db.session.delete(assignment)
                    db.session.commit()

            return redirect(f"/manage-drivers?ssn={ssn}")

        drivers = Driver.query.all()
        models = Model.query.all()
        assignments = DriverModel.query.all()
        return render_template("manage_drivers.html", drivers=drivers, models=models, assignments=assignments, manager_ssn=ssn)

    @app.route('/top-k-clients', methods=['GET', 'POST'])
    def top_k_clients():
        ssn = request.args.get('ssn', '1')
        clients = []
        k = None

        if request.method == 'POST':
            k = int(request.form['k'])
            query = text("""
                SELECT c.name, c.email, COUNT(r.rent_id) AS rent_count
                FROM client c
                JOIN rent r ON c.client_id = r.client_id
                GROUP BY c.client_id
                ORDER BY rent_count DESC
                LIMIT :k
            """)
            result = db.session.execute(query, {'k': k})
            clients = result.fetchall()

        return render_template('top_k_clients.html', clients=clients, k=k, manager_ssn=ssn)
    
    @app.route('/driver-stats')
    def driver_stats():
        ssn = request.args.get('ssn')
        
        query = text("""
            SELECT 
                d.name,
                COUNT(r.rent_id) AS total_rents,
                AVG(rv.rating) AS avg_rating
            FROM driver d
            LEFT JOIN rent r ON d.driverid = r.driverid
            LEFT JOIN review rv ON d.driverid = rv.driverid
            GROUP BY d.driverid, d.name
        """)
        results = db.session.execute(query).fetchall()

        return render_template('view_driver_stats.html', stats=results, manager_ssn=ssn)

    @app.route('/client-cross-city', methods=['GET', 'POST'])
    def client_cross_city():
        ssn = request.args.get('ssn')
        results = []
        
        if request.method == 'POST':
            city1 = request.form['city1']
            city2 = request.form['city2']
            
            query = text("""
                SELECT DISTINCT c.name, c.email
                FROM client c
                JOIN clientaddress ca ON c.client_id = ca.client_id
                JOIN rent r ON c.client_id = r.client_id
                JOIN driver d ON r.driverid = d.driverid
                WHERE ca.city = :city1 AND d.city = :city2
            """)
            results = db.session.execute(query, {'city1': city1, 'city2': city2}).fetchall()

        return render_template('client_cross_city.html', results=results, manager_ssn=ssn)




