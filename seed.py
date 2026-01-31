from app import create_app, db
from app.models.organization import Organization
from app.models.service import Service
from app.models.site import Site
from app.models.admin_user import AdminUser
from seed_data.seed_data import data, services_data
from dotenv import load_dotenv

load_dotenv()
my_app = create_app()
with my_app.app_context():
    db.drop_all()
    db.create_all()

    # Seed Services
    for service_data in services_data:
        service = Service.from_dict(service_data)
        db.session.add(service)
    db.session.commit()

    # Seed Organizations and Sites
    for org_data in data:
        organization = Organization.from_dict(org_data["register"]["organization"])
        db.session.add(organization)
        # Get organization.id before committing
        db.session.flush() 

        # Seed Admin
        admin = AdminUser.from_dict(org_data["register"]["admin"])
        # Link admin to organization
        admin.organization = organization
        db.session.add(admin)

        for site_data in org_data["site"]:
            site = Site.from_dict(site_data, org_id=organization.id)

            # Link services to site
            service_names = site_data.get("services", [])
            services = db.session.scalars(
                db.select(Service).where(Service.name.in_(service_names))
            ).all()
            site.services = services

            db.session.add(site)

    db.session.commit()
    print("Database seeded successfully.")

