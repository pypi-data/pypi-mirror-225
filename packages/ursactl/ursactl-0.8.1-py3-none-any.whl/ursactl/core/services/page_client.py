"""
Page Service client
"""

from ._base import Base

LIST_PAGES_QUERY = """
query list_pages($id: String!) {
    project(handleName: $id) {
        pages {
            id
            title
            path
            isSynced
            tags
        }
    }
}
"""

CREATE_PAGE_MUTATION = """
mutation create_page($input: CreatePageInput!) {
    createPage(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            title
            path
        }
    }
}
"""

SYNC_PAGE_MUTATION = """
mutation sync_page($input: SyncPageInput!) {
    syncPage(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            title
            path
        }
    }
}
"""

UPDATE_PAGE_MUTATION = """
mutation update_page($id: ID!, $input: UpdatePageInput!) {
    updatePage(id: $id, input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            title
            path
        }
    }
}
"""

GET_PAGE_BY_PATH_QUERY = """
query get_page_by_path($path: String!, $project: String!) {
    project(handleName: $project) {
        page(limit: 1, filter: { path: { eq: $path } }) {
            id
            path
            isSynced
            tags
        }
    }
}
"""

GET_PAGE_QUERY = """
query get_page($id: ID!) {
    page(id: $id) {
        id
        path
        title
        isSynced
        tags
    }
}
"""

GET_PAGE_CONTENT_QUERY = """
query get_page_content($id: ID!) {
    page(id: $id) {
        id
        path
        title
        content
        isSynced
        tags
    }
}
"""

DELETE_PAGE_MUTATION = """\
mutation delete_page($id: ID!) {
    deletePage(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""

DELETE_SYNCED_PAGE_MUTATION = """\
mutation delete_synced_page($id: ID!) {
    deleteSyncedPage(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            path
        }
    }
}
"""


class PageClient(Base):
    """
    Client providing access to the Page functions.
    """
    def list_pages(self, project_uuid=None):
        """
        Returns a list of available pages.
        """
        result = self.raw_query(LIST_PAGES_QUERY, {
            'id': project_uuid
        })
        return result['data']['project']['pages']

    def get_page(self, uuid=None, path=None, project_uuid=None):
        """
        Returns more detail about a page - but not the content.
        """
        if uuid is None and path is None:
            raise ValueError("Must specify either uuid or path")
        if uuid is None:
            result = self.raw_query(GET_PAGE_BY_PATH_QUERY, {
                'project': project_uuid,
                'path': path
            })

            return result['data']['project']['page']

        result = self.raw_query(GET_PAGE_QUERY, {
            'id': uuid
        })
        return result['data']['page']

    def create_page(self, project_uuid=None, title=None, path=None, content=None, tags=None):
        """
        Create a new page.
        """
        if project_uuid is None:
            raise AttributeError("pages must be assigned to a project.")
        if path is None:
            raise AttributeError("page path must be provided.")
        if content is None:
            raise AttributeError("page content must be provided.")
        variables = {
            'input': {
                'project': project_uuid,
                'path': path,
                'content': content,
            }
        }

        if title is not None:
            variables['input']['title'] = title
        if tags is not None:
            variables['input']['tags'] = tags
        result = self.raw_query(query=CREATE_PAGE_MUTATION, variables=variables)

        return result['data']['createPage']['result']

    def sync_page(self, project_uuid=None, title=None, path=None, content=None, tags=None):
        """
        Sync a page.
        """
        if project_uuid is None:
            raise AttributeError("pages must be assigned to a project.")
        if path is None:
            raise AttributeError("page path must be provided.")
        if content is None:
            raise AttributeError("page content must be provided.")
        variables = {
            'input': {
                'project': project_uuid,
                'path': path,
                'content': content,
            }
        }

        if title is not None:
            variables['input']['title'] = title
        if tags is not None:
            variables['input']['tags'] = tags
        result = self.raw_query(query=SYNC_PAGE_MUTATION, variables=variables)

        return result['data']['syncPage']['result']

    def update_page(self, uuid=None, title=None, path=None, content=None, tags=None):
        """
        Update a page.
        """
        if uuid is None:
            raise AttributeError("page uuid must be provided.")
        variables = {
            'id': uuid,
            'input': {}
        }
        if title is not None:
            variables['input']['title'] = title
        if path is not None:
            variables['input']['path'] = path
        if content is not None:
            variables['input']['content'] = content
        if tags is not None:
            variables['input']['tags'] = tags
        result = self.raw_query(query=UPDATE_PAGE_MUTATION, variables=variables)

        return result['data']['updatePage']['result']

    def delete_page(self, id, project_uuid=None):
        """
        Delete a page.
        """
        if self.is_uuid(id):
            variables = {
                'id': id
            }
        else:
            page = self.get_page(path=id, project_uuid=project_uuid)
            if page is None:
                return {}
            variables = {'id': page['id']}

        result = self.raw_query(query=DELETE_PAGE_MUTATION, variables=variables)

        return result['data']['deletePage']

    def delete_synced_page(self, id, project_uuid=None):
        """
        Delete a synced page.
        """
        if self.is_uuid(id):
            variables = {
                'id': id
            }
        else:
            page = self.get_page(path=id, project_uuid=project_uuid)
            if page is None:
                return {}
            variables = {'id': page['id']}

        result = self.raw_query(query=DELETE_SYNCED_PAGE_MUTATION, variables=variables)

        return result['data']['deleteSyncedPage']
