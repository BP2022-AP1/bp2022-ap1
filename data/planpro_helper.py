from orm_importer.importer import ORMImporter
from planproexporter import Generator
from railwayroutegenerator.routegenerator import RouteGenerator


def generate_plan_pro():
    polygon = "51.559286255426606 14.22958373936126 51.52956887166332 14.249153136333918 51.547102337669735 14.353866576275324 51.57915827365655 14.286231993755793"
    # This is somewhere west of Schwarze Pumpe.

    # Import from OSM/ORM
    topology = ORMImporter().run(polygon)

    # Generate Routes
    RouteGenerator(topology).generate_routes()

    # Write PlanPro
    generator = Generator()
    generator.generate(
        topology, "BP2022-AP1", "BP2022-AP1", "data/planpro/test_example"
    )


if __name__ == "__main__":
    generate_plan_pro()
