"""
Project API client.
"""
from typing import Optional

from ._base import Base

LIST_PROJECTS_QUERY = """\
{
    projects {
        id
        name
        description
        isArchived
        user { handle }
    }
}
"""

CREATE_PROJECT_MUTATION = """\
mutation create_project($input: CreateProjectInput!) {
    createProject(input: $input) {
        result {
            id
        }
        errors {
            message
        }
    }
}
"""

UPDATE_PROJECT_MUTATION = """\
mutation update_project($id: ID!, $input: UpdateProjectInput!) {
    updateProject(id: $id, input: $input) {
        errors {
            message
        }
    }
}
"""

CLOSE_PROJECT_MUTATION = """\
mutation archive_project($id: ID!) {
    archiveProject(id: $id) {
        result {
            isArchived
        }
        errors {
            message
        }
    }
}
"""

OPEN_PROJECT_MUTATION = """\
mutation unarchive_project($id: ID!) {
    unarchiveProject(id: $id) {
        result {
            isArchived
        }
        errors {
            message
        }
    }
}
"""


class ProjectClient(Base):

    def list(self):
        """
        Lists projects for the authenticated user.
        """

        data = self.raw_query(query=LIST_PROJECTS_QUERY)
        return data['data']['projects']

    def create(self, name: str, description: Optional[str] = None):
        """
        Create a new project.
        """
        variables = {
            'input': {
                'name': name,
                'description': description
            }
        }
        data = self.raw_query(query=CREATE_PROJECT_MUTATION, variables=variables)
        return data['data']['createProject']['result']

    def update(self, id: str, name: Optional[str] = None, description: Optional[str] = None):
        """
        Update an existing project.
        """
        variables = {
            'id': id,
            'input': {
            }
        }

        if name is not None:
            variables['input']['name'] = name
        if description is not None:
            variables['input']['description'] = description

        data = self.raw_query(query=UPDATE_PROJECT_MUTATION, variables=variables)
        result = data['data']['updateProject']['errors']
        if result:
            result = {
                'errors': result,
                'accepted': False
            }
        else:
            result = {}
            result['accepted'] = True
        return result

    def unarchive(self, id: str):
        """
        Unarchives an archived project.
        """
        data = self.raw_query(query=OPEN_PROJECT_MUTATION, variables={'id': id})
        return data['data']['unarchiveProject']

    def archive(self, id: str):
        """
        Archive a project.
        """
        data = self.raw_query(query=CLOSE_PROJECT_MUTATION, variables={'id': id})
        return data['data']['archiveProject']
