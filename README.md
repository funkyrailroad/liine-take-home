# Start postgres container
docker run -d -p 5432:5432 \
            -e POSTGRES_DB=liine \
            -e POSTGRES_PASSWORD=takehome \
            -e POSTGRES_USER=postgres \
            --name postgres \
            postgres

# Build image
docker build -t liine-takehome .

# Run container in dev version
docker run --rm -it --network=host -v $(pwd):/outside --entrypoint bash liine-takehome

# Start server within container
cd outside/liine_take_home/
python manage.py runserver 0:8000

# Populate the weekly opening hours table
python manage.py load_csv_to_weekly_table
