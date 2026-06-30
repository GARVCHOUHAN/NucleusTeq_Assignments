from app.database.collections import projects_collection


class ProjectRepository:

    @staticmethod
    def create_project(
        project_document: dict
    ):

        projects_collection.insert_one(
            project_document
        )


    @staticmethod
    def get_project_by_name(
        project_name: str
    ):

        return projects_collection.find_one(
            {
                "name": project_name
            }
        )