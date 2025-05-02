from flask import render_template, request, redirect, url_for
from models import Client, Driver, Manager, Address, ClientAddress, CreditCard, Car, Model, Rent, DriverModel, Review
from flask import flash
from sqlalchemy import func, distinct
from datetime import datetime
from sqlalchemy import text
import re

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
                return redirect(url_for('client_dashboard', client_id=client.client_id))
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
    
    # Updating the driver address
    @app.route('/update-address/<driver_id>', methods=['GET', 'POST'])
    def update_address(driver_id):
        driver = Driver.query.filter_by(driverid=driver_id).first()
        if not driver:
            return "Driver not found", 404

        if request.method == 'POST':
            street = request.form['street']
            number = request.form['number']
            city = request.form['city']

            # Step 1: Ensure address exists in address table
            address = Address.query.filter_by(street=street, number=number, city=city).first()
            if not address:
                address = Address(street=street, number=number, city=city)
                db.session.add(address)
                db.session.commit()

            # Step 2: Update driver's address
            driver.street = street
            driver.number = number  
            driver.city = city      
            db.session.commit()

            return redirect(f"/driver-dashboard/{driver_id}")   
           
        return render_template('update_address.html', driver=driver)

    @app.route('/register-client', methods=['GET', 'POST'])
    def register_client():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            new_client = Client(name=name, email=email)
            db.session.add(new_client)
            db.session.commit()

            client_id = new_client.client_id  # ✅ correct field name

            # Add up to 2 addresses
            for i in [1, 2]:
                street = request.form.get(f'street{i}')
                number = request.form.get(f'number{i}')
                city = request.form.get(f'city{i}')
                if street and number and city:
                    address = Address.query.filter_by(street=street, number=number, city=city).first()
                    if not address:
                        address = Address(street=street, number=number, city=city)
                        db.session.add(address)
                        db.session.commit()
                    db.session.add(ClientAddress(client_id=client_id, street=address.street, number=address.number, city=address.city))

            # Add up to 2 credit cards
            for i in [1, 2]:
                card = request.form.get(f'card{i}')
                street = request.form.get(f'card_street{i}')
                number = request.form.get(f'card_number{i}')
                city = request.form.get(f'card_city{i}')
                if card and street and number and city:
                    billing_address = Address.query.filter_by(street=street, number=number, city=city).first()
                    if not billing_address:
                        billing_address = Address(street=street, number=number, city=city)
                        db.session.add(billing_address)
                        db.session.commit()
                    db.session.add(CreditCard(
                    card_number=card,
                    client_id=client_id,
                    street=billing_address.street,
                    number=billing_address.number,
                    city=billing_address.city
                    )
                )

            db.session.commit()
            return redirect(url_for('login_client'))

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

    # Route for drivers to manage their cars
    @app.route('/manage-cars/<driver_id>', methods=['GET', 'POST'])
    def driver_manage_cars(driver_id):
        driver = Driver.query.filter_by(driverid=driver_id).first()
        if not driver:
            return "Driver not found", 404

        # Get all car models this driver can drive
        driver_models = db.session.query(
            DriverModel, Car, Model
        ).join(
            Model, (DriverModel.carid == Model.carid) & (DriverModel.modelid == Model.modelid)
        ).join(
            Car, DriverModel.carid == Car.carid
        ).filter(
            DriverModel.driverid == driver_id
        ).all()

        # Get all available car models not assigned to this driver
        available_models = db.session.query(
            Model, Car
        ).join(
            Car, Model.carid == Car.carid
        ).outerjoin(
            DriverModel, (Model.carid == DriverModel.carid) & 
                         (Model.modelid == DriverModel.modelid) & 
                         (DriverModel.driverid == driver_id)
        ).filter(
            DriverModel.driverid == None
        ).all()

        if request.method == 'POST':
            form_type = request.form.get('form_type')

            if form_type == 'add_model':
                car_model = request.form.get('car_model')
                if car_model:
                    carid, modelid = map(int, car_model.split('-'))
                    
                    # Check if assignment already exists
                    existing = DriverModel.query.filter_by(
                        driverid=driver_id, 
                        carid=carid, 
                        modelid=modelid
                    ).first()
                    
                    if not existing:
                        # Add new driver-model assignment
                        new_assignment = DriverModel(
                            driverid=driver_id,
                            carid=carid,
                            modelid=modelid
                        )
                        db.session.add(new_assignment)
                        db.session.commit()

            elif form_type == 'remove_model':
                carid = request.form.get('carid')
                modelid = request.form.get('modelid')
                
                if carid and modelid:
                    # Remove the driver-model assignment
                    assignment = DriverModel.query.filter_by(
                        driverid=driver_id,
                        carid=carid,
                        modelid=modelid
                    ).first()
                    
                    if assignment:
                        db.session.delete(assignment)
                        db.session.commit()

            # Redirect to refresh the page after POST
            return redirect(f"/manage-cars/{driver_id}")

        return render_template('driver_manage_cars.html', 
                               driver=driver, 
                               driver_models=driver_models, 
                               available_models=available_models)



    
    #------------------------------------------------------------------------------------------------------------------------------------------#
    #----------------------------------------------------------------- CLIENT -----------------------------------------------------------------#
    #------------------------------------------------------------------------------------------------------------------------------------------#

    @app.route('/client-dashboard')
    def client_dashboard():
        client_id = request.args.get('client_id')
        client = Client.query.get(client_id)
        return render_template("client_dashboard.html", client_name=client.name, client_id=client.client_id)


    @app.route('/search-cars', methods=['GET'])
    def search_cars():
        selected_date = request.args.get('date')
        if not selected_date:
            return render_template('search_cars.html', available_cars=[])

        # Convert date input to datetime object
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            return render_template('search_cars.html', available_cars=[])

        # Step 1: Find all model IDs that are already rented on this date
        rented_model_ids = db.session.query(Car.model_id).join(Car.rents).filter(
            func.date(Rent.date) == selected_date
        ).distinct()

        # Step 2: Find all model IDs with at least one qualified, available driver on this date
        qualified_models = db.session.query(Model).join(Driver.can_drive).filter(
            ~Driver.rents.any(func.date(Rent.date) == selected_date)
        ).filter(
            ~Model.id.in_(rented_model_ids)
        ).distinct().all()

        return render_template('search_cars.html', available_cars=qualified_models)


    @app.route("/view-rents")
    def view_rents():
        client_id = request.args.get("client_id")

        bookings = db.session.query(
            Rent.rent_date,
            Model.modelid,
            Model.color,
            Car.carid,
            Driver.name.label("driver_name")
        ).join(Model, (Rent.modelid == Model.modelid) & (Rent.carid == Model.carid))\
        .join(Car, Rent.carid == Car.carid)\
        .join(Driver, Rent.driverid == Driver.driverid)\
        .filter(Rent.client_id == client_id)\
        .order_by(Rent.rent_date.asc()).all()

        return render_template("view_rents.html", bookings=bookings)

    @app.route("/review-driver", methods=["GET", "POST"])
    def review_driver():
        client_id = request.args.get("client_id")

        if request.method == "POST":
            driver_id = request.form["driver_id"]
            rating = request.form["rating"]
            comment = request.form["comment"]

            review = Review(
                client_id=client_id,
                driverid=driver_id,
                rating=rating,
                comment=comment
            )
            db.session.add(review)
            db.session.commit()
            flash("Review submitted!", "success")
            return redirect(url_for("review_driver", client_id=client_id))

        bookings = db.session.query(
            Rent.rent_id,
            Rent.rent_date,
            Model.modelid,
            Model.color,
            Car.carid,
            Driver.driverid,
            Driver.name.label("driver_name")
        ).join(Model, (Rent.modelid == Model.modelid) & (Rent.carid == Model.carid))\
        .join(Car, Rent.carid == Car.carid)\
        .join(Driver, Rent.driverid == Driver.driverid)\
        .filter(Rent.client_id == client_id)\
        .order_by(Rent.rent_date.asc()).all()

        drivers = Driver.query.all()

        return render_template("review_driver.html", bookings=bookings, drivers=drivers, client_id=client_id)


    @app.route("/book-rent", methods=["GET", "POST"])
    def book_rent():
        client_id = request.args.get("client_id") if request.method == "GET" else request.form.get("client_id")

        if not client_id:
            return "Client ID required", 400

        client_id = int(client_id)

        if request.method == "POST":
            model_id = request.form.get("car_model")
            date_str = request.form.get("date")
            best_driver = request.form.get("best_driver")

            if not model_id or not date_str:
                return "Missing data", 400

            try:
                rent_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return "Invalid date format", 400

            # Extract carid from car_model string like "Model 222 (Car 123)"
            match = re.search(r'\(Car (\d+)\)', model_id)
            if not match:
                return "Invalid car model format", 400
            carid = int(match.group(1))
            modelid = int(model_id.split()[1])

            selected_model = Model.query.filter_by(carid=carid, modelid=modelid).first()
            if not selected_model:
                return "Model not found", 404

            if best_driver:  # checkbox selected
                # Get drivers who can drive this car+model and are not booked for the same date
                eligible_drivers = db.session.query(DriverModel.driverid).filter_by(carid=car_id, modelid=model_id).subquery()
                
                available_drivers = db.session.query(Driver).filter(Driver.driverid.in_(eligible_drivers)).filter(
                    ~db.session.query(Rent).filter(
                        and_(
                            Rent.rent_date == rent_date,
                            Rent.driverid == Driver.driverid
                        )
                    ).exists()
                ).all()

                # Calculate average rating for each available driver
                best_driver_id = None
                highest_avg = -1
                for driver in available_drivers:
                    ratings = db.session.query(Review.rating).filter_by(driverid=driver.driverid).all()
                    avg = sum(r[0] for r in ratings) / len(ratings) if ratings else 0
                    if avg > highest_avg:
                        highest_avg = avg
                        best_driver_id = driver.driverid

                if not best_driver_id:
                    return "No available drivers for this model on that date."
                driver_id = best_driver_id
            else:
                rent = Rent(
                    rent_date=rent_date,
                    client_id=client_id,
                    carid=selected_model.carid,
                    modelid=selected_model.modelid,
                    driverid=1  # dummy for now
                )
                db.session.add(rent)
                db.session.commit()
                return redirect(url_for("client_dashboard", client_id=client_id))

        models = Model.query.all()
        model_choices = [f"Model {m.modelid} (Car {m.carid})" for m in models]
        return render_template("book_rent.html", models=model_choices, client_id=client_id)
    
    @app.route('/submit-review', methods=['POST'])
    def submit_review():
        client_id = request.form.get("client_id")
        driver_id = request.form.get("driver_id")
        rating = request.form.get("rating")
        message = request.form.get("message")

        # Check if this client ever had a rent with this driver
        valid_rent = db.session.query(Rent).filter_by(client_id=client_id, driverid=driver_id).first()

        if not valid_rent:
            return "You can't review this driver – no rental history."

        new_review = Review(
            driverid=driver_id,
            client_id=client_id,
            rent_id=valid_rent.rent_id,
            message=message,
            rating=int(rating)
        )
        db.session.add(new_review)
        db.session.commit()
        return redirect(f"/client-dashboard?client_id={client_id}")