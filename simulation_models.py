from datetime import datetime
from extensions import db

# fmt: off


# Define association tables
simulation_config_vehicle_association = db.Table(
    "simulation_condig_vehicle_association",
    db.Column("simulation_config_id", db.Integer, db.ForeignKey("simulation_config.id"), primary_key=True),
    db.Column("vehicle_id", db.Integer, db.ForeignKey("vehicle.id"), primary_key=True)
)

class Vehicle(db.Model):
    __tablename__ = "vehicle"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    
    sensor_information = db.Column(db.JSON, nullable=False) # Sensor decription and properties could go on a separate table
    physical_properties = db.Column(db.JSON, nullable=False) # Simentions, mass, etc.

    def __repr__(self):
        return f"<vehicle {self.name}>"

class SimulationType(db.Model):
    __tablename__ = "simulation_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<SimulationType {self.name}>"


class SimulationConfig(db.Model):
    __tablename__ = "simulation_config"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    simulation_type_id = db.Column(db.Integer, db.ForeignKey("simulation_type.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # One simulation can have many vehicles
    vehicles = db.relationship("Vehicle", secondary=simulation_config_vehicle_association, backref="simulation_config")

    # These could be in SimulationType, but it seems to give more flexibility to have them here
    environmental_conditions = db.Column(db.JSON, nullable=False) # Weather, time of day, temperature, preassure, etc.
    initial_conditions = db.Column(db.JSON, nullable=False) # initial positions, velocities, etc.
    physical_constants = db.Column(db.JSON, nullable=False) # It could be useful to make this a table of its own
    time_settings = db.Column(db.JSON, nullable=False) # Time step, duration of simulation, etc.
    traffic_rules = db.Column(db.JSON, nullable=False) # Traffic rules, speed limits, etc.

    success_definition = db.Column(db.JSON, nullable=False) # What is considered a successful simulation? (e.g. no collisions, no near misses, etc.)


    def __repr__(self):
        return f"<SimulationConfig {self.id}>"
    
class SimulationResult(db.Model):
    __tablename__ = "simulation_result"

    id = db.Column(db.Integer, primary_key=True)
    simulation_config_id = db.Column(db.Integer, db.ForeignKey("simulation_config.id"), nullable=False)
    finished_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    success = db.Column(db.JSON, nullable=False) # Parameters that define success (e.g. no collisions, no near misses, etc.)
    navigation_data = db.Column(db.JSON, nullable=False) # Route, time taken, distance travel, speed (avg, min, max), etc.
    safety_metrics = db.Column(db.JSON, nullable=False) # Collisions, near misses, trafic rules violations, etc.
    vehicle_system_performance = db.Column(db.JSON, nullable=False) # Object detection accuracy, CPU, response times, etc.

    def __repr__(self):
        return f"<SimulationResult {self.success}>"
