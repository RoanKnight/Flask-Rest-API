from app import create_app, db
import click

app = create_app()

@app.cli.command("seed-database")
def seed_database():
  with app.app_context():
    db.drop_all()
    db.create_all()
    from app.seeders.user_seeder import seed_users
    seed_users()
    click.echo("Database refreshed and seeded successfully.")

@app.cli.command("drop-tables")
def drop_tables():
  with app.app_context():
    db.drop_all()
    click.echo("All tables dropped successfully.")

if __name__ == '__main__':
  app.run()
