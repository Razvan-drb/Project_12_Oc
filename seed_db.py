#!/usr/bin/env python3
from epic_events.utils.database import init_db, get_db
from epic_events.models.user import User
from epic_events.models.client import Client
from epic_events.models.contract import Contract
from epic_events.models.event import Event
from datetime import datetime, timedelta
from epic_events.utils.display import print_success, print_info


def seed_database():
    """Seed the database with initial test data"""
    print_info("Seeding database with test data...")

    # Initialize database
    init_db()

    db = next(get_db())

    try:
        # Create management user
        management_user = User(
            full_name="Dawn Stanley",
            email="dawn@epicevents.com",
            department="management"
        )
        management_user.set_password("management123")
        db.add(management_user)

        # Create sales users
        sales_user1 = User(
            full_name="Bill Boquet",
            email="bill@epicevents.com",
            department="sales"
        )
        sales_user1.set_password("sales123")
        db.add(sales_user1)

        sales_user2 = User(
            full_name="Sarah Sales",
            email="sarah@epicevents.com",
            department="sales"
        )
        sales_user2.set_password("sales123")
        db.add(sales_user2)

        # Create support users
        support_user1 = User(
            full_name="Kate Hastroff",
            email="kate@epicevents.com",
            department="support"
        )
        support_user1.set_password("support123")
        db.add(support_user1)

        support_user2 = User(
            full_name="Alienor Vichum",
            email="alienor@epicevents.com",
            department="support"
        )
        support_user2.set_password("support123")
        db.add(support_user2)

        db.commit()
        print_success("Users created successfully")

        # Create clients
        client1 = Client(
            full_name="Kevin Casey",
            email="kevin@startup.io",
            phone="+678 123 456 78",
            company_name="Cool Startup LLC",
            commercial_contact_id=sales_user1.id
        )
        db.add(client1)

        client2 = Client(
            full_name="John Ouick",
            email="john.ouick@gmail.com",
            phone="+1 234 567 8901",
            company_name="Ouick Wedding Services",
            commercial_contact_id=sales_user1.id
        )
        db.add(client2)

        client3 = Client(
            full_name="Lou Bouzin",
            email="jacky@loubouzin.grd",
            phone="+666 12345",
            company_name="Lou Bouzin Group",
            commercial_contact_id=sales_user2.id
        )
        db.add(client3)

        db.commit()
        print_success("Clients created successfully")

        # Create contracts
        contract1 = Contract(
            client_id=client1.id,
            total_amount=5000.00,
            amount_due=2000.00,
            is_signed=True,
            commercial_contact_id=sales_user1.id
        )
        db.add(contract1)

        contract2 = Contract(
            client_id=client2.id,
            total_amount=3000.00,
            amount_due=3000.00,
            is_signed=False,
            commercial_contact_id=sales_user1.id
        )
        db.add(contract2)

        contract3 = Contract(
            client_id=client3.id,
            total_amount=7500.00,
            amount_due=0.00,
            is_signed=True,
            commercial_contact_id=sales_user2.id
        )
        db.add(contract3)

        db.commit()
        print_success("Contracts created successfully")

        # Create events
        event1 = Event(
            contract_id=contract1.id,
            client_id=client1.id,
            name="Cool Startup Launch Party",
            start_date=datetime.now() + timedelta(days=30),
            end_date=datetime.now() + timedelta(days=30, hours=6),
            location="53 Rue du Château, Paris",
            attendees=150,
            notes="Tech startup launch with investors and press",
            support_contact_id=support_user1.id
        )
        db.add(event1)

        event2 = Event(
            contract_id=contract3.id,
            client_id=client3.id,
            name="Lou Bouzin General Assembly",
            start_date=datetime.now() + timedelta(days=45),
            end_date=datetime.now() + timedelta(days=45, hours=3),
            location="Salle des fêtes de Mufflins",
            attendees=200,
            notes="Annual shareholder meeting with presentations",
            support_contact_id=None  # No support assigned yet
        )
        db.add(event2)

        db.commit()
        print_success("Events created successfully")

        print_success("Database seeding completed successfully!")
        print_info("\nTest users created:")
        print_info("Management: dawn@epicevents.com / management123")
        print_info("Sales: bill@epicevents.com / sales123")
        print_info("Sales: sarah@epicevents.com / sales123")
        print_info("Support: kate@epicevents.com / support123")
        print_info("Support: alienor@epicevents.com / support123")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
